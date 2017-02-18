#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An example Kik bot implemented in Python.

It's designed to greet the user, send a suggested response and replies to them with their profile picture.
Remember to replace the BOT_USERNAME_HERE, BOT_API_KEY_HERE and WEBHOOK_HERE fields with your own.

See https://github.com/kikinteractive/kik-python for Kik's Python API documentation.

Apache 2.0 License

(c) 2016 Kik Interactive Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.

"""

from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, PictureMessage, \
    SuggestedResponseKeyboard, TextResponse, StartChattingMessage
import random


class KikBot(Flask):
    """ Flask kik bot application class"""

    def __init__(self, kik_api, import_name, static_path=None, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False,
                 root_path=None):

        self.kik_api = kik_api

        super(KikBot, self).__init__(import_name, static_path, static_url_path, static_folder, template_folder,
                                     instance_path, instance_relative_config, root_path)

        self.route("/incoming", methods=["POST"])(self.incoming)
        self.question_ans = True
        self.questions = [('This statement is False.', False), ('This statement is True.', True)]
        self.question_count = 0


    def incoming(self):
        """Handle incoming messages to the bot. All requests are authenticated using the signature in
        the 'X-Kik-Signature' header, which is built using the bot's api key (set in main() below).
        :return: Response
        """
        # verify that this is a valid request
        if not self.kik_api.verify_signature(
                request.headers.get("X-Kik-Signature"), request.get_data()):
            return Response(status=403)

        messages = messages_from_json(request.json["messages"])

        response_messages = []

        for message in messages:
            user = self.kik_api.get_user(message.from_user)
            # Check if its the user's first message. Start Chatting messages are sent only once.
            if isinstance(message, StartChattingMessage):

                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Welcome to StudyHelper!"))

                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Type 'q' or 'question' to be asked a new question!"))

            # Check if the user has sent a text message.
            elif isinstance(message, TextMessage):
                user = self.kik_api.get_user(message.from_user)
                message_body = message.body.lower()

                if message_body.split()[0] in ["q", "question"] and self.question_count < len(self.questions):

                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body=self.questions[self.question_count][0],
                        keyboards=[SuggestedResponseKeyboard(
                            responses=[TextResponse("True"),
                                       TextResponse("False")])]))
                    self.question_ans = self.questions[self.question_count][1]

                elif message_body.split()[0] in ["q", "question"] and self.question_count == len(self.questions):
                    self.question_count = 0
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="You've gone through all of the questions, so we will start you back from the beginning."))

                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body=self.questions[self.question_count][0],
                        keyboards=[SuggestedResponseKeyboard(
                            responses=[TextResponse("True"),
                                       TextResponse("False")])]))
                    self.question_ans = self.questions[self.question_count][1]

                elif message_body == "true" and self.question_ans == True:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="That's correct! Good work!"))
                    self.question_count += 1
                elif message_body == "false" and self.question_ans == True:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Oh no! The answer was True!"))
                    self.question_count += 1
                elif message_body == "false" and self.question_ans == False:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="That's correct! Good work!"))
                    self.question_count += 1
                elif message_body == "true" and self.question_ans == False:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Oh no! The answer was False!"))
                    self.question_count += 1
                # If response was not found.
                else:
                    response_messages.append(TextMessage(
                        to=message.from_user,
                        chat_id=message.chat_id,
                        body="Sorry {}, I didn't quite understand that. How are you?".format(user.first_name),
                        keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))
            elif isinstance(message, PictureMessage):
                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="yes"))
            # If its not a text message, give them another chance to use the suggested responses
            else:

                response_messages.append(TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body="Sorry, I didn't quite understand that. How are you, {}?".format(user.first_name),
                    keyboards=[SuggestedResponseKeyboard(responses=[TextResponse("Good"), TextResponse("Bad")])]))

            # We're sending a batch of messages. We can send up to 25 messages at a time (with a limit of
            # 5 messages per user).

            self.kik_api.send_messages(response_messages)

        return Response(status=200)

if __name__ == "__main__":
    """ Main program """
    kik = KikApi('thisbotbestbot', '5228b346-4e6c-423f-820d-316baae9beda')
    # For simplicity, we're going to set_configuration on startup. However, this really only needs to happen once
    # or if the configuration changes. In a production setting, you would only issue this call if you need to change
    # the configuration, and not every time the bot starts.
    kik.set_configuration(Configuration(webhook='http://29e3c70f.ngrok.io/incoming'))
    app = KikBot(kik, __name__)
    app.run(port=8080, host='127.0.0.1', debug=True)
