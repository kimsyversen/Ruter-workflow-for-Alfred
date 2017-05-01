# encoding: utf-8
from Route import Route
from workflow import Workflow, ICON_WEB, web
import datetime

class RouteParser(object):
  def __init__(self, from_place_id, to_place_id):
    self.from_place_id = from_place_id
    self.to_place_id = to_place_id

    self.base_url = "http://reisapi.ruter.no/"
    self.from_place_name = self.get_stop_name(self.base_url, self.from_place_id)
    self.to_place_name = self.get_stop_name(self.base_url, self.to_place_id)
    self.routes = []
    self.current_time = self.get_current_time()

    self.from_place_district = self.get_district(self.base_url, self.from_place_id)
    self.to_place_district = self.get_district(self.base_url, self.to_place_id)
    
  def get_routes(self):
    self.request = self.send_request()
    self.routes = self.parse_request()
    return self.routes

  #Initiate request
  def send_request(self):
    """
    Todo: It exist at least three types of URLs. Two of them does not work. The API does not return any data.

    Does not work:
    https://ruter.no/reiseplanlegger/Mellom/Fra/(30117566)Toftes%20gate%202%20(Oslo)/til/(1000020910)Grunerl%C3%B8kka%20(omr%C3%A5de)%20(Oslo)/etter/#st:0,sp:0,bp:0
    https://ruter.no/reiseplanlegger/Mellom/Fra/(598455%2c6644943)Min%20posisjon/til/(3012507)Thune%20(Oslo)/etter/300420172305/#st:0,sp:0,bp:0
    

    Does work:
    
    """
    url = self.base_url + "Travel/GetTravels?fromPlace={0}&toPlace={1}&isafter=true&time={2}".format(self.from_place_id,self.to_place_id,self.current_time)
  
    params = dict(count=20, format='json')
    response = web.get(url, params)

    #Show an error to the user if anything goes wrong
    response.raise_for_status()

    return response.json()

  def check_for_deviation(self, stages):
  	# If stage contain Deviation and contain more than [], then it is actually a deviation
		for stage in stages:
			if "Deviations" in stage and len(stage["Deviations"]):
				return True
			break

		return False

  def create_line_description(self, stages):
		
		# The first result in Stages will contain "LineNumber" unless you have to walk. A line can be bus, tram, metro or possibly train
		# Todo: Ideally it should not be like this. #Codebetter
		if "LineName" not in stages[0]:
			if "WalkingTime" in stages[0]:
				walking_time = stages[0]["WalkingTime"]
			else:
				walking_time = "x"

			if "LineName" in stages[1]:
				return "Walk %s minutes to line %s " % (walking_time, stages[1]["LineName"])
			return "walk"
		
		return "Take line %s" % (stages[0]["LineName"])

  def parse_request(self):
    travelproposals = self.request['TravelProposals']

    for tp in travelproposals:
      requires_change = False
      number_of_changes_required = 0
      deviations = False

      depTime = datetime.datetime.strptime(tp['DepartureTime'], "%Y-%m-%dT%H:%M:%S")
      arrTime = datetime.datetime.strptime(tp['ArrivalTime'], "%Y-%m-%dT%H:%M:%S")
      travTime = datetime.datetime.strptime(tp['TotalTravelTime'], "%H:%M:%S")

      number_of_changes_required = len(tp['Stages']) - 1

      # Get the first line. This assumes the API returns the tram/bus/metro you should take as the first result
      line = self.create_line_description(tp['Stages'])

      #Check for deviations 
      deviations = self.check_for_deviation(tp['Stages'])

      route = Route(
        self.from_place_id, 
        self.to_place_id, 
        self.from_place_name, 
        self.to_place_name, 
        arrTime.strftime("%H:%M"), 
        depTime.strftime("%H:%M"), 
        travTime.strftime("%H:%M"), 
        line,
        number_of_changes_required, 
        self.current_time, 
        self.to_place_district, 
        self.from_place_district,
        deviations)

      self.routes.append(route)
      
    return self.routes

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