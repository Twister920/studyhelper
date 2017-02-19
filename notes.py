import imageAnalytics
import noteAnalytics

def get_notes_from_image(url):
	notes = imageAnalytics.get_text_from_url(url)
	sorted_notes = noteAnalytics.get_json_from_notes(notes)

	print sorted_notes