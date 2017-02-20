import textAnalytics
import random
from kik.messages import TextMessage, SuggestedResponseKeyboard, TextResponse

TRUE_FALSE = 0
FILL_BLANK = 1
MULTIPLE_CHOICE = 2


class Question:

	def __init__(self, question_type, question, answer):
		self.type = question_type
		self.question = question
		self.answer = answer

	def ask_question(self, bot):
		if self.type == TRUE_FALSE:
			bot.response_messages.append(TextMessage(
		        to=bot.message.from_user,
		        chat_id=bot.message.chat_id,
		        body=self.question,
		        keyboards=[SuggestedResponseKeyboard(
		        responses=[TextResponse("True"),
		                   TextResponse("False")])]))

		elif self.type == FILL_BLANK:
			bot.send_message(self.question)

	def check_answer(self, user_answer):
		user_answer = user_answer.lower()

		if self.type == TRUE_FALSE:
			positive_answers = ["true", "yes", "t", "y"]
			negative_answers = ["false", "no", "f", "n"]

			# Converts user's input of true or false into boolean value
			if user_answer in positive_answers:
				user_answer = True
			elif user_answer in negative_answers:
				user_answer = False
			else:
				self.send_message("Sorry {}, I didn't get that. Try again?".format(self.user.first_name))
				return None

			return user_answer == self.answer


		elif self.type == FILL_BLANK:
			return user_answer == self.answer




class QuestionBuilder:

	def __init__(self):
		self.question_types = { TRUE_FALSE : 0,
						   		FILL_BLANK : 0
		}

		self.truths = 0
		self.falses = 0

	def create_questions(self, sorted_notes):
		questions = []
		question = None

		for statement in sorted_notes["Sentences"]:
			print statement

			least_asked_question = min(self.question_types.items(), key=lambda x: x[1])[0]

			print ("Questions asked: " + str(self.question_types))
			print ("Least asked type: " + str(least_asked_question))

			if least_asked_question == FILL_BLANK:
				question = self.create_fill_blank_question(statement)
				self.question_types[FILL_BLANK] += 1

			if least_asked_question == TRUE_FALSE or question == None:
				question = self.create_true_false_question(statement)
				self.question_types[TRUE_FALSE] += 1

			if question == None:
				continue

			questions.append(question)

			question = None

		return questions

	# Creates true-false question based on some statement
	def create_true_false_question(self, statement):
		action_verbs = ["is", "was", "are", "were", "will", "can", "should"]

		answer = True

		# Tries to create a true-false question with a false answer if there
		# are fewer of these, to create an equal balance
		if self.truths > self.falses:
			if "not" in statement:
				question = statement.replace("not ", "")
				answer = False

				self.falses += 1
			else:
				for action_verb in action_verbs:
					if action_verb in statement:
						question = statement.replace(action_verb, action_verb + " not")
						answer = False

						self.falses += 1
						break
		
		# If creating a statement with a false answer was unsuccessful, default to 
		# creating a true one.
		if answer == True:
			question = statement
			answer = True

			self.truths += 1

		return Question(TRUE_FALSE, question, answer)



	# Creates fill-in-the-blank question based on some statement
	# Returns None if unsuccessful
	def create_fill_blank_question(self, statement):
		print ("FILL BLANK CREATED")

		key_words = textAnalytics.get_key_phrases(statement)

		if key_words == []:
			return None

		key_word_index = random.randint(0, len(key_words) - 1)
		key_word = key_words[key_word_index]

		question = statement.replace(key_word, "________")
		answer = key_word

		return Question(FILL_BLANK, question, answer)





