# -*- coding: utf-8 -*-

"""" sourecs 
https://www.programcreek.com/python/index/7371/mido
https://stackoverflow.com/questions/42975735/nameerror-trying-to-use-get-output-names-from-mido
pip install python-rtmidi
to use ports:   pip install python-rtmidi

RtMidi = recommended backend
PortMidi = old backend
"""

import mido as Mido #remove and import the classes you need
import rtmidi as rt
import sys
#from constants import ChordId
from classes import Globals, EventType, MidiMess
from classes import MidiDevice, Session
from constants import MidimsgID
import binascii  
from text import * 
#from tkinter import filedialog

dev_global = None

glob = Globals()


def startReport():
    print("-----------------------------------------------------------------")
    print("Python installed: \t", sys.version_info[0], sys.version_info[1])
    print("Mido version:   \t", Mido.__version__)
    print("Backend version:\t", rt.__version__)
    print("Available midi in dev:\t", Mido.get_input_names())
    print("Available midi out dev:\t", Mido.get_output_names())

def developerReport(): print(report)

#callback used only for register new events in sessions
def callbackRegisterNewEvents(msg): 
    Globals.globalMidimessage=msg                       #<-------- hopfully a valid class variable !!! NBNBNBNBNBNB 
    print("- callbackRegisterNewEvents -", msg)
    

# the service will trigger controller messages as notes or cc
# controller messages|tones cannot  be on the same performance midi-channel as     
# controller messages|cc    can     be ....
#got problem with mido.velocity = nontype, so used msg instead 
def callbackMido(msg): 
    global s
    global glob
    Globals.globalMidimessage=msg #needed?
    mido=MidiMess(msg)
    
    isNote = msg.type == MidimsgID.note_on or msg.type == MidimsgID.note_off
    isControl = msg.type == 'control_change'
    
    
    if isNote and msg.channel==glob.bassChannel:  #update root note in Global only bass channel  
        
        
        #implement as filter_remove_notes_velocity ....
        if msg.velocity==0: 
            pass
            #print("velocity in is zero - reject incomming midi message")
          
        else:
            #service_global.send(mido) #engage SERVICE's callbackservice
            Globals._rootnote=mido.note  #update rootnote
            print("root note: ", Globals._rootnote)
        



    if isNote:
        if msg.channel==glob.detectionChannel and msg.velocity > 0:   #runned if fcb1010 is used "we use notes only"
            #filter out velocity = 0 ....
            #print("s.send(mido)")
            s.notifybyMidi(msg) #send to Service , callbackservice fills globals 
        
            #using those globals to to play a chord 
            s.playChord(Globals._chordId, Globals._rootnote, Globals._eventType)

            s.engangeControl(Globals._controlId, Globals._eventType)
        

        if msg.channel==glob.detectionChannel and msg.velocity == 0: #special for bug in fcb1010
            pass
            #print("pedal up event! ")
 
    
    if isControl:
        pass
                            
#engaged from Service.send() function, do not use this as a callback other than Service class
 # this callback shal only update the Global registry only            
# -----------------------------------------------------
# callbackService 
# -----------------------------------------------------     play chords from here instead ,try it out ?

# reference to the businessprocessing object = business 
def callbackService(eventClient, business): #midomess is "MidiMess" and from callbackLearn
     
    eventType = eventClient.eventType #type event chord, control or other    
    chordID = eventClient.chordControlId #the chord 
    mido = eventClient.midoMess #midi message
    
    # update chordID
    if mido.isNote(): #only notes are stored anyway .... check the type midimessage in the service and act from there 
      #print("callbackService-  if eventClient.midoMess.isNote():")  
      
      
      if eventType == EventType.chordEvent: #chordEvent
         print("- chord change - update ", eventType)
         # change cord in globals 
             #here
         Globals._chordId =   chordID  
         Globals._eventType = eventType
         print("global chordID: ", Globals._eventType)
      
        
      if eventType == EventType.controlEvent:
          print("- control change - update ", eventType)
          Globals._eventType = eventType
          Globals._controlId = chordID
          
        

    
def sendSysex():

    #print(recievesysEx_fcb1010)
    path = Globals.filepath + "setup1.syx"
    sysex=Mido.read_syx_file(path)
    
    ## needed?
    ##msg = Mido.Message('sysex', data=sysex) 

    #out=mido.open_output('name')
    #out.send(sysex)
    #out.close
    # use with ... for a better solution . see manual
    

    #convert to HEX for viewing .....
    with open(path, 'rb') as f:
        hex1=binascii.hexlify(f.read()).decode('utf-8')   
    print(str(hex1).upper())
    
    
    #--------------------------
    
    print("Do you want to send? (y/n)")
    while True:
        data = input("answer y or n:  ")
        if data.lower() not in ('y', 'n'):
            print("Not an appropriate choice.")
        else:
            if(data == "y"):
                print("sending data ......")
                break
            else:
                break
    
    print("aborting!!!")    


import os
#make a filepath if it not exist
def makefilePath(path):

    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# ----------------------------------------------------------------------------
#   main()
# ----------------------------------------------------------------------------
def main():
    startReport()
    
    glob = Globals()
    glob.load()
    
    #developerReport()
    makefilePath(glob.filepath)
    
    Mido.set_backend('mido.backends.rtmidi')
    
    global dev_global
    global s
  
    dev_global = MidiDevice() 
    s=Session(dev_global, glob)
    
    
    
    choice ='0'
    while choice =='0':
          
        print("================================================")
        print("=                  MENU                        =")
        print("================================================")
        
        print("Detection channel is: ", glob.detectionChannel)
        print("->   1. open midi, load last setup, start process ")
        print("->   2. recording control messages: <---- must be tested")
        print("->   3. load and read globals")
        print("->   4. Send sysex data")
        print("->   5. test")
        print("->   6. exit")
        
        choice = input("Please make a choice: ")
        if choice == "1":
            
            glob.load()
            glob.print()
            
            s.createNew() #constructing new internal objects + open midiports
            s.loadLast(callbackMido, callbackService)
            s.startListening()   
            #session.close() # called by keyb interrupt , but not finished ! NBNB 
            main()
            break      
            choice = '0'    
          
        if choice == "2":
             #first fill in user data in the "glob" object
             glob.load()
             glob.print()
             s.createNew() 
             s.readNewChords(callbackRegisterNewEvents)
             s.close()
             
             choice = '0'    

         
        if choice == "4":
            sendSysex()
            break
        
            choice = '0'    
        
        if choice == "5":
            glob.load()
            s.createNew() #constructing new internal objects + open midiports
            s.playchordTest()
            s.close()
            main()
            break  
            
            choice = '0'
            
            
        if choice == "3":           
                
            glob.load()
            glob.print() 
            
            main()
            break 
        
        
        if choice == "6": #exit
            print("- exiting program-")
            if dev_global is not None:
                dev_global.close()
                
            sys.exit("bye!")   
            
            break
            
              
        
        else: 
            choice = '0'



if __name__ == "__main__":
    main()
            
     



























