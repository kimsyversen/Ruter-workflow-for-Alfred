# encoding: utf-8
import datetime, sys, os
from workflow import Workflow, ICON_WEB, web
from ParseTripData import ParseTripData
from Config import Config

if __name__ == u"__main__":
  wf = Workflow()
 
  config = Config()

  route = config.get_route(wf.args[0])

  route_name = wf.args[0]

  from_stop = route['from_stop_id']
  to_stop = route['to_stop_id']

  t = ParseTripData(from_stop, to_stop)

  previous_selected_route = config.get_last_requested_route()

  # If we search the same route as last time, get the result from cache
  if route_name == previous_selected_route:
    trips = wf.cached_data('trips', t.get_trips, max_age=180) #Todo: Fix cache from config
  else:
    trips = t.get_trips()
    config.set("last_requested_route", route_name)

  #trips = t.get_trips()
  
  for trip in trips:
    if trip.requires_change == True and trip.deviations == True:
      subtitle = "DEVIATION on %s. Requires %s change. Go to URL to read more" % (trip.line, trip.number_of_changes_required)
    elif trip.requires_change == True and trip.deviations == False:
      subtitle = "Take %s. Requires %s change. Go to URL to read more" % (trip.line, trip.number_of_changes_required)
    elif trip.requires_change == False and trip.deviations == True: 
      subtitle = "DEVIATION on %s. Go to URL to read more" % (trip.line)
    else:
      subtitle = "Take %s directly to destination" % (trip.line)

    url= u"https://ruter.no/reiseplanlegger/Mellom/Fra/({0}){1} ({2})/til/({3}){4} ({5})/etter/{6}".format(
      trip.from_place_id, 
      trip.from_place_name, 
      trip.from_place_district, 
      trip.to_place_id, 
      trip.to_place_name,
      trip.to_place_district,
      trip.current_time) 

    title = "%s: %s - %s: %s (%s)" % (trip.from_place_name, trip.departure_time, trip.to_place_name, trip.arrival_time, trip.travel_time)
    
    wf.add_item(title=title, subtitle=subtitle, arg=url, valid=True, icon=ICON_WEB)

  wf.send_feedback()