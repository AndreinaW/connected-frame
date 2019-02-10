#!/usr/bin/python
import json

class JsonHandler:

	def __init__(self, filename):
		self.filename = filename

	def get_data_from_file(self, keyword):
		all = self.read_json_from_file()

		res = {}
		res[keyword] = all[keyword]

		return str.encode(json.dumps(res))

	def read_json_from_file(self):
		with open(self.filename) as file:
			return json.load(file)

	def write_json_to_file(self, json_object):
		with open(self.filename, 'w') as file:
			file.write(json.dumps(json_object))

	def calculate_average_age(self, json_content, new_entry_age):
		total = json_content["totalFaces"]
		current = json_content["currentAverageAge"]

		return (current * total + new_entry_age)/(total + 1)

	def calculate_parity(self, json_content, gender):
		if gender == "female":
			json_content["parity"]["woman"] += 1
		else:
			json_content["parity"]["man"] += 1

	def calculate_emotions(self, json_content, emotion_data):
		current_most_percentage = -1
		most_possible = ""

		for emotion in emotion_data:
			if(emotion_data[emotion] > current_most_percentage):
				current_most_percentage = emotion_data[emotion]
				most_possible = emotion

		json_content["expressions"][most_possible] += 1

	def process_data_from_json(self, post_data):
		json_content = self.read_json_from_file()
		json_data = json.loads(post_data)

		for entry in json_data:
			json_content["currentAverageAge"] = self.calculate_average_age(json_content, entry["faceAttributes"]["age"])

			self.calculate_parity(json_content, entry["faceAttributes"]["gender"])

			self.calculate_emotions(json_content, entry["faceAttributes"]["emotion"])

			json_content["totalFaces"] += 1

		self.write_json_to_file(json_content)