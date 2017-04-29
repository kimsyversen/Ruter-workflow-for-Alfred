# encoding: utf-8
import json

class Config(object):
	def get_route(self, route):
		return self.config["routes"][route]

	def get_routes(self):
		return self.config["routes"]

	def get(self):
		return self.config

	def get_last_requested_route(self):
		return self.config["last_requested_route"]

	def set_last_requested_route(self, value):
		self.config["last_requested_route"] = value

	def check_if_route_exists(self, route_name):
		for route in self.get_routes():
			if name in route:
				return True

	def set(self, key, value):
		self.config[key] = value
		self.save()

	def load(self):
		with open('config.json', 'r') as f:
			return json.load(f)

	def save(self):
		with open('config.json', 'w') as f:
			json.dump(self.config, f, sort_keys=True, indent=4)

	def add(self, parent, child, start_id, stop_id):
		self.config[parent][child] = { "from_stop_id" : start_id, "to_stop_id" : stop_id }

	def delete(self, parent, child):
		self.config[parent].pop(child)
		self.save()

	def __init__(self):
		self.config = self.load()
