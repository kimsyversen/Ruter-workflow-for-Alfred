# encoding: utf-8
from Trip import Trip
from workflow import Workflow, ICON_WEB, web
import datetime

class ParseTripData(object):
  def __init__(self, from_place_id, to_place_id):
    self.from_place_id = from_place_id
    self.to_place_id = to_place_id

    self.base_url = "http://reisapi.ruter.no/"
    self.from_place_name = self.get_stop_name(self.base_url, self.from_place_id)
    self.to_place_name = self.get_stop_name(self.base_url, self.to_place_id)
    self.trips = []
    self.current_time = self.get_current_time()

    self.from_place_district = self.get_district(self.base_url, self.from_place_id)
    self.to_place_district = self.get_district(self.base_url, self.to_place_id)
    

  def get_trips(self):
    self.request = self.send_request()

    self.trips = self.parse_request()

    return self.trips
    
  #Initiate request
  def send_request(self):
    url = self.base_url + "Travel/GetTravels?fromPlace={0}&toPlace={1}&isafter=true&time={2}".format(self.from_place_id,self.to_place_id,self.current_time)
  
    params = dict(count=20, format='json')
    response = web.get(url, params)

    #Show an error to the user if anything goes wrong
    response.raise_for_status()
    return response.json()

  def parse_request(self):
    travelproposals = self.request['TravelProposals']

    for tp in travelproposals:
      requires_change = False
      number_of_changes_required = 0
      deviations = False

      depTime = datetime.datetime.strptime(tp['DepartureTime'], "%Y-%m-%dT%H:%M:%S")
      arrTime = datetime.datetime.strptime(tp['ArrivalTime'], "%Y-%m-%dT%H:%M:%S")
      travTime = datetime.datetime.strptime(tp['TotalTravelTime'], "%H:%M:%S")

      number_of_stages = len(tp['Stages']) 
      if number_of_stages > 1:
        requires_change = True
        number_of_changes_required = number_of_stages - 1

      # Get the first line. This assumes the API returns the tram/bus/metro you should take as the first result
      if "LineName" not in tp['Stages'][0]:
        line = "a walk"
      else:
        line = "line %s" % (tp['Stages'][0]["LineName"])
      
      #Check for deviations 
      for stage in tp['Stages']:
        if "Deviations" in stage and len(stage["Deviations"]):
          deviations = True
          break

      trip = Trip(
        self.from_place_id, 
        self.to_place_id, 
        self.from_place_name, 
        self.to_place_name, 
        arrTime.strftime("%H:%M"), 
        depTime.strftime("%H:%M"), 
        travTime.strftime("%H:%M"), 
        line, 
        requires_change, 
        number_of_changes_required, 
        self.current_time, 
        self.to_place_district, 
        self.from_place_district,
        deviations)

      self.trips.append(trip)
      
    return self.trips

  def get_current_time(self):
    return datetime.datetime.now().strftime("%d%m%Y%H%M%S")

  def get_stop_name(self, base_url, id):
    url = base_url +  "Place/GetStop/{0}".format(id)
    response = web.get(url)
    data = response.json()
    return data['Name']

  def get_district(self, base_url, id):
    url = base_url +  "Place/GetPlaces/{0}".format(id)
    response = web.get(url)
    data = response.json()
    return data[0]['District']