# encoding: utf-8
class Route(object):
    def __init__(self, from_place_id, to_place_id, from_place_name, 
    to_place_name, arrival_time, departure_time, travel_time, line, 
    number_of_changes_required, current_time, from_place_district,to_place_district,
    deviations):
        self.from_place_id = from_place_id
        self.to_place_id = to_place_id
        self.from_place_name = from_place_name
        self.to_place_name = to_place_name
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.travel_time = travel_time
        self.line = line
        self.number_of_changes_required = number_of_changes_required
        self.current_time = current_time
        self.from_place_district = from_place_district
        self.to_place_district = to_place_district
        self.deviations = deviations

    def is_bad(self):
        if self.deviations or self.number_of_changes_required >= 1:
            return True
        return False

    def is_horrible(self):
        if self.deviations and self.number_of_changes_required >= 1:
            return True
        return False