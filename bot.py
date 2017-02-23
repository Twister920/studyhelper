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

LISTENING_SERVER = "http://ea390353.ngrok.io"

NO_RESPONSE = -1
REPLACE_NOTES = 0
ANSWER = 1
CONTINUE_QUIZZING = 2
UPLOAD_NOTES = 3
UPLOADING_MORE_NOTES = 4
CANCEL = 5

NO_ACTION = 5
ADD_NOTES = 6
REPLACE_NOTES = 7


class KikBot(Flask):
    """ Flask kik bot application class"""

    def __init__(self, kik_api, import_name, static_path=None, static_url_path=None, static_folder="static",
                 template_folder="templates", instance_path=None, instance_relative_config=False,
                 root_path=None):

        self.kik_api = kik_api

        super(KikBot, self).__init__(import_name, static_path, static_url_path, static_folder, template_folder,
                                     instance_path, instance_relative_config, root_path)

        self.route("/incoming", methods=["POST"])(self.incoming)

        self.quiz = QuizCreator()
        self.pic_url = None

        # Has the user sent their first message yet
        self.first_message = True

        # What the bot is currently waiting on a response for
        self.awaiting_response = UPLOAD_NOTES
        self.awaiting_action = NO_ACTION
        self.next_action = NO_ACTION

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
                self.send_message("Welcome to StudyHelper!")

            # Check if the user has sent a picture
            elif isinstance(message, PictureMessage):
                if self.quiz.is_empty() or self.awaiting_action == UPLOAD_NOTES:
                    if self.quiz.is_empty():
                        self.send_message("Thanks! Reading notes...")
                        self.send_message("Creating questions...")
                        self.quiz.add_notes_from_picture(message.pic_url)

                    elif self.next_action == ADD_NOTES:
                        self.quiz.add_notes_from_picture(message.pic_url)

                    elif self.next_action == REPLACE_NOTES:
                        self.quiz.replace_notes_from_picture(message.pic_url)

                    self.send_message_with_responses("What would you like to do now?",
                                                    ["Add More", "Replace", "Cancel", "Start Quiz"])

                    self.awaiting_action = UPLOAD_NOTES
                    self.awaiting_response = UPLOADING_MORE_NOTES

                else:
                    # Saves the picture url
                    self.pic_url = message.pic_url
                    self.send_message_with_responses("I already have some notes, should I add to them or replace them?",
                                                     ["Add", "Replace", "Cancel"])

                    self.awaiting_response = REPLACE_NOTES

            # Check if the user has sent a text message.
            elif isinstance(message, TextMessage):
                # Prompt user to upload notes if there are none
                if self.awaiting_response == UPLOAD_NOTES:
                    self.send_message("To get started, please take a picture of your notes.")
                    self.send_message("Then the quizzing can begin")

                elif self.awaiting_response == CANCEL:
                    response = message.body.strip().lower()[0]

                    if response == 'c':
                        if self.quiz.is_empty():
                            self.awaiting_action = UPLOAD_NOTES
                            self.awaiting_response = UPLOAD_NOTES
                        else:
                            self.send_message_with_responses("Okay! What would you like to do now?",
                                                    ["Add More", "Replace", "Cancel", "Start Quiz"])

                            self.awaiting_action = UPLOAD_NOTES
                            self.awaiting_response = UPLOADING_MORE_NOTES

                # If the user
                elif self.awaiting_response == UPLOADING_MORE_NOTES:
                    response = message.body.strip().lower()[0]

                    if response == 'a':
                        self.send_message("Okay! Please upload the notes to add, or type 'Cancel'.")
                        self.awaiting_response = CANCEL
                        self.awaiting_action = UPLOAD_NOTES
                        self.next_action = ADD_NOTES

                    elif response == 'r':
                        self.send_message("Okay! Please upload notes to replace, or type 'Cancel'.")
                        self.awaiting_response = CANCEL
                        self.awaiting_action = UPLOAD_NOTES
                        self.next_action = REPLACE_NOTES

                    elif response == 'c':
                        self.send_message("Okay!")
                        self.quiz.reset()
                        self.awaiting_response = UPLOAD_NOTES
                        self.awaiting_action = NO_ACTION

                    elif response == 's':
                        self.send_message("Okay! Starting the quiz...")
                        self.awaiting_response = ANSWER
                        self.awaiting_action = NO_ACTION

                elif self.awaiting_response == REPLACE_NOTES:
                    response = message.body.strip().lower()[0]

                    if response == 'a':
                        self.send_message("Okay! Adding new notes...")
                        self.quiz.add_notes_from_picture(message.pic_url)

                    elif response == 'r':
                        self.send_message("Okay! Replacing notes...")
                        self.quiz.replace_notes_from_picture(message.pic_url)

                    elif response == 'c':
                        self.send_message("Okay! Keeping old notes...")

                    self.awaiting_response = ANSWER

                # After the questions have run out, checks if user wants to continue or stop
                elif self.awaiting_response == CONTINUE_QUIZZING:
                    response = message.body.strip().lower()[0]

                    if response == 'y':
                        self.quiz.regenerate_questions()
                        self.send_message("Okay! Starting over...")
                        self.awaiting_response = ANSWER

                    elif response == 'n':
                        self.send_message("Okay!")
                        self.awaiting_response = UPLOAD_NOTES

                # Check the user's answer
                elif self.awaiting_response == ANSWER:
                    self.quiz.check_answer(self, self.message.body)


            # If its not a text message, give them another chance to use the suggested responses
            else:
                self.send_message("Sorry {}, I didn't get that. Try again?".format(self.user.first_name))


            if not self.quiz.is_empty() and self.awaiting_response == ANSWER:
                # Tries to ask user a question, returns false if it fails
                if not self.quiz.ask_next_question(self):
                    self.send_message_with_responses("You've gone through all of the questions, would you like to start over?",
                                                     ["Yes", "No"])
                    self.awaiting_response = CONTINUE_QUIZZING
                else:
                    self.awaiting_response = ANSWER

            # We're sending a batch of messages. We can send up to 25 messages at a time (with a limit of
            # 5 messages per user).

            if self.response_messages != []:
                self.kik_api.send_messages(self.response_messages)

            self.response_messages = []

        return Response(status=200)




    def send_message(self, message):
        self.response_messages.append(TextMessage(
            to=self.message.from_user,
            chat_id=self.message.chat_id,
            body=message))

    def send_message_with_responses(self, message, responses):
        text_responses = []

        for response in responses:
            text_responses.append(TextResponse(response))

        self.response_messages.append(TextMessage(
            to=self.message.from_user,
            chat_id=self.message.chat_id,
            body=message,
            keyboards=[SuggestedResponseKeyboard(
            responses=text_responses)]))




if __name__ == "__main__":
    """ Main program """
    kik = KikApi('studyhelper', 'be6f061d-69f2-401a-9fad-0a31aa9cac68')
    # For simplicity, we're going to set_configuration on startup. However, this really only needs to happen once
    # or if the configuration changes. In a production setting, you would only issue this call if you need to change
    # the configuration, and not every time the bot starts.
    kik.set_configuration(Configuration(webhook= LISTENING_SERVER + '/incoming'))
    app = KikBot(kik, __name__)
    app.run(port=8080, host='127.0.0.1', debug=True)







