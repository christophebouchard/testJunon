#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import random

import requests
import datetime as dt
import time
import logging
logging.basicConfig(filename='/tmp/jingo.log', level=logging.DEBUG)
logging.debug('start debug')

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 
    Refer to the documentation for further details. 
    """ 
    #city = intentMessage.slots.position.first().value
    city = 'Bangalore'
    print city
    logging.debug(city)
    
    #headers = {'accept': 'application/json', 'authorization': 'Basic anVub246UlFXSnVub25YcG0yWA=='}
    #response = requests.get('https://junon---develop-sr3snxi-ma2sa5nwhuqdk.fr-1.platformsh.site/v1/status', auth=('junon', 'RQWJunonXpm2X'))
    #data = res.json()
    #aqi = data['breezometer_aqi']
    aqi = 90
    
    quality_word = 'mauvaise'
    if aqi >= 80:
        quality_word = 'bonne'
    elif aqi >= 60:
        quality_word = 'moyenne'
    
    result_sentence = 'Aujourd\'hui la qualité de l\'air à {} est {}'.format(city, quality_word)

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("testJunon:getPosition", subscribe_intent_callback) \
.start()
