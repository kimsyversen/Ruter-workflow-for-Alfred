# encoding: utf-8
import datetime, sys, os
from workflow import Workflow, ICON_WEB, web
from Config import Config

if __name__ == u"__main__":
	wf = Workflow()

	c = Config()

	routes = c.get_routes()

	route_name = os.getenv('env_route_name')
	
	c.delete("routes",route_name)