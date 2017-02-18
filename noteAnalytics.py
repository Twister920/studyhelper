import requests
import textAnalytics

def get_json_from_notes(string):
	bullet_characters = ["-", "*"]

	sorted_notes = {}

	note = string.splitlines()

	for line in :
		if line[0] in bullet_characters:
			print line + " - is a bullet."

	return string #string.replace("\n", " ")




sample_notes = {
	"Mitochondria" : 
	{"phrase" : "is the powerhouse of the cell", "keywords" : ["Mitochondria", "powerhouse", "cell"]}
}




