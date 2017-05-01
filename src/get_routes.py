# encoding: utf-8
import datetime, sys, os
from workflow import Workflow, ICON_WEB, web
from RouteParser import RouteParser
from Config import Config

if __name__ == u"__main__":
  wf = Workflow()
 
  config = Config()

  route_name = wf.decode(wf.args[0])
 
  route = config.get_route(route_name)

  raw_data = RouteParser(route['from_stop_id'], route['to_stop_id'])

  for route in raw_data.get_routes():
    #Line is actually a string that is created in RouteParser
    subtitle = "%s. " % (route.line) 

    if route.deviations == True:
      subtitle += "Deviations on route. "

    if route.number_of_changes_required >= 1:
      subtitle += "Requires changes. " 

    if route.number_of_changes_required >= 1 or route.deviations == True:
      subtitle += "Hit enter to read more on Ruter's website. "

    url= u"https://ruter.no/reiseplanlegger/Mellom/Fra/({0}){1} ({2})/til/({3}){4} ({5})/etter/{6}".format(
      route.from_place_id, 
      route.from_place_name, 
      route.from_place_district, 
      route.to_place_id, 
      route.to_place_name,
      route.to_place_district,
      route.current_time) 

    #Add emoticons and assume it's a good route
    icon = "thumbsup.png"

    if route.is_bad():
      icon="neutralface.png"

    if route.is_horrible():
      icon="angryface.png"

    title = "%s: %s - %s: %s (%s)" % (route.from_place_name, route.departure_time, route.to_place_name, route.arrival_time, route.travel_time)
    
    wf.add_item(title=title, subtitle=subtitle, arg=url, valid=True, icon=icon)

  wf.send_feedback()