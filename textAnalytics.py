# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib2
import urllib
import sys
import base64
import json

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = 'aa799359c05d43b3bfdd6e68ed47d7da'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
            
input_texts = '{"documents":[{"id":"1","text":"Mitochondria is the powerhouse of the cell. Chemistry is the study of matter"},{"id":"2","text":"Chemistry is the study of matter"},{"id":"three","text":"hello my world"},]}'

num_detect_langs = 1;

# Detect key phrases.
batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
req = urllib2.Request(batch_keyphrase_url, input_texts, headers) 
response = urllib2.urlopen(req)
result = response.read()
obj = json.loads(result)
for keyphrase_analysis in obj['documents']:
    print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))
