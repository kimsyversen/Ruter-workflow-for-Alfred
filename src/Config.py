# encoding: utf-8
import json

class Config(object):
	def get_route(self, route = ""):
		if route == "":
			return self.config["routes"]

		return self.config["routes"][route]

	def get(self, key = ""):
		if key == "":
			return self.config

		return self.config[key]

	def set(self, key, value):
		self.config[key] = value
		self.save()

	def load(self):
		with open('config.json', 'r') as f:
			return json.load(f)

	def save(self):
		with open('config.json', 'w') as f:
			json.dump(self.config, f, sort_keys=True, indent=4)

	def add(self, parent, child, data):
		self.config[parent][child] = data
		self.save()

	def delete(self, parent, child):
		self.config[parent].pop(child)
		self.save()

	def __init__(self):
		self.config = self.load()
