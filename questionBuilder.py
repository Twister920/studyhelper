import textAnalytics
import imageAnalytics
import noteAnalytics
import random
import sys
import string
from kik.messages import TextMessage, SuggestedResponseKeyboard, TextResponse

TRUE_FALSE = 0
FILL_BLANK = 1
MULTIPLE_CHOICE = 2

# Parent class of all question types
class Question:

	def __init__(self, statement):
		self.create_question_from_statements(statement)

	# Returns False if unsuccessful
	def create_question_from_statements(self, statement):
		return False

	def ask_question(self, bot):
		bot.send_message(self.question)

	# Not sure how to make abstract functions in python
	def check_answer(self, user_answer):
		return None



class QuestionTrueFalse(Question):

	def __init__(self, statement):
		Question.__init__(self, statement)

	# Returns False if unsuccessful
	def create_question_from_statements(self, statement):
		action_verbs = ["is", "was", "are", "were", "will", "can", "should"]
		self.answer = True

		# Randomly chooses if answer to question is "True" or "False"
		is_true = random.randint(0, 1)

		if not is_true:
			self.question = make_statement_false(statement)
			if self.question != None:
				self.answer = False
		
		# If creating a statement with a false answer was unsuccessful, also create a true one
		if is_true or self.answer == True:
			self.question = statement
			self.answer = True

		return True

	def ask_question(self, bot):
		bot.send_message_with_responses(self.question, ["True", "False"])

	def check_answer(self, user_answer):
		user_answer = user_answer.lower().strip()

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



class QuestionFillBlank(Question):

	def __init__(self, statement):
		Question.__init__(self, statement)

	def create_question_from_statements(self, statement):
		key_words = textAnalytics.get_key_phrases(statement)

		if key_words == []:
			return False

		key_word_index = random.randint(0, len(key_words) - 1)
		key_word = key_words[key_word_index]

		self.question = statement.replace(key_word, "________")
		self.answer = key_word

		return True

	def ask_question(self, bot):
		bot.send_message(self.question)

	def check_answer(self, user_answer):
		user_answer = user_answer.lower().strip()
		return user_answer == self.answer.lower().strip()



class QuestionMultipleChoice(Question):

	def __init__(self, statement):
		Question.__init__(self, statement)

	# Tries to make a multiple choice question of at least 2 choices from inputted statements
	def create_question_from_statements(self, statements):
		minimum_responses = 2

		false_statements = []
		true_statement = None

		for i in range(len(statements)):
			if i == len(statements) - 1:
				true_statement = statements[i]
			else:
				false_statement = make_statement_false(statements[i])
				if false_statement != None:
					false_statements.append(false_statement)
				else:
					if true_statement == None:
						true_statement = statements[i]
					else:
						if i < minimum_responses:
							return False
						else:
							break

		self.number_of_responses = len(false_statements) + 1
		answer_index = random.randint(0, len(false_statements))
		
		question_and_responses = "Which of the following is true?"

		j = 0
		for i in range(self.number_of_responses):
			question_and_responses += "\n" + string.uppercase[i] + ". "
			if i == answer_index:
				question_and_responses += true_statement
			else:
				question_and_responses += false_statements[j]
				j += 1

		self.question = question_and_responses
		self.answer = string.uppercase[answer_index]

		return True

	def ask_question(self, bot):
		# Responses are first capital letters - corresponding to number of responses
		responses = list(string.uppercase[:self.number_of_responses])

		bot.send_message_with_responses(self.question, responses)

	def check_answer(self, user_answer):
		user_answer = user_answer.lower().strip()
		return user_answer == self.answer.lower().strip()



# Returns None if failed
def make_statement_false(statement):
	action_verbs = ["is", "was", "are", "were", "will", "can", "should"]
	answer = True

	if "not" in statement:
		question = statement.replace("not ", "")
		answer = False
	else:
		for action_verb in action_verbs:
			if action_verb in statement:
				question = statement.replace(action_verb, action_verb + " not")
				answer = False

				break

	return question if (answer == False) else None



class QuizCreator:

	def __init__(self):
		# The number of each type of question created
		self.question_types = { TRUE_FALSE : 0,
								FILL_BLANK : 0,
								MULTIPLE_CHOICE : 0
		}

		self.sorted_notes = {}
		self.questions = []
		self.question_index = -1

	# TODO: introduce an element of randomness
	def create_questions(self):
		question = None

		for statement in self.sorted_notes["Sentences"]:
			# To make an equal balance of questions, find the least asked type of question
			least_asked_question = min(self.question_types.items(), key=lambda x: x[1])[0]

			'''if least_asked_question == FILL_BLANK:
				question = QuestionFillBlank(statement)
				self.question_types[FILL_BLANK] += 1

			if least_asked_question == TRUE_FALSE or question == None:
				question = QuestionTrueFalse(statement)
				self.question_types[TRUE_FALSE] += 1'''

			if least_asked_question == MULTIPLE_CHOICE or question == None:
				current_index = self.sorted_notes["Sentences"].index(statement)
				question = QuestionMultipleChoice(self.sorted_notes["Sentences"][current_index:current_index+4])
				self.question_types[MULTIPLE_CHOICE] += 1

			if question == None:
				continue

			self.questions.append(question)
			question = None

	# Checks user's answer
	def check_answer(self, bot, user_answer):
		if self.question_index == -1:
			print "No questions to check answer!"
			sys.exit(0)

		print self.question_index

		question = self.questions[self.question_index]

		if question.check_answer(user_answer):
			bot.send_message("That's correct! Good work!")
		else:
			bot.send_message("Oh no that's wrong, the correct answer was: " + str(question.answer) + ".")



	def is_empty(self):
		return self.sorted_notes == {}

	def reset(self):
		self.sorted_notes = {}
		self.questions = []
		self.question_index = -1

	def add_notes_from_picture(self, url):
		notes = imageAnalytics.get_text_from_url(url)
		sorted_notes = noteAnalytics.get_json_from_notes(notes)

		self.sorted_notes = dict(self.sorted_notes, **sorted_notes)

		self.regenerate_questions()

	def replace_notes_from_picture(self, url):
		notes = imageAnalytics.get_text_from_url(url)
		sorted_notes = noteAnalytics.get_json_from_notes(notes)

		self.sorted_notes = sorted_notes

		self.regenerate_questions()

	# Gets the next question in the array. Returns false if out of bounds
	def ask_next_question(self, bot):
		self.question_index += 1

		if self.question_index == len(self.questions):
			self.question_index = 0
			return False
		else:
			question = self.questions[self.question_index]
			question.ask_question(bot)
			return True

	def regenerate_questions(self):
		self.questions = []
		self.question_index = -1
		self.create_questions()

