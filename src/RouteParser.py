# encoding: utf-8
from Route import Route
from workflow import Workflow, ICON_WEB, web
import datetime

class RouteParser(object):
  def __init__(self, from_place_id, to_place_id):
    self.from_place_id = from_place_id
    self.to_place_id = to_place_id

    self.base_url = "http://reisapi.ruter.no/"
    self.from_place_name = ""
    self.to_place_name = ""
    self.routes = []
    self.current_time = self.get_current_time()

    self.from_place_district = "" 
    self.to_place_district = "" 
    
  def get_routes(self):
    self.request = self.send_request()
    self.routes = self.parse_request()
    return self.routes

  #Initiate request
  def send_request(self):
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

      depTime = datetime.datetime.strptime(tp['DepartureTime'][0:19], "%Y-%m-%dT%H:%M:%S")
      arrTime = datetime.datetime.strptime(tp['ArrivalTime'][0:19], "%Y-%m-%dT%H:%M:%S")
      travTime = datetime.datetime.strptime(tp['TotalTravelTime'][0:19], "%H:%M:%S")

      stages = tp['Stages']

      #Decide name and district for start and destination. 
      #If DepartureStop is present, ArrivalStop is also present. If none of these are present, the stage is a walk
      #Do not want to show "walk" as destination since it's good to know where to go off

      last_stage = len(tp['Stages']) - 1
      if "DepartureStop" in stages[0]: #DepartureStop is in stages[0]
        self.from_place_name =  tp['Stages'][0]["DepartureStop"]["Name"]
        self.from_place_district = tp['Stages'][0]["DepartureStop"]["District"]

        if "ArrivalStop" in stages[last_stage]:
          self.to_place_name = tp['Stages'][last_stage]["ArrivalStop"]["Name"]
          self.to_place_district = tp['Stages'][last_stage]["ArrivalStop"]["District"]
        elif "ArrivalStop" in stages[last_stage -1]:
          self.to_place_name = tp['Stages'][last_stage -1 ]["ArrivalStop"]["Name"]
          self.to_place_district = tp['Stages'][last_stage -1 ]["ArrivalStop"]["District"]
        else:
          self.to_place_name = "Bug1"
          self.to_place_district = "Bug1"
          self.from_place_name =  "Bug1"
          self.from_place_district = "Bug1"
      else: #DepartureStop has to be in stages[1]:
        self.from_place_name =  tp['Stages'][1]["DepartureStop"]["Name"]
        self.from_place_district = tp['Stages'][1]["DepartureStop"]["District"]

        if "ArrivalStop" in stages[last_stage]:
          self.to_place_name = tp['Stages'][last_stage]["ArrivalStop"]["Name"]
          self.to_place_district = tp['Stages'][last_stage]["ArrivalStop"]["District"]
        elif "ArrivalStop" in stages[last_stage -1]:
          self.to_place_name = tp['Stages'][last_stage -1 ]["ArrivalStop"]["Name"]
          self.to_place_district = tp['Stages'][last_stage -1 ]["ArrivalStop"]["District"]
        else:
          self.to_place_name = "Bug2"
          self.to_place_district = "Bug2"
          self.from_place_name =  "Bug2"
          self.from_place_district = "Bug2"


      number_of_changes_required = last_stage

      line = self.create_line_description(tp['Stages'])

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