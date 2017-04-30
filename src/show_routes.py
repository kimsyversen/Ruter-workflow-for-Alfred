# encoding: utf-8
import datetime
import sys
from workflow import Workflow, ICON_WEB, web
from ParseTripData import ParseTripData
from Config import Config

if __name__ == u"__main__":
	wf = Workflow()

	config = Config()
	routes = config.get_route()

	for route in routes:
		title = "Route to %s" % (route) 
		wf.add_item(title=title, subtitle="", valid=True,  arg=route)

	wf.send_feedback()
