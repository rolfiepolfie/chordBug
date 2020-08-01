# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 07:20:29 2020

@author: Rolf Eilert Johansen
"""
from mido import Message

class ControlId: 
    readexternalMidiMessage =1000
    chordDetectOnOFF=1001

class ChordId:
    major = [0,4,7]
    minor = [0,3,7]
    major7 = [-2,0,4,7]
    minor7 = [-2,0,3,7]
    sus2 = [0,2,7]
    sus4 = [0,4,7]

class EventType:
    chord = 100
    control =101
    other =102
    
   
def dummyMidiMessage(note):
    return  Message('note_on', channel=1, note=note, velocity=60, time=0)   
    
    
class Service:
    def __init__(self, eventType, ID, midimsg):
        
        self._eventType=eventType
        self._Chord_control_ID=ID
        self._midimsg=midimsg
        
        
    def print(self):
        print(self._eventType)
        print(self._Chord_control_ID)
        print(self._midimsg)
      
    
    def compMidi(self, midiMsg):
        return self._midimsg.note == midiMsg.note
        
        
def callbackService(Service):
    print('got midi note "{}" , ID: {}'.format(Service._midimsg.note, Service._Chord_control_ID))
    


class Publisher:
    def __init__(self):
        self.supportedEvents=[EventType.chord, EventType.control] 
        self._events = {event : dict() for event in self.supportedEvents}
    
 
    def get_Services(self, event):
        return self._events[event]
    
    def register(self, service):
        
        event=service._eventType
#        if (type(event) is EventType): #not working, I want to force the use of EventType class ...
#            print("correct")
            
        self.get_Services(event)[service] = callbackService
    
    def clear():
        # use copy of a dict to avoid runtime error https://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
        pass
    
    def clear2(self):
        self._events.clear()
        self._events = {event : dict() for event in self.supportedEvents}
    
    def unregister_subscriber(self, service): #ok
        if len(self._events)==0:
            print("array empty, no deletion possible!")
            return
        try:    
            del self.get_Services(service._eventType)[service]
        except KeyError:
            print("KeyError, no deletion possible!")
            return None
        
#    def unregister_event_subscriber(self, event, subscriber):
#        del self.get_subscribers(event)[subscriber]
                  
    
    def notifybyMidi(self, midiMsg): #we must send the midimess to all subscribers 
        for event in self._events:
            for service, cb in self.get_Services(event).items():
                if service.compMidi(midiMsg):
                    cb(service) 
                    break
                
    def print(self):
        for event in self._events:
            for Service, callback in self.get_Services(event).items():
                Service.print()
                
                
#the only unique is the midi-message ?
    

pub = Publisher()

midi1=dummyMidiMessage(50)
midi2=dummyMidiMessage(51)
midi3=dummyMidiMessage(52)
midi4=dummyMidiMessage(54)


s1=Service(EventType.chord, ChordId.major,                   midi1)
s2=Service(EventType.chord, ChordId.minor,                   midi2)
s3=Service(EventType.control, ControlId.chordDetectOnOFF ,   midi3)

pub.register(s1)
pub.register(s2)
pub.register(s3)

pub.print()

pub.clear2()

pub.register(s1)
pub.register(s2)
pub.register(s3)

pub.print()
# -register
# 1. press controller
# 2. recieve and make an class: Record(EventType, Chord_controltype, midimessage)
# 3. register Record to Publisher

# - chain 
# 1. pedal press 
# 2. send Midi to service 
# 3. service update global value in callback
# 4. playchord_control(global_values) 



# -test- send a midimsg , get back the correct subscriber 

#nb! in reality, we only recieve a midiMsg from controller

#
pub.notifybyMidi(midi1)
pub.notifybyMidi(midi2)
pub.notifybyMidi(midi3)
pub.notifybyMidi(midi4)
#
#
#
#print("- delete s2... -")
##pub.unregister_subscriber(s1)
#    
pub.unregister_subscriber(s2)    
#
##only one event <-> subscriber
#
#pub.notifybyMidi(midi1)
#pub.notifybyMidi(midi2)
#pub.notifybyMidi(midi3)





