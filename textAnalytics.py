# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib2
import urllib
import sys
import base64
import json

#Gets key phrases from a document
def get_key_phrases(string):
	# Azure portal URL.
	base_url = 'https://westus.api.cognitive.microsoft.com/'
	# Your account key goes here.
	account_key = 'aa799359c05d43b3bfdd6e68ed47d7da'

	headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

	input_texts = '{"documents":[{"id":"1","text":"' + string + '"}]}'

	num_detect_langs = 1;

	# Detect key phrases.
	batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
	req = urllib2.Request(batch_keyphrase_url, input_texts, headers) 
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)

	return obj['documents'][0]['keyPhrases']