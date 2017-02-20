import requests

def get_json_from_notes(string):
	bullet_characters = ["-", "*"]

	note = string.splitlines()
	is_bullets = False

	bullets = []

	note_organized = {"Sentences" : []}

	#Goes through notes from bottom to top
	for line_index in range(len(note) - 1, -1, -1):
		line = note[line_index]

		if line[0] in bullet_characters:
			is_bullets = True

			#Adds the bullet and its keyword to the list of bullets
			bullets.append(line)

		#If the iterator hits a non-bullet after a list of bullets, assume it is the heading
		elif is_bullets:
			is_bullets = False

			note_organized[line] = bullets

		#Otherwise, it must just be a regular phrase
		else:
			note_organized["Sentences"].append(line)

	return note_organized 


'''sample_notes = {
	"Mitochondria" : 
	["is the powerhouse of the cell", "is still the powerhouse of the cell"]

	"Sentences" :
	[["is the powerhouse of the cell", ["Mitochondria", "powerhouse", "cell"]],
	["is still the powerhouse of the cell", ["Mitochondria", "still", "cell"]]]]
}'''




