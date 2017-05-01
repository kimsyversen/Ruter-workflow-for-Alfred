# encoding: utf-8
from __future__ import unicode_literals, print_function
import datetime, sys, os

from workflow import Workflow, ICON_WEB, web
from Config import Config


def find_route_id(string, start_pattern, end_pattern):
	start_index = string.find(start_pattern) + len(start_pattern)

	end_index = string.find(end_pattern, start_index)

	return string[start_index:end_index]

if __name__ == u"__main__":
	wf = Workflow()
	log = wf.logger


	c = Config()

	routes = c.get_route()

	#route_name = os.getenv('env_route_name')
	#route_name = route_name.encode("utf-8")
	route_name = wf.decode(os.getenv('env_route_name'))

	log.debug("Created the route %s" % (route_name))

	url = os.getenv('env_url')

	start_id = find_route_id(url, "Fra/(", ")")
	stop_id = find_route_id(url, "til/(", ")")

	data = { "from_stop_id" : start_id, "to_stop_id" : stop_id }

	c.add("routes", route_name, data)