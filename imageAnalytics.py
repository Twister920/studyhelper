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
























'''
#Accesses the API and retreives a string from the image
def ocr_space_image(image, api_key='45fff96fe888957', language='eng'):
				payload = {'isOverlayRequired': False,
															'apikey': api_key,
															'language': language,
															}

				r = requests.post('https://api.ocr.space/parse/image',
																						files={"image file": image},
																						data=payload,
																						)

				return r.json()

#Reads text from an image, given filename
def get_text_from_file(filename):
				with open(filename, 'rb') as image:
						return get_text_from_image(image)

#Reads text from an image, given the opened image file
def get_text_from_image(image):
		return get_sentences(((ocr_space_image(image))["ParsedResults"][0]['ParsedText']))


'''