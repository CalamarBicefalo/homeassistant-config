import appdaemon.plugins.hass.hassapi as hass

class your_class_name(hass.Hass):

  def initialize(self): 
    self.log("registering callback")
    self.listen_state(self.clean_kitchen,"sensor.desk_bs_pushed")
	
  def clean_kitchen (self, entity, attribute, old, new, kwargs):
    self.log("callback is happening")