# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 13:31:34 2020

@author: Pro3
"""

########### routine ##########
# init
# key depressed or control
# midoCallback is engaged
# from midocallback we send the key/control to Service
# service is engaging its callback
# ServiceVallback is engaging if chord/control was registered
# 
import sys

from constants import MidimsgID, VelocityLevel, ChordId, ControlId,Midinotes, EventType
from mido import Message, get_output_names, get_input_names, open_input, open_output
from collections import deque
import pickle
import signal
import time
log=True


class Filters:  
    def filter_stopNotesOnly_OndetectionChannel(midiMess, detChannel):
        if midiMess.isNote(): 
            return midiMess.channel != detChannel 
        

def dummyMidiMessage(self, channel):
    return  Message('note_on', channel=channel, note=Midinotes.c3, velocity=VelocityLevel.default, time=0)
   
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------
#store and handler all data needed for performing a session        
class Session:
    def __init__(self, dev, glob):
        self._dev=dev     #place Mididev inside ? 
        self._glob=glob
        
        self._service=None
        self._business=None
 
    def notifybyMidi(self, midomsg): #used in callback to trigger servicecallback
        self._service.notify(midomsg)
        
    def business(self):
        return self._business
         
    def startListening(self):
        self._dev.startListening()      
            
    def createNew(self): # new session, reading new global data as channels ... omit?
             
        self._dev.openMidiAll(self._glob.midiInDevNr, self._glob.midioutDevNr)    #<- new position    
        self._business = BusinessProcessing(self._glob, self._dev.midiOut()) #business needs midiout        
        self._service=Service(self.business()) 
        
        #self._service.clear()?
    
    
    #midomsg are used to update root-note 
    #check chord detect-flag
    #check for empty ChordId's
    
    
         #def playchord(self, chordId, msg, vel):
    def playChord(self, chordID, rootNote, eventType):
        
        if eventType==EventType.chordEvent:
            self._business.playchord(chordID, rootNote, VelocityLevel.default)
        
    
    def engangeControl(self, controlId, eventType):
        
        if EventType.controlEvent == eventType:
        
            if ControlId.chordDetectOnOFF == controlId:
                print("chordDetectOnOFF is detected")
                Globals._control_Detection_toggle ^= True
                print("Toggle flag is: ", Globals._control_Detection_toggle)
    
    def playchordTest(self):
        
        self._business.playchordTest()
        #also info witch channel ....
        
    def panic(self):
       self._dev.panic()
       
        
        
    def updateRootNote(self, mido):
        bus=self._service.getbusiness()
        bus.updateRootNote(mido)
        
    
    def _askUserforChords(self, callback):
        
        # engage the callback to fill the Globals for avoiding an error of nontype
        midi=dummyMidiMessage(self, self._glob.detectionChannel)
        callback(midi)
        
        print("** Chord major, activate control")
        input("Press Enter to continue...\n\n")
        chord1_mido=MidiMess(self._glob.globalMidimessage)  
        print("major chord is detected by: ")
        chord1_mido.printProp()                                   #remove log ....
        
        print("** Chord sus2, activate control")
        input("Press Enter to continue...\n\n")
        chord2_mido=MidiMess(self._glob.globalMidimessage)  
        print("major chord is detected by: ")
        chord2_mido.printProp()           
        
        
        
        print("** Chord major7 , activate control")
        input("Press Enter to continue...\n\n")
        chord3_mido=MidiMess(self._glob.globalMidimessage)
        print("major7 chord is detected by: ")
        chord3_mido.printProp()
        
        print("** Chord minor , activate control")
        input("Press Enter to continue...\n\n")
        chord4_mido=MidiMess(self._glob.globalMidimessage)
        print("major7 chord is detected by: ")
        chord4_mido.printProp()
              
        
        
        
        print("** Control toggleonOff, activate control")
        input("Press Enter to continue...\n\n")
        control1_mido=MidiMess(self._glob.globalMidimessage)
        print("Control toggleonOff is detected by: ")
        control1_mido.printProp()
        
        chord1= EventClient(ChordId.major,                 chord1_mido,    EventType.chordEvent)
        chord2= EventClient(ChordId.sus2,                  chord2_mido,    EventType.chordEvent) 
        
        chord3= EventClient(ChordId.major7,                chord3_mido,    EventType.chordEvent)
        chord4= EventClient(ChordId.minor,                 chord4_mido,    EventType.chordEvent)
        
        control1=EventClient(ControlId.chordDetectOnOFF,    control1_mido,  EventType.controlEvent)  
        

        r1=chord1
        r2=chord2
        r3=chord3
        r4=chord4
        r5=control1
        
        
        return [r1,r2,r3,r4,r5] 
    
    def _setCallback(self, callback):
        self._dev.setCallback(callback) 
       
    
    def readNewChords(self, callback):
        
        self._setCallback(callback)
        
        records=self._askUserforChords(callback) 
        fs=Filesave(self._glob.filepath)
        
        for rec in records:
            fs.addRecord(rec)
    
        print("saving temporarily disabled!!!!!!!!")   
        ##when save() no filename ,  lastsession.dat is used 
        #fs.save() # default lastsession.dat                                   <-engage this NBNBNBNBNBNBNBN
        print("chord session saved to disk as: " , fs.fileWithPath())
       
    

    
    
    def loadLast(self, callback, callbackService): #load using defualt file and register in service
        self._service.clear()     
        self._setCallback(callback)
        
        self._service.setCallbackService(callbackService)
        
        self._service.load(self._glob.filepath)
        self._service.print() 
                
        

    def save(self, filename): # save session to another filename
        pass
    
    def close(self): #close ports, save current sessiondata , etc ...
        self._dev.close()
        
            
        

#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------         
class EventClient:   
    def __init__(self, chordControlId, midoMess, eventType):
        self.chordControlId=chordControlId
        self.midoMess=midoMess        
        self.eventType=eventType
          
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------        
class Globals:
    _chordId=[0, 4, 7] 
    _rootnote=60  
    _chordDetectPedalFlag=False
    _eventType=100  #chord, control , ...
    _controlId=1000
    
    _control_Detection_toggle =True
    
   
    midiOut=None
    midiIn=None
    
    indevname = ""
    outdevname= ""
    
    globalmessage = None #used for the initial learning process       multiple with globalMidimessage? NBNBNNBNB 
    
    detectionChannel=15 #do not "play" on this channel, only for controls 
    bassChannel=2
    pianoChannel=1 #used to read chord 

    filepath="c:\\chordFly\\"
    
    midiInDevNr=1
    midioutDevNr=1
    
    
    filename="globals.dat"
    
    def print(self):
        print("from Class: ", __class__.__name__)
        print("----------------------------------")
        print("detectionChannel: ", self.detectionChannel)
        print("bassChannel: ", self.bassChannel)
        print("pianoChannel: ", self.pianoChannel)
        print("global_filepath: ", self.filepath)
        print("midi in dev nr: ", self.midiInDevNr)
        print("midi in out nr: ", self.midioutDevNr)
        print("----------------------------------")
    
    def save(self):
        filenamepath=self.filepath + self.filename
        
        with open(filenamepath, "wb") as fh: 
            pickle.dump(self, fh, pickle.HIGHEST_PROTOCOL)
        
    
    def load(self):
        data=[]
        filenamepath=self.filepath + self.filename
        
        with open(filenamepath, "rb") as fh:
            data = pickle.load(fh)
        #load back in the class
        self.detectionChannel=data.detectionChannel
        self.bassChannel=data.bassChannel    
        self.pianoChannel=data.pianoChannel
        self.filepath=data.filepath
        print("Global user data restored from last session!")
        
  
#### -----------------------------------------------------
#### class 
####
#### ----------------------------------------------------- 
class BusinessProcessing:

   
   
    def __init__(self, glob, midiout):

        self._glob=glob
        self._oldChord=[]
        self._rootNote=0
        self._midiOut=midiout
        self._activateDetection=False
    
    def executeControl(controlID):
        pass

        
    def activate(self, flag):
        print("Activation of Class:Business is: ", flag )
        self._activateDetection=flag

        
    def invertChordLeft(self, chordId):
        it=deque(self, chordId)
        it.rotate(1)    
        return(list(it)) 
      
    def invertChordRight(chordId):
        it=deque(chordId)
        it.rotate(-1)    
        return(list(it)) 
     
    def detectionChannel(self, dc):
        self._detectionChannel=dc
        
        #change type to id 
    def _chordtomidi(self, chordId, type_, vel):
        
        for notes in chordId:       
            ###### use Midimess instead id Mido Message.......check!  why?
            mido = Message(type_, note=notes+self._rootNote, velocity=vel)
            self._midiOut.send(mido) 
    

            
            
    def playchord(self, chordId, rootNote, vel):
        delOldChord=True
        self._rootNote=rootNote

                
        if delOldChord:#turn off old chord -
            self._chordtomidi(self._oldChord, MidimsgID.note_off, vel)
            #print("deleted chord: ", self._oldChord)
        
        #play new chord
        self._chordtomidi(chordId, MidimsgID.note_on, vel)
        
        print("played chord: ", chordId)
        
        #store the chord
        self._oldChord = chordId
        self._OldrootNote=self._rootNote
        
        
        
    def updateRootNote(self, midomsg):

        #evt reject wrong channel midi
#        if midomsg.channel != self._glob.bassChannel:
#            return 
        
        if midomsg.isNote(): # and midomsg.channel = self.glob.basschannel .... ? stop unwanted messages earlier ....NBNB
            self._rootNote = midomsg.note
            print("current rootNote: ", self._rootNote)
    
    def playchordTest(self):
        port = self._midiOut
        
        notes=[0,4,7,12]
        root=60
       
        for notes in notes:
            mes= Message(MidimsgID.note_on, note=notes+root, velocity=VelocityLevel.default)
            port.send(mes)
            time.sleep(0.3)
        time.sleep(1)    
        #repeat the same notes again with note_off    
          
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------         
class MidiMess:

    def printProp(self):

        print("from Class: ", __class__.__name__)
        if self.isControlChange():
            print("--- control ---")
            print("type: \t\t", self.type)
            print("control: \t", self.control)
            print("channel: \t", self.channel)
            print("value: \t\t", self.value)
        
        else:
            print("--- note ---")
            print("type: \t\t", self.type)
            print("note: \t\t", self.note)
            print("channel: \t", self.channel)
            print("velocity: \t", self.velocity)
        print("- - - - - - - - - - - - - - - - - - - - - ")    

    
    def __init__(self, msg): #the msg is a "raw" midi message
        
        self.type=msg.type
        self.time=msg.time  
        
        if getattr(msg, 'velocity', None): #used  hasattr() maybe it works better for nontype error ?
            #if self.velocity is None:                       #delete......NBNBNNBNB
            self.velocity=msg.velocity
            #self.velocity=msg.velocity
        else: self.velocity=None
        
        if getattr(msg, 'note', None): #the None prevents exception
            self.note=msg.note
        else: self.note=None
                  
        if getattr(msg, 'channel', None):
            self.channel=msg.channel
        else: self.channel = None
        
        if getattr(msg, 'control' ,None):
            self.control=msg.control
        else: self.control=None
    
        if getattr(msg, 'value', None):
            self.value =msg.value
        else: self.value=None


    def channel(self):
        return self.channel
    
    def velocity(self):
        return self.velocity
    
    def isControlChange(self):
        return self.type == 'control_change'
    
    def isNote(self):
        return self.type == 'note_on' or self.type == 'note_off'
    
    
    ### used by service if the message shall be detected ................................
    ## if the message has the same channel and type , we send it through 
    # more detailed info is handled by the callback
    def comp(self, msg): #compare  type and channel for now
        ## take into consideration the type of message note/cc
        if self.isControlChange(): #type, channel, control, (value is omitted)               
            if(self.channel == msg.channel and self.control == msg.control):
                return True              
        else: #assume note, #type, channel, note , (velocity is omitted)        
            if(self.type == msg.type and self.channel == msg.channel and self.note == msg.note):
                return True
        return False
    
    
    #same as comp only omitting the channel 
    def comp_omitChannel(self, msg): #compare  type and channel for now
       ## take into consideration the type of message note/cc
       if self.isControlChange(): #type, channel, control, (value is omitted)               
           if(self.control == msg.control):
               return True              
       else: #assume note, #type, channel, note , (velocity is omitted)        
           if(self.type == msg.type and self.note == msg.note):
            return True
       return False 

         


#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------   
class Service:

        
    def __init__(self, business):
        self._suppEvents = [EventType.chordEvent, EventType.controlEvent]
        self.subscribers = {event : dict() for event in self._suppEvents}
 
        self._business=business
        self._callback=0
    

    def getbusiness(self):
        return self._business
    
    def getSubscribers(self, event=EventType.chordEvent):
        return self.subscribers[event]
    
    
    #who = chords or controls found in EventClient
#    def reg(self, who, callback, eventType=EventType.chordId): 
#        self.getSubscribers(eventType)[who] = callback
    
    def reg(self, client, callback): 
        
        eventType=client.eventType   
        
        self.getSubscribers(eventType)[client] = callback
    
    def unregister(self, eventType , who):
        del self.getSubscribers(eventType)[who]
        
    def clear(self):   
        self.subscribers.clear()
        self.subscribers = {event : dict() for event in self._suppEvents}
        
    def setCallbackService(self, callback): #this will the callbackService 
        self._callbackService=callback
        
                
    def notify(self, midoMess):  #we send to all subscribers as we get a midi only from controller    
        for event in self.subscribers:
            for subscriber, callb in self.getSubscribers(event).items():
                if subscriber.midoMess.comp(midoMess):
                    callb(subscriber, self._business) #these paraneters must match callbackService(eventId, eventClient, midoMess, business):
                    break
        
    
    def load(self, filepath):
        # check if  self._callback is empty first ....
        if not self._callbackService: print("set callback for service class first")
        
        fs=Filesave(filepath)
        records=fs.load() #the lastsession file is default ..... make better use filename from glabals NBNBNBNNBN!
               
        for client in records:
            self.reg(client, self._callbackService)
                           
        print("Last session restored from file!, number of records: " , len(records))
          
        
    # subscriber = EventClient class
    def print(self, eventType=EventType.chordEvent):     

        for subscriber, callback in self.getSubscribers(eventType).items():
            subscriber.midoMess.printProp()
            #print(callback) # -- keep for check

  
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------   
class MidiDevice:
    def __init__(self):
        
        self._midiOut=None
        self._midiIn=None
        self._outdevname=""
        self._indevname=""
        self._nrdevIn=len(get_input_names())
        self._nrdevOut=len(get_output_names())
    

    def startListening(self):
        if log:print("message processing enabled: ")
        
        print("press ctrl+c for interruption") 
           
        def keyboardInterruptHandler(signal, frame): # move this to another place , we need to close the session obj           
            
            self.close() #call your function here 
            sys.exit("bye!") 
        
        signal.signal(signal.SIGINT, keyboardInterruptHandler)

        while True:
            for msg in self.midiIn().iter_pending():
                pass 
    
    def midiIn(self):
        return self._midiIn
    
    def midiOut(self):
        return self._midiOut
    
       
    def openDeviceOut(self, devNr):
        
        s=get_output_names() 
        if len(s)==0:
            self._outdevname="* no output devices found! *"
            return None
        
        self._outdevname = s[devNr]
        self._midiOut = open_output(self._outdevname)
        return self._midiOut
    
    def openDeviceIn(self, devNr):
        
        s=get_input_names() 
        if len(s)==0:
            self._indevname = "* no input devices found! *"
            return None
        
        self._indevname=s[devNr] 
        self._midiIn = open_input(self._indevname)
        return self._midiIn

    def openMidiAll(self, nrIn, nrOut):
        print("Number of in devices: ", self._nrdevIn)
        print("Number of out devices: ", self._nrdevOut)
        
        if self._nrdevIn > 0:
            self._midiIn = self.openDeviceIn(nrIn)
        else:
            print("no midi in available")

        if self._nrdevOut > 0:
            self._midiOut = self.openDeviceOut(nrOut)
        else:
            print("no midi out available")
                 
        print("selected in device: ->\t", self._indevname.strip())
        print("selected out device:->\t", self._outdevname.strip())
        if self._midiIn is None:
            print("no midi dev in")
            sys.exit()
            
        if self._midiOut is None:
            print("no midi dev out")
            sys.exit()
       
    def setCallback(self, callbackFunction):     #can be called anytime    

        self._midiIn.callback=callbackFunction
        print("callback enabled")
    
    #not tested
    def close(self):
        if self._midiOut is not None:
            self._midiOut.close()
            if self._midiOut.closed:
                print("midi out is closed")
            
        if self._midiIn is not None:    
            self._midiIn.close()
        
            if self._midiIn.closed:
                print("midi in is closed")
            
    def panic():
        self._midiOut.panic()
        
            
#        
#    def resetMidi():
#        ALL_SOUNDS_OFF = 120
#        for channel in range(16):
#            yield Message('control_change',
#                      channel=channel, control=ALL_SOUNDS_OFF)
#
#        pass

#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------    
class Filesave: #needs pickle 
    def __init__(self, filepath):
        self.path = filepath
        self.filename = "lastsession.dat"
        self.records = []
    def defaulFilename(self):
        return self.filename
        
    
    def setFilename(self, name):
        self.filename = name
        
    def addRecord(self, rec):
        self.records.append(rec)
        
    def deleteRecords(self):
        self.records.clear()
                
    def printloadedFile(self):
        print("from Class: ", __class__.__name__)
        for i in self.records:
            print(i)
            
    def _getpathAndFile(self):
        return self.path + self.filename
    
        
    def _isempty(self):       
        return len(self.records) == 0    
    
    def save(self, filename = "lastsession.dat"):
        with open(self.path + filename, "wb") as fh: 
            pickle.dump(self.records, fh, pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(self._getpathAndFile(), "rb") as fh:
            self.records = pickle.load(fh)
        return self.records
    
    def fileWithPath(self):
        return self._getpathAndFile()
 
    
    
#### -----------------------------------------------------
#### class 
####
#### -----------------------------------------------------     
class SysexHandler:
    def __init__(self, filepath):
        self.data=[]
        
    def send():
        pass
    def load():
        pass
    def erase():
        pass
        







