# encoding: utf-8
from __future__ import unicode_literals, print_function
import datetime, sys, os
from workflow import Workflow, ICON_WEB, web
from Config import Config

log = None
if __name__ == u"__main__":
	wf = Workflow()
	log = wf.logger

	log.debug("script started")
	c = Config()

	#routes = c.get_route()
	

	# Get route name as selected from the user
	route_name = wf.decode(os.getenv('env_route_name'))

	log.debug("Got route name %s" % (route_name))
	
	
	#Route name is now e.g. Kåk


	#utf8_route_name = unicode(route_name, 'utf-8')




	#log.debug("Created the utf8 route name %s" % (utf8_route_name))

	#log.debug(route_name)

	#log.debug(route_name.encode("utf-8"))

	
	c.delete("routes", route_name)