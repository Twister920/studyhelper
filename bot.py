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

from questionBuilder import *
import imageAnalytics
import noteAnalytics

LISTENING_SERVER = "http://1bd1333c.ngrok.io"

class KikBot(Flask):
    """ Flask kik bot application class"""

    def __init__(self, kik_api, import_name, static_path=None, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False,
                 root_path=None):

        self.kik_api = kik_api

        super(KikBot, self).__init__(import_name, static_path, static_url_path, static_folder, template_folder,
                                     instance_path, instance_relative_config, root_path)

        self.route("/incoming", methods=["POST"])(self.incoming)
        self.questions = None
        self.question_count = 0

        self.response_messages = []

        self.message = None
        self.user = None

    def incoming(self):
        """Handle incoming messages to the bot. All requests are authenticated using the signature in
        the 'X-Kik-Signature' header, which is built using the bot's api key (set in main() below).
        :return: Response
        """

        # Verify that this is a valid request
        if not self.kik_api.verify_signature(
                request.headers.get("X-Kik-Signature"), request.get_data()):
            return Response(status=403)

        messages = messages_from_json(request.json["messages"])

        for message in messages:
            self.message = message
            self.user = self.kik_api.get_user(message.from_user)

            # Check if its the user's first message. Start Chatting messages are sent only once.
            if isinstance(message, StartChattingMessage):
                self.send_first_message()

            # Check if the user has sent a picture
            elif isinstance(message, PictureMessage):
                self.send_message("Thanks! Reading notes...")

                notes = imageAnalytics.get_text_from_url(message.pic_url)
                sorted_notes = noteAnalytics.get_json_from_notes(notes)

                self.send_message("Creating questions...")

                self.questions = QuestionBuilder().create_questions(sorted_notes)

            # Check if the user has sent a text message.
            elif isinstance(message, TextMessage):
                if self.questions == None:
                    self.send_message("Hi! To get started, please take a picture of your notes.")
                    self.send_message("Then the quizzing can begin")

                else:
                    self.check_answer(self.message.body)
                    self.question_count += 1
                    print (self.question_count)
                    print (len(self.questions))

                if self.questions != None and self.question_count == len(self.questions):
                    self.question_count = 0
                    self.send_message("You've gone through all of the questions, so we will start you back from the beginning.")

            # If its not a text message, give them another chance to use the suggested responses
            else:
                self.send_message("Sorry {}, I didn't get that. Try again?".format(self.user.first_name))



            if self.questions != None:
                self.questions[self.question_count].ask_question(self)

            # We're sending a batch of messages. We can send up to 25 messages at a time (with a limit of
            # 5 messages per user).

            self.kik_api.send_messages(self.response_messages)

            self.response_messages = []

        return Response(status=200)

    # Checks user's answer
    def check_answer(self, user_answer):
        question = self.questions[self.question_count]

        if question.check_answer(user_answer):
            self.send_message("That's correct! Good work!")
        else:
            self.send_message("Oh no that's wrong, the correct answer was: " + str(question.answer) + ".")

    def send_first_message(self):
        self.send_message("Welcome to StudyHelper!")
        self.send_message("Type 'q' or 'question' to be asked a new question!")
        self.send_message("Alternatively, type 'true_false' for true or false or 'blanks' for fill in the blanks")

    def send_message(self, message):
        self.response_messages.append(TextMessage(
            to=self.message.from_user,
            chat_id=self.message.chat_id,
            body=message))





if __name__ == "__main__":
    """ Main program """
    kik = KikApi('studyhelper', 'be6f061d-69f2-401a-9fad-0a31aa9cac68')
    # For simplicity, we're going to set_configuration on startup. However, this really only needs to happen once
    # or if the configuration changes. In a production setting, you would only issue this call if you need to change
    # the configuration, and not every time the bot starts.
    kik.set_configuration(Configuration(webhook= LISTENING_SERVER + '/incoming'))
    app = KikBot(kik, __name__)
    app.run(port=8080, host='127.0.0.1', debug=True)







