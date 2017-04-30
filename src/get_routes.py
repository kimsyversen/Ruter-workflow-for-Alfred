# encoding: utf-8
import datetime, sys, os
from workflow import Workflow, ICON_WEB, web
from ParseTripData import ParseTripData
from Config import Config

if __name__ == u"__main__":
  wf = Workflow()
 
  config = Config()

  route_name = wf.args[0]

  route = config.get_route(route_name)

  t = ParseTripData(route['from_stop_id'], route['to_stop_id'])

  previous_selected_route = config.get("last_requested_route")

  # If user search the same route as last time, get the result from cache
  #cache_time = int(config.get("cache_time"))

  """if route_name == previous_selected_route:
    trips = wf.cached_data('trips', t.get_trips, max_age=cache_time) #Todo vurder om cache funker 
  else:
    trips = t.get_trips()
    config.set("last_requested_route", route_name)"""

  trips = t.get_trips()
  for trip in trips:
    subtitle = ""

    subtitle += " %s. " % (trip.line) 

    if trip.deviations == True:
      subtitle += "Deviation on trip found. "

    if trip.number_of_changes_required >= 1 or trip.deviations == True:
      subtitle += "Requires changes. Hit enter to read more on Ruter's website. " 

    url= u"https://ruter.no/reiseplanlegger/Mellom/Fra/({0}){1} ({2})/til/({3}){4} ({5})/etter/{6}".format(
      trip.from_place_id, 
      trip.from_place_name, 
      trip.from_place_district, 
      trip.to_place_id, 
      trip.to_place_name,
      trip.to_place_district,
      trip.current_time) 

    #Add emoticons and assume no deviation
    thumbs = ""
    
    if trip.deviations or trip.number_of_changes_required >= 1:
      #thumbs = u"\U0001F44E"
      thumbs = u"\U0001F61E"

    title = "%s %s: %s - %s: %s (%s)" % (thumbs, trip.from_place_name, trip.departure_time, trip.to_place_name, trip.arrival_time, trip.travel_time)
    
    wf.add_item(title=title, subtitle=subtitle, arg=url, valid=True)

  wf.send_feedback()