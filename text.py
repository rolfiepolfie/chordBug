# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 08:12:53 2020

@author: Rolf Eilert Johansen
"""





setMidiChannel_fcb1010="""
Set the MIDI Channels

The MIDI channel on your FCB1010 must match the MIDI channel used on your other MIDI gear.  If they are not the same,  MIDI commands sent buy the FCB1010 will just be ignored by your MIDI gear.  Try MIDI channel 1 on both for a start.

To set the MIDI channel on your FCB1010, do the following:

1. If FCB1010 is turned on, turn it off
2. Press and hold the Down button while you turn on the FCB1010.  Keep holding it down for about 5 seconds. When you see the small green light come on, release the button
3. Press the UP button once.  The green light will have changed to the MIDI Function selection.
4. Press the 1 button.  The 1 button LED and green light will begin to blink.  The display will change to show you the current MIDI channel for PC command.
5. Press the UP button once.  The green light will move to MIDI Chann and the display digit will begin to blink.
6. Press the 0 button and then the 1 button.  This will change it to MIDI channel 1.  The display should now show 01.
7. Press the UP button once.  The green light will move to the MIDI Config selection.
8. Now press and hold the Down button for about 5 seconds.  The display will change to 00.

"""


recievesysEx_fcb1010="""
Make FCB-1010 recieve sysex data:
1. Connect cables
2. Press DOWN and hold while powering up , enter global menu
3. Press UP until config led lights (must be in config mode)
4. Press footswitch #7 (SYSEX_RCV) to tell the unit to wait for sysex data 
    (footswitch LED lights up). 
5. Send sysex data from computer (footswitch LED blinks)
6. Footswitch LED blink ends if when data has been received correctly
7. Quit GLOBAL_CONFIG mode by a long press on DOWN    
"""



report="""**************NEXT TIME***************")
"https://docs.python.org/3/library/doctest.html")

2707-keyboard interupt made in dev object, make it or move to session close
2707-implement session.close() function
2707-fix readNewChords ("saving temporarily disabled!!!!!!!!")  
3107-make some controls detect on/off, Panic
3107-make use of dynamic instances to create cord schemes 

    def panic(self): make a control
---------------------------------------------------"""