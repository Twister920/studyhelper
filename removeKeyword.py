def RemoveKeyword(sentence, keyword, index = 0):
	sentence.replace(keyword[index], "_____")
	return sentence, keyword[index]