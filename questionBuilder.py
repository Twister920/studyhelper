import textAnalytics
import random
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
			if "not" in statement:
				self.question = statement.replace("not ", "")
				self.answer = False
			else:
				for action_verb in action_verbs:
					if action_verb in statement:
						self.question = statement.replace(action_verb, action_verb + " not")
						self.answer = False

						break
		
		# If creating a statement with a false answer was unsuccessful, also create a true one
		if is_true or self.answer == True:
			self.question = statement
			self.answer = True

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

	def ask_question(self, bot):
		bot.send_message_with_responses(self.question, ["True", "False"])

	def check_answer(self, user_answer):
		user_answer = user_answer.lower().strip()
		return user_answer == self.answer.lower().strip()



class QuestionMultipleChoice(Question):

	def __init__(self, statement):
		Question.__init__(self, statement)

	def ask_question(self, bot):
		bot.send_message_with_responses(self.question, ["True", "False"])

	def check_answer(self, user_answer):
		user_answer = user_answer.lower().strip()
		return user_answer == self.answer.lower().strip()







class QuestionBuilder:

	def __init__(self):
		# The number of each type of question created
		self.question_types = { TRUE_FALSE : 0,
						   		FILL_BLANK : 0,
						   		MULTIPLE_CHOICE : 0
		}

	def create_questions(self, sorted_notes):
		questions = []
		question = None

		for statement in sorted_notes["Sentences"]:
			# To make an equal balance of questions, find the least asked type of question
			least_asked_question = min(self.question_types.items(), key=lambda x: x[1])[0]

			if least_asked_question == FILL_BLANK:
				question = QuestionFillBlank(statement)
				self.question_types[FILL_BLANK] += 1

			if least_asked_question == TRUE_FALSE or question == None:
				question = QuestionTrueFalse(statement)
				self.question_types[TRUE_FALSE] += 1

			#if least_asked_question == MULTIPLE_CHOICE or question == None:
			#	question = QuestionMultipleChoice(statement)
			#	self.question_types[MULTIPLE_CHOICE] += 1

			if question == None:
				continue

			questions.append(question)
			question = None

		return questions