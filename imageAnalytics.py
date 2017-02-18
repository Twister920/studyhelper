import requests

#Reads text from an image, given the opened image file
def get_text_from_url(url):
		return (ocr_space_url(url))["ParsedResults"][0]['ParsedText']



#Accesses the API and retreives a string from the image
def ocr_space_url(url, api_key='45fff96fe888957', language='eng'):
	payload = {'url' : url,
				'isOverlayRequired': False,
				'apikey': api_key,
				'language': language,
				}

	r = requests.post('https://api.ocr.space/parse/image',
					  data=payload,
					  )

	return r.json()