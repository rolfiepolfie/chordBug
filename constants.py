# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 07:08:25 2020

@author: rrr
"""


#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
class MidimsgID:
    note_on = 'note_on'
    note_off = 'note_off' 
    sysex = 'sysex'
    controlchange = 'control_change'
    pitchwheel = 'pitchwheel'
    program_change = 'program_change'
    afterTouch = 'aftertouch'
    pitchwheel = 'pitchwheel'
    
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------   
class ControlId: #UsercontrolmsgID: data bytes must be 0..127
    panic =1000 #send note off to all channels 
    chordDetectOnOFF=1001
    readExtMidi =1002
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
class ChordId:
    major = [0,4,7]
    minor = [0,3,7]
    major7 = [-2,0,4,7]
    minor7 = [-2,0,3,7]
    sus2 = [0,2,7]
    sus4 = [0,4,7]

#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
class VelocityLevel:
    high=120
    medium =60
    low=30
    default=64
    maximum=127
    zero=0
    
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
class EventType:
    chordEvent = 100
    controlEvent = 101
        
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------    
class Midinotes:
    c3 = 48
    c4 = 60
    c5 = 72

#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
class Allnotes:
    c=1
    c_sharp=2
    d=3
    d_sharp=4
    e=5
    f=6
    f_sharp=7
    g=8
    g_sharp=9
    a=10
    a_sharp=11
    b=12

#https://github.com/mido/mido/issues/54
#make som mesages for testing 
#msg2 = m.Message(c.note_on)
#msg2.copy(note=99)
#
#msg3=m.Message(c.controlchange)
#msg3.copy(control=90)

### improve => fetch values from midi messae register instead of control values
    
#Since the callback runs in a different thread you may need to use locks or 
#other synchronization mechanisms to keep your main program and the callback 
#from stepping on each other’s toes.
#
#Calling receive(), __iter__(), or iter_pending() on a port with a callback 
#will raise an exception:
    

#def sendTestTone(note=60):
#    #make a message 
#    m1=m.Message(c.note_on , note=65, velocity=77)
#    m.ports.set_sleep_time(1)
#    midiOut.send(m1)
#    m.ports.sleep()
    
#    def mido(self):  #rename to midoMessage
#        if self.type == 'note_on':
#            return Mido.Message('note_on', channel=self.channel, note=self.note, velocity=self.note, time=self.time)
#        
#        if self.type == 'note_off':
#            return Mido.Message('note_off', channel=self.channel, note=self.note, velocity=self.note, time=self.time)
#        
#        if self.type == 'control_change':   
#            return Mido.Message('control_change', channel=self.channel, control=self.control, value=self.value, time=self.time)
#        
#    
#        #if .... the rest of all Midi message constructors ....
#        #    mido.new('polytouch', channel=0, note=0, value=0, time=0)
#        #    mido.new('program_change', channel=0, program=0, time=0)
#        #    mido.new('aftertouch', channel=0, value=0, time=0)
#        #    mido.new('pitchwheel', channel=0, value=0, time=0)
#    
#    
#    
##NB! no channel info .......        
#        #    mido.new('sysex', data=(), time=0)
#        #    mido.new('undefined_f1', time=0)
#        #    mido.new('songpos', pos=0, time=0)
#        #    mido.new('song', song=0, time=0)
#        #    mido.new('undefined_f4', time=0)
#        #    mido.new('undefined_f5', time=0)
#        #    mido.new('tune_request', time=0)
#        #    mido.new('sysex_end', time=0)
#        #    mido.new('clock', time=0)
#        #    mido.new('undefined_f9', time=0)
#        #    mido.new('start', time=0)
#        #    mido.new('continue', time=0)
#        #    mido.new('stop', time=0)
#        #    mido.new('undefined_fd', time=0)
#        #    mido.new('active_sensing', time=0)
#        #    mido.new('reset', time=0)
#                
#        
#        else:
#            print("**** Message is not supported: ", self.type)
#            return None      


