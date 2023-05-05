# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:17:50 2022
@author: Edward Wait, Student N.O. 24755257

Changed the options for the advanced page.
Instead of teaching nesting if statements within loops,
instead shows how to create and use a function from the main class

Updated by: Joshua Porter-Lightwood
Last Updated: Thu Apr 28 11:07:47 2022
"""

import numpy as np
import cv2
from pydub import AudioSegment
from pydub.playback import play
import threading
import datetime

#globals for making use of buttons within the program
#global for selecting which button is pressed 
global optionClick
optionClick = 0
global optionClicked
optionClicked = False
#global for selecting depth of choices made in program
global depth
depth = 0
global consoleOutput
consoleOutput = ""
global choicesFinished
choicesFinished = False
#
global endTime
endTime = datetime.datetime.now()
global recalibrateTime
#global for storing the previous sound
global recalibrating
recalibrating = False
global prevSound
prevSound = AudioSegment.from_wav('sound/silence.wav')

# Beginning of Button Class

#callable class which allows the creation of the button, provided that appropriate values are passed into the relevant functions
class ButtonDraw(object):
    def __init__(self, name, x, y, w, h, img, colour, textColour, borderColour, textScale, textThickness,borderCheck, pointer, buttonSound):
        self.name = name
        self.coords = [x, y]
        self.sizes = [w, h]
        self.pointer = pointer
        self.hoverSound = buttonSound
        
        #values which are used by the hover function
        self.image = img
        self.colours = [colour, textColour, borderColour]
        self.scaling = [textScale, textThickness]
        self.bordering = borderCheck
        self.prevSound = None
        
        
        #check to see if button has a border
        if borderCheck == True:
            #drawing border first so button can be placed on top
            self.Border(0, self.colours[2])
        
        #drawing button
        cv2.rectangle(img, (x, y), (x+w, y+h), self.colours[0], -1)
        
        #calculate offset of text relative to button in order to centre and create text
        textBoxSize = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, textScale, textThickness)
        textX = int(x + (w - textBoxSize[0][0]) / 2)
        textY = int(y + textBoxSize[0][1] + (h - textBoxSize[0][1]) / 2)
        cv2.putText(img, name, (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, textScale, textColour, textThickness)
        
    #function that draws border around button
    def Border(self, borderThickness, borderColour):
        outlineX = int(self.coords[0] - 5)
        outlineY = int(self.coords[1] - 5)
        outlineW = int(self.sizes[0] + 10)
        outlineH = int(self.sizes[1] + 10) 
        #draw border
        cv2.rectangle(img, (outlineX, outlineY), (outlineX + outlineW, outlineY + outlineH), borderColour, -1)
      
    #function that changes colour of a button when hovered over by the cursor
    def Hover(self, cursorX, cursorY, traversalButtonCol, interactButtonCol, traversalHoverCol, interactHoverCol, backgroundCol, soundOn):
        #global variable that saves the previous sound to prevent repeated playback of same sound
        global prevSound
        #if the x value of the cursor's tip is within the dimensions of the button on the x axis...
        if cursorX >= self.coords[0] and cursorX <= (self.coords[0] + self.sizes[0]): 
            #if the y value of the cursor's tip is within the dimensions of the button on the y axis..
             if cursorY >= self.coords[1] and cursorY <= (self.coords[1] + self.sizes[1]):
                 #change the colours of the traversal buttons when hovered over
                     if self.colours[0] == traversalButtonCol:
                         buttonDisplay.append(ButtonDraw(
                                                    self.name,
                                                    self.coords[0],
                                                    self.coords[1],
                                                    self.sizes[0],
                                                    self.sizes[1],
                                                    self.image,
                                                    traversalHoverCol,
                                                    backgroundCol,
                                                    self.colours[2],
                                                    self.scaling[0],
                                                    self.scaling[1],
                                                    self.bordering,
                                                    self.pointer,
                                                    self.hoverSound
                                                    ))
                #change the colours of the interact buttons when hovered over
                     if self.colours[0] == interactButtonCol:
                         buttonDisplay.append(ButtonDraw(
                                                    self.name,
                                                    self.coords[0],
                                                    self.coords[1],
                                                    self.sizes[0],
                                                    self.sizes[1],
                                                    self.image,
                                                    interactHoverCol,
                                                    backgroundCol,
                                                    self.colours[2],
                                                    self.scaling[0],
                                                    self.scaling[1],
                                                    self.bordering,
                                                    self.pointer,
                                                    self.hoverSound
                                                    ))  
                #if the sound on variable is set to true...
                     if soundOn == True:
                         #if previous sound played is not equal to the current sound from the array...
                         if prevSound != self.hoverSound:
                            #and the button has a sound...
                            if self.hoverSound != None:
                                #call sound play function
                                self.SoundPlay()
                     return True
        return False
    
    def SoundPlay(self):
        #global variable that dictates from when a new sound can be played
        global endTime
        global prevSound
        
        #current time variable
        currentTime = datetime.datetime.now()
        #if the previous sound has finished playing...
        if currentTime > endTime:
            #variable adds silence between sounds
            mixedSound = AudioSegment.from_wav('sound/silence.wav')

            #append the current array cell of allSounds to mixedSound
            mixedSound = mixedSound.append(self.hoverSound,0)
            #variable that's set to the length of the sound to be played
            lengthSound = mixedSound.duration_seconds
            deltaSound = datetime.timedelta(0,lengthSound)
            
            
            #create a unique thread for the audio file to be played on to prevent program from freezing 
            t = threading.Thread(target=play, args=(mixedSound,))
            #play the sound file
            t.start()

            #setting variables for next time through
            endTime = currentTime + deltaSound
            prevSound = self.hoverSound

    #function that returns whether button has been clicked on
    def Click(self, cursorX, cursorY):
        if cursorX >= self.coords[0] and cursorX <= (self.coords[0] + self.sizes[0]): 
             if cursorY >= self.coords[1] and cursorY <= (self.coords[1] + self.sizes[1]):
                if self.pointer != None:    
                     print("Click. Pointing to ", self.pointer)
                     runPointer = self.pointer()
                     runPointer.Run()
                     return True
        return False
    
    
    def returnName(self):
        return self.name
    
# End of Button Class

# Beginning of Menu Classes

# Master Menu Class, all other Menu classes inherit from it
class Menus(object):
    global buttonDisplay
    buttonDisplay = []
    
    # Assigns the currentMenu variable to this menu
    def __init__(self):
        global currentMenu
        currentMenu = self
        
    # Called by the currentMenu variable to continually build this menu
    def Run(self):
        currentMenu.Build()

# Options Menu Class that controls all the menu's with questions
class OptionsMenu(Menus):
    def __init__(self):
        # Runs the Menus init function and then stores the coding classes as variables
        super().__init__()
        self.codeArea = CodingArea()
        self.codeConsole = CodingConsole()
        
    # Called when a new options menu is opened and resets all the variables
    def MenuCheck(self, menu):
        global optionClicked
        global depth
        global consoleOutput
        global choicesFinished
        
        if Menus.currentMenu != menu:
            optionClicked = False
            depth = 0
            consoleOutput = ""
            choicesFinished = False
            self.codeArea.ClearCodeArea()
            self.codeConsole.ClearCodeConsole()
                
    # Called to determine if a option has been selected
    # If so, tells the user whether they were right or wrong
    # If the user was right, appends the text to the coding console
    def OptionCheck(self, optionArray):
        global optionClicked
        global depth
        global consoleOutput
        global choicesFinished
        #if all correct choices have not been completed and if an option has been clicked on...
        if choicesFinished == False and optionClicked == True:
                #if the option's validity is true...
                if optionArray[depth][optionClick][1] == True:
                    #add the correct text from the array to the textbox
                    self.codeArea.AppendCodeArea(optionArray[depth][optionClick][0], optionArray[depth][3]) 
                    #if depth is equal to 0...
                    if depth != (len(optionArray)-1):
                        #increase depth
                        depth += 1
                        #make the console output display "correct choice"
                        self.codeConsole.ClearCodeConsole()
                        self.codeConsole.AppendCodeConsole("Correct Choice!")
                    else:
                        #make the output state the final output
                        self.codeConsole.ClearCodeConsole()
                        Menus.currentMenu.PageResponse()
                        choicesFinished = True
                else:
                    self.codeConsole.ClearCodeConsole()
                    self.codeConsole.AppendCodeConsole("Incorrect Choice!")
                #make optionClicked = False
                optionClicked = False
            
    # Getters for the coding variables
    def GetCodeArea(self):
        return self.codeArea
    def GetCodeConsole(self):
        return self.codeConsole
            
# Coding Area Class. Where all the text that the user has got right is placed
# This allows the user to see what the whole function would look like    
class CodingArea(object):
    # Assigns default values on start
    def __init__(self):
        self.contents = list()
        self.contents.append("")
        self.currentLine = 0
    
    # Creates the coding area on the page and assigns any text stored in contents to the page
    def Build(self, x, y, w, h, img, colour, textColour, borderColour, textScale):
        self.coords = [x, y]
        self.sizes = [w, h]
        
        #values which are used by the hover function
        self.image = img
        self.colours = [colour, textColour, borderColour]
        self.scaling = [textScale, textThickness]
        
        #drawing border first so button can be placed on top
        self.Border(0, self.colours[2])
        
        #drawing button
        cv2.rectangle(img, (x, y), (x+w, y+h), self.colours[0], -1)
        
        for i in range(len(self.contents)):    
            #calculate offset of text relative to button in order to centre and create text
            textBoxSize = cv2.getTextSize(self.contents[i], cv2.FONT_HERSHEY_SIMPLEX, textScale, textThickness)
            if len(self.contents) != 1:
                i2 = (len(self.contents) / 20) + 1
                textY = int((y + textBoxSize[0][1] + (h - textBoxSize[0][1]) / 2) / i2)
            else:
                textY = int((y + textBoxSize[0][1] + (h - textBoxSize[0][1]) / 2))
            if i != 0:
                i2 = (i/10) + 1
                textY = int(textY * i2)

            textX = int(x + 10)
            cv2.putText(img, self.contents[i], (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, textScale, textColour, textThickness)
        
    #function that draws border around button
    def Border(self, borderThickness, borderColour):
        outlineX = int(self.coords[0] - 5)
        outlineY = int(self.coords[1] - 5)
        outlineW = int(self.sizes[0] + 10)
        outlineH = int(self.sizes[1] + 10) 
        #draw border
        cv2.rectangle(img, (outlineX, outlineY), (outlineX + outlineW, outlineY + outlineH), borderColour, -1)
        
    # Assigns text to contents and applies a new line if needed
    def AppendCodeArea(self, textToAppend, newLine):
        if newLine == False:
            self.contents[self.currentLine] += textToAppend
        else:
            self.currentLine += 1
            self.contents.append(textToAppend)
            
    # Wipes the coding area of text
    def ClearCodeArea(self):
        for i in range(len(self.contents)):
            self.contents[i] = ""
        self.currentLine = 0
        
# Coding Console Class. Similar to the coding area, but stores text differently
class CodingConsole(object):
    # Declares needed variables to start
    def __init__(self):
        self.contents = list()
    
    # Builds the coding console
    def Build(self, x, y, w, h, img, colour, textColour, borderColour, textScale):
        self.coords = [x, y]
        self.sizes = [w, h]
        
        #values which are used by the hover function
        self.image = img
        self.colours = [colour, textColour, borderColour]
        self.scaling = [textScale, textThickness]
        
        #drawing border first so button can be placed on top
        self.Border(0, self.colours[2])
        
        #drawing button
        cv2.rectangle(img, (x, y), (x+w, y+h), self.colours[0], -1)
        
        self.OutputScaling()

        
    #function that draws border around button
    def Border(self, borderThickness, borderColour):
        outlineX = int(self.coords[0] - 5)
        outlineY = int(self.coords[1] - 5)
        outlineW = int(self.sizes[0] + 10)
        outlineH = int(self.sizes[1] + 10) 
        #draw border
        cv2.rectangle(img, (outlineX, outlineY), (outlineX + outlineW, outlineY + outlineH), borderColour, -1)
        
    # Appends text to the code console
    def AppendCodeConsole(self, textToAppend):
        self.contents.append(textToAppend)
            
    # Clears the code console of text
    def ClearCodeConsole(self):
        self.contents.clear()
        
    # Called on build and places the text within contents on the page
    # If any text is outside of the console window, the latest stored information
    # is removed and the scaling recalibrates
    def OutputScaling(self):
        try:
            for i in range(len(self.contents)):    
                # Base value for determining the spacing between the outputs
                i2 = ((i/20) + 1)
                
                # Size of the output box
                textY = int(self.coords[1] + self.sizes[1])
                
                # If multiple things need to be outputted, it spaces them out
                if i != 0:
                    textY = int(textY / i2)
                
                # Padding
                textY -= 10
                
                # If the text exits out of the output box, it removes the first text stored and recalibrates
                if textY < (self.coords[1] + 10) or textY > (self.coords[1]+self.sizes[1]):
                    self.contents.pop(0)
                    i2 = (((i-1)/20) + 1)
                    textY = int((self.coords[1] + self.sizes[1]) / i2)

                # Calculates the x position of the text and then places the text
                textX = int(self.coords[0] + 10)
                cv2.putText(img, self.contents[i], (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, self.scaling[0], self.colours[1], self.scaling[1])
        except:
            print("Answers Finished")


        
class DisplayAppend(object):
    def __init__(self, buttonArray):
        buttonArrayRows = len(buttonArray)
        buttonArrayColumns = len(buttonArray[0])
        
        for i in range(buttonArrayRows):
            buttonDisplay.append(ButtonDraw(buttonArray[i][0],
                                   buttonArray[i][1],
                                   buttonArray[i][2],
                                   buttonArray[i][3],
                                   buttonArray[i][4],
                                   buttonArray[i][5],
                                   buttonArray[i][6],
                                   buttonArray[i][7],
                                   buttonArray[i][8],
                                   buttonArray[i][9],
                                   buttonArray[i][10],
                                   buttonArray[i][11],
                                   buttonArray[i][12],
                                   buttonArray[i][13]
                                   ))
        
            
# MainMenu class which is called at the very beginning
class MainMenu(Menus):
        
    # Called by the run function inherited by the Menus class, contains all the code to build the menu
    def Build(self):
        Menus.currentMenu = self
        #array which has the information required for placement of buttons and text
        #the title is considered is a button, but the border and click functionality are never called
        buttonArray = [
            ["Coursework 2", titleBoxLocX, titleBoxLocY, titleBoxSizeX, titleBoxSizeY, img, colOutlines, colTitleText, colOutlines, titleSize, titleThickness,False, None, AudioSegment.from_wav('sound/coursework_2.wav')],
            ["Hello World", windowCentreX - 550, windowSizeY - 420, 270, 140, img, colTraversalButton, colOutlines, colOutlines, textSize + 0.3, textThickness + 1,True, HelloWorldMenu, AudioSegment.from_wav('sound/hello_world.wav')],
            ["Counter", windowCentreX - 130, windowSizeY - 420, 270, 140, img, colTraversalButton, colOutlines, colOutlines, textSize + 0.3, textThickness + 1,True, CounterMenu, AudioSegment.from_wav('sound/counter.wav')],
            ["Advanced", windowCentreX + 290, windowSizeY - 420, 270, 140, img, colTraversalButton, colOutlines, colOutlines, textSize + 0.3, textThickness + 1,True, AdvancedMenu, None],
            ["Settings", windowCentreX - 600, windowCentreY + 200, 200, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, SettingsMenu, AudioSegment.from_wav('sound/settings.wav')],
            ["Edward Wait, Josh Porter Lightwood", nameBoxLocX, nameBoxLocY, 600, 80, img, colBackground, colOutlines, colOutlines, textSize, textThickness,True, None, AudioSegment.from_wav('sound/names.wav')]
            ]
                  
        buttonDisplay.clear()

        # Place into an array and declare them by hand, then you can run a foreach loop with the click function
        # This should allow you to find out which button has been hovered over for the time by having the
        # function = True. If it doesn't return True, then the button either hasn't been hovered long enough
        # or its not being hovered over at all
        DisplayAppend(buttonArray)
            
class HelloWorldMenu(OptionsMenu):
        
    # Called by the run function inherited by the Menus class, contains all the code to build the menu
    def Build(self):
        # Assigns all the required options menus
        OpMenu = super()
        OpMenu.MenuCheck(self)
        OpCodeArea = OpMenu.GetCodeArea()
        self.OpCodeConsole = OpMenu.GetCodeConsole()
            
        Menus.currentMenu = self
        
        #array with the text on the button options, and whether they are the correct or incorrect answers
        optionArray = [[['print("',True],['Flobby"',False], ['Writeline("', False], False],
                       [['Hello World")', True], ['Hollo Warld......', False], ['Hallo Wood"', False], False]]

        #setting the values of the buttons based on the array
        option0 = optionArray[depth][0][0]
        option1 = optionArray[depth][1][0]
        option2 = optionArray[depth][2][0]
        
        # Checks if the options were correct or not
        OpMenu.OptionCheck(optionArray)

        
        
        #array which has the information required for placement of buttons and text
        #the title is considered is a button, but the border and click functionality are never called
        buttonArray = [
            ["Hello World", titleBoxLocX, titleBoxLocY, titleBoxSizeX, titleBoxSizeY, img, colOutlines, colTitleText, colOutlines, titleSize, titleThickness,False, None, AudioSegment.from_wav('sound/hello_world.wav')],
            [option0, windowCentreX + 350, windowCentreY - 150, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option0, None],
            [option1, windowCentreX + 350, windowCentreY - 45, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option1, None],
            [option2, windowCentreX + 350, windowCentreY + 60, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option2, None],
            ["Main Menu", windowCentreX - 600, windowCentreY + 200, 200, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, MainMenu, AudioSegment.from_wav('sound/main_menu.wav')],
            ["Counter", windowCentreX + 350, windowCentreY + 200, 220, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, CounterMenu, AudioSegment.from_wav('sound/counter.wav')]
            ]
        
        # Creates the coding area and the coding console for the page
        OpCodeArea.Build(windowCentreX - 600, titleBoxLocY + titleBoxSizeY + 50, 850, 300, img, colTitleText, colOutlines, colOutlines, textSize)
        self.OpCodeConsole.Build(windowCentreX - 600 + 200 + 50, windowCentreY + 200, 600, 100, img, colTitleText, colOutlines, colOutlines, textSize)
          
        
        buttonDisplay.clear()
        # Place into an array and declare them by hand, then you can run a foreach loop with the click function
        # This should allow you to find out which button has been hovered over for the time by having the
        # function = True. If it doesn't return True, then the button either hasn't been hovered long enough
        # or its not being hovered over at all
        DisplayAppend(buttonArray)
        
    # Called when all the options have been picked and the end result is shown
    def PageResponse(self):
        self.OpCodeConsole.AppendCodeConsole("Hello World")
            
class CounterMenu(OptionsMenu):
    # Called by the run function inherited by the Menus class, contains all the code to build the menu
    def Build(self):
        # Assigns all the required options menus
        OpMenu = super()
        OpMenu.MenuCheck(self)
        OpCodeArea = OpMenu.GetCodeArea()
        self.OpCodeConsole = OpMenu.GetCodeConsole()
            
        Menus.currentMenu = self
        
        #array with the text on the button options, and whether they are the correct or incorrect answers
        optionArray = [[['when i', False],['keep going i', False], ['for i', True], False],
                       [[' become 3', False], [' in range(3)', True], [' stopAt(3)', False], False],
                       [['Execute(3)', False], ['print(3)', False], ['print(i)', True], True]]

        #setting the values of the buttons based on the array
        option0 = optionArray[depth][0][0]
        option1 = optionArray[depth][1][0]
        option2 = optionArray[depth][2][0]
        
        # Checks if the options were correct or not
        OpMenu.OptionCheck(optionArray)

        
        
        #array which has the information required for placement of buttons and text
        #the title is considered is a button, but the border and click functionality are never called
        buttonArray = [
            ["Counter", titleBoxLocX, titleBoxLocY, titleBoxSizeX, titleBoxSizeY, img, colOutlines, colTitleText, colOutlines, titleSize, titleThickness,False, None, AudioSegment.from_wav('sound/counter.wav')],
            [option0, windowCentreX + 350, windowCentreY - 150, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option0, None],
            [option1, windowCentreX + 350, windowCentreY - 45, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option1, None],
            [option2, windowCentreX + 350, windowCentreY + 60, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option2, None],
            ["Main Menu", windowCentreX - 600, windowCentreY + 200, 200, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, MainMenu, AudioSegment.from_wav('sound/main_menu.wav')],
            ["Advanced", windowCentreX + 350, windowCentreY + 200, 220, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, CounterMenu, AudioSegment.from_wav('sound/hello_world.wav')]
            ]
        
        # Creates the coding area and the coding console for the page
        OpCodeArea.Build(windowCentreX - 600, titleBoxLocY + titleBoxSizeY + 50, 850, 300, img, colTitleText, colOutlines, colOutlines, textSize)
        self.OpCodeConsole.Build(windowCentreX - 600 + 200 + 50, windowCentreY + 200, 600, 100, img, colTitleText, colOutlines, colOutlines, textSize)

        
        buttonDisplay.clear()
        # Place into an array and declare them by hand, then you can run a foreach loop with the click function
        # This should allow you to find out which button has been hovered over for the time by having the
        # function = True. If it doesn't return True, then the button either hasn't been hovered long enough
        # or its not being hovered over at all
        DisplayAppend(buttonArray)
        
    # Called when all the options have been picked and the end result is shown
    def PageResponse(self):
        for i in range(3):
            self.OpCodeConsole.AppendCodeConsole(str(i))

class AdvancedMenu(OptionsMenu): 
    # Called by the run function inherited by the Menus class, contains all the code to build the menu
    def Build(self):
        # Assigns all the required options menus
        OpMenu = super()
        OpMenu.MenuCheck(self)
        OpCodeArea = OpMenu.GetCodeArea()
        self.OpCodeConsole = OpMenu.GetCodeConsole()
        
        Menus.currentMenu = self
        
        #array with the text on the button options, and whether they are the correct or incorrect answers
        optionArray = [[['func Function', False],['def Function', True], ['Function create', False], False],
                       [['(object, x)', False], ['(build, x)', False], ['(self, x)', True], False],
                       [['print("x")', False], ['print(range)', False], ['print(x)', True], True],
                       [['#Comment ', True], ['//Comment ', False], ['<--Comment ', False], True],
                       [['Function End', True], ['Function Done', True], ['Finally Finished', True], False],
                       [['x = 1', True], ['x = 2', True], ['x = 3', True], True],
                       [['Function(x)', True], ['Function = x', False], ['Function(self  x)', False], True]]
        
        #setting the values of the buttons based on the array
        option0 = optionArray[depth][0][0]
        option1 = optionArray[depth][1][0]
        option2 = optionArray[depth][2][0]
        
        # Stores the final decision of the user!
        if depth == 5:
            finalOptions = ["1", "2", "3"]
            self.specialOption = finalOptions[optionClick]
            
        
        # Checks if the options were correct or not
        OpMenu.OptionCheck(optionArray)
        
        #array which has the information required for placement of buttons and text
        #the title is considered is a button, but the border and click functionality are never called
        buttonArray = [
            ["Advanced", titleBoxLocX, titleBoxLocY, titleBoxSizeX, titleBoxSizeY, img, colOutlines, colTitleText, colOutlines, titleSize, titleThickness,False, None, AudioSegment.from_wav('sound/counter.wav')],
            [option0, windowCentreX + 350, windowCentreY - 150, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option0, None],
            [option1, windowCentreX + 350, windowCentreY - 45, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option1, None],
            [option2, windowCentreX + 350, windowCentreY + 60, 220, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True, Option2, None],
            ["Main Menu", windowCentreX - 600, windowCentreY + 200, 200, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, MainMenu, AudioSegment.from_wav('sound/main_menu.wav')],
            ["Hello World", windowCentreX + 350, windowCentreY + 200, 220, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, HelloWorldMenu, AudioSegment.from_wav('sound/hello_world.wav')]
            ]
 
        # Creates the coding area and the coding console for the page
        OpCodeArea.Build(windowCentreX - 600, titleBoxLocY + titleBoxSizeY + 50, 850, 300, img, colTitleText, colOutlines, colOutlines, textSize)
        self.OpCodeConsole.Build(windowCentreX - 600 + 200 + 50, windowCentreY + 200, 600, 100, img, colTitleText, colOutlines, colOutlines, textSize)
        
        buttonDisplay.clear()
        # Place into an array and declare them by hand, then you can run a foreach loop with the click function
        # This should allow you to find out which button has been hovered over for the time by having the
        # function = True. If it doesn't return True, then the button either hasn't been hovered long enough
        # or its not being hovered over at all
        DisplayAppend(buttonArray)
        
    # Called when all the options have been picked and the end result is shown
    def PageResponse(self):
        self.OpCodeConsole.AppendCodeConsole(self.specialOption)
            
class SettingsMenu(Menus):   
    # Called by the run function inherited by the Menus class, contains all the code to build the menu
    def Build(self):
        Menus.currentMenu = self
        #array which has the information required for placement of buttons and text
        #the title is considered is a button, but the border and click functionality are never called
        buttonArray = [
            ["Settings", titleBoxLocX, titleBoxLocY, titleBoxSizeX, titleBoxSizeY, img, colOutlines, colTitleText, colOutlines, titleSize, titleThickness,False, None, AudioSegment.from_wav('sound/settings.wav')],
            ["Dark Mode", windowCentreX - 400, windowCentreY - 120, 200, 100, img, colOutlines, colBackground, colOutlines, textSize, textThickness,True,  DarkMode, AudioSegment.from_wav('sound/dark_mode.wav')],
            ["Audio", windowCentreX + 200, windowCentreY - 120, 200, 100, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  SoundSwitch, AudioSegment.from_wav('sound/sound.wav')],
            ["Cursor Size", windowCentreX - 450, windowCentreY + 50, 300, 80, img, colBackground, colOutlines, colOutlines, textSize, textThickness,True,  None, AudioSegment.from_wav('sound/cursor_size.wav')],
            ["-", windowCentreX - 530, windowCentreY + 50, 80, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  CursorSizeLower, AudioSegment.from_wav('sound/-.wav')],
            ["+", windowCentreX - 150, windowCentreY + 50, 80, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  CursorSizeHigher,AudioSegment.from_wav('sound/+.wav')],
            ["Cursor Sensitivity", windowCentreX + 150, windowCentreY + 50, 300, 80, img, colBackground, colOutlines, colOutlines, textSize, textThickness,True,  None, AudioSegment.from_wav('sound/cursor_sensitivity.wav')],
            ["-", windowCentreX + 70, windowCentreY + 50, 80, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  CursorSensLower, AudioSegment.from_wav('sound/-.wav')],
            ["+", windowCentreX + 450, windowCentreY + 50, 80, 80, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  CursorSensHigher, AudioSegment.from_wav('sound/+.wav')],
            ["Recalibrate Triggers", windowCentreX - 200, windowCentreY + 200, 400, 100, img, colInteractButton, colOutlines, colOutlines, textSize, textThickness,True,  RecalibratePage, AudioSegment.from_wav('sound/recalibrate_triggers.wav')],
            ["Main menu", windowCentreX - 600, windowCentreY + 200, 200, 100, img, colTraversalButton, colOutlines, colOutlines, textSize, textThickness,True, MainMenu, AudioSegment.from_wav('sound/main_menu.wav')]
            ]
                  
        buttonDisplay.clear()
        # Place into an array and declare them by hand, then you can run a foreach loop with the click function
        # This should allow you to find out which button has been hovered over for the time by having the
        # function = True. If it doesn't return True, then the button either hasn't been hovered long enough
        # or its not being hovered over at all
        DisplayAppend(buttonArray)
        
class RecalibratePage(Menus):
    def Build(self):
        #recalibrate time is the time that current time is checked against to see whether three seconds has elapsed
        global recalibrateTime
        #recalibrating is a first time through switch for the recalibrate page function
        global recalibrating
        #recalibrate is the switch to say whether the user's bodypart should be identified as being in a new neutral position
        global recalibrate
        Menus.currentMenu = self
        
        #setting the current time for each run of the loop
        currentTime = datetime.datetime.now()

        #if first time through when clicking button...
        if recalibrating == False:
            #set recalibrate time to current time + 3 seconds
            recalibrateTime = currentTime + datetime.timedelta(0,3)
            #prevent loop being passed through until recalibrate button is hit again
            recalibrating = True
            

        #set up text on screen to describe what users should do on page
        buttonArray = [
            ["Please place your face in the desired neutral position", titleBoxLocX - 200, titleBoxLocY + 100, 1000, titleBoxSizeY, img, colOutlines, colTitleText, None, textSize, textThickness,False, None, None]
            ]
        buttonDisplay.clear()
        DisplayAppend(buttonArray)
        

        #if current time has gone further than the three seconds specified...
        if currentTime > recalibrateTime:
            #set recalibrate to true
            recalibrate = True
            #reset recalibrating to allow for use on next run through
            recalibrating = False
            #leave page
            Menus.currentMenu = SettingsMenu()
        
            
# End of Menu Classes

# Start of Settings Classes

# Alternates the screen between dark mode and light mode
class DarkMode(object):
    def Run(self):
        global darkMode, checkDarkMode
        self.darkMode = darkMode
        darkMode = not self.darkMode
        checkDarkMode = True
        
class SoundSwitch(object):
    def Run(self):
        global soundOn
        self.soundOn = soundOn
        soundOn = not self.soundOn
        
# CursorSize classes, the class name should be called from the buttonarray
# Any values will need to be changed in here
class CursorSizeLower(object):
    def Run(self):
        global cursorSizeY, cursorSizeX
        # If statement to provide a limit to size
        if(cursorSizeX > 1):
            cursorSizeX-= 1
            cursorSizeY-= 1
            print(cursorSizeX)
            print(cursorSizeY)
class CursorSizeHigher(object):
    def Run(self):
        global cursorSizeY, cursorSizeX
        # If statement to provide a limit to size
        if(cursorSizeX < 5):
            cursorSizeX+= 1
            cursorSizeY+= 1
            print(cursorSizeX)
            print(cursorSizeY)
    
# CursorSensitivity classes, the name should be called from the buttonarray
# Any values will need to be changed here
class CursorSensLower(object):
    def Run(self):
        global cursorSensitivity
        # If statement to provide a limit to sensitivity
        if(cursorSensitivity > 1):
            cursorSensitivity-= 0.5
            print(cursorSensitivity)
class CursorSensHigher(object):
    def Run(self):
        global cursorSensitivity
        # If statement to provide a limit to sensitivity
        if(cursorSensitivity < 5):
            cursorSensitivity+= 0.5
            print(cursorSensitivity)
    
#Options for each page of the program to be called by the main program pages
class Option0(object):    
    def Run(self):
        global optionClick
        global optionClicked
        optionClick = 0
        optionClicked = True
        
class Option1(object):
    def Run(self):
        global optionClick
        global optionClicked
        optionClick = 1
        optionClicked = True
    
class Option2(object):
    def Run(self):
        global optionClick
        global optionClicked
        optionClick = 2
        optionClicked = True
        
# End of Settings Classes
    
#function that draws open hand on screen based on cascade location
def cursorOpen(img, sizeX, sizeY, posX, posY, outlineColour):
    #cursor creation
    pts = np.array([
                    [posX - sizeX * -2,posY + sizeY * 8],
                    [posX - sizeX * 6, posY - (sizeY * 7)], 
                    [posX - sizeX * 3, posY - (sizeY * 9)],
                    [posX + sizeX * 1.5, posY - (sizeY * 5)],
                    [posX + sizeX * 1.5, posY - (sizeY * 20)],
                    [posX + sizeX * 5, posY - (sizeY * 20)],
                    [posX + sizeX * 5, posY - (sizeY * 5)],
                    [posX + sizeX * 5, posY - (sizeY * 23)],
                    [posX + sizeX * 8.5, posY - (sizeY * 23)],
                    [posX + sizeX * 8.5, posY - (sizeY * 5)],
                    [posX + sizeX * 8.5, posY - (sizeY * 21)],
                    [posX + sizeX * 12, posY - (sizeY * 21)],
                    [posX + sizeX * 12, posY - (sizeY * 5)],
                    [posX + sizeX * 12, posY - (sizeY * 18)],
                    [posX + sizeX * 15.5, posY - (sizeY * 18)],
                    [posX + sizeX * 15.5, posY + sizeY * 4],
                    [posX + sizeX * 15, posY + sizeY * 6],
                    [posX + sizeX * 14, posY + sizeY * 8]
                 
                    ], np.int32)
    pts = pts.reshape((-1,1,2))
    
    #draw unfilled polygon to image
    cv2.polylines(img, [pts], True, outlineColour,2)
    
#function that draws pointing hand on screen based on cascade location
def cursorPoint(img, sizeX, sizeY, posX, posY, outlineColour, fillCheck):
    #cursor creation
    pts = np.array([
                    [posX - sizeX * -2,posY + sizeY * 8],
                    [posX - sizeX * 6, posY - (sizeY * 7)], 
                    [posX - sizeX * 3, posY - (sizeY * 9)],
                    [posX + sizeX * 1.5, posY - (sizeY * 5)],
                    [posX + sizeX * 1.5, posY - (sizeY * 20)],
                    [posX + sizeX * 5, posY - (sizeY * 20)],
                    [posX + sizeX * 5, posY - (sizeY * 5)],
                    [posX + sizeX * 5, posY - (sizeY * 13)],
                    [posX + sizeX * 8.5, posY - (sizeY * 13)],
                    [posX + sizeX * 8.5, posY - (sizeY * 5)],
                    [posX + sizeX * 8.5, posY - (sizeY * 12)],
                    [posX + sizeX * 12, posY - (sizeY * 12)],
                    [posX + sizeX * 12, posY - (sizeY * 5)],
                    [posX + sizeX * 12, posY - (sizeY * 11)],
                    [posX + sizeX * 15.5, posY - (sizeY * 11)],
                    [posX + sizeX * 15.5, posY + sizeY * 4],
                    [posX + sizeX * 15, posY + sizeY * 6],
                    [posX + sizeX * 14, posY + sizeY * 8]
                 
                    ], np.int32)
    pts = pts.reshape((-1,1,2))
    
    #check to see whether hand is filled or outline
    if fillCheck == False:
        #creating unfilled polygon
        cv2.polylines(img, [pts], True, outlineColour,2)
    else:
    #creating filled polygon
        cv2.fillPoly(img,[pts],outlineColour)


#main function which sets up values for other functions, contains window and animation logic
if __name__ == "__main__":  
    #window setup
    windowSizeX = int(1280) 
    windowSizeY = int(720) 
    windowCentreX = int(windowSizeX / 2)
    windowCentreY = int(windowSizeY / 2)
    
    
    #setup camera parameters
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(1, 1)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, windowSizeX)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,windowSizeY)
    
    #reading in cascade xml for detecting body part
    detected_cascade1 = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    
    #changeable colours
    #draw indicator colours
    drawIndicatorB = 255
    drawIndicatorG = int()
    drawIndicatorR = int()

    
    #line thicknesses
    lineFill = -1
    lineThickness = 2
    drawThickness = 13
    
    #bodypart text settings
    textLocationX = int(windowSizeX - 200)
    textLocationY = int(60)
    textThickness = 2
    textSize = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    textCheck = False
    
    #title settings
    titleSize = 2.5
    titleThickness = 4
    titleBoxLocX = 350
    titleBoxLocY = 60
    titleBoxSizeX = 600
    titleBoxSizeY = 120
    
    #author textbox variables
    nameBoxLocX = 370
    nameBoxLocY = 580
    
    #cursor settings
    cursorSizeX = 2
    cursorSizeY = cursorSizeX
    cursorSensitivity = 2.5
    
    #cursor animation setup
    cursorFillCheck = False
    clickAnimCount = 0.1
    clickAnimCheck = False
    
    #window colour palette setting, 3 = full colours with no alpha channel
    windowColourSetting = int(3)
    
    #movement settings
    movementCheck = False
    movementCounter = int(0)
    
    #body part coordinate values
    cascadeX = 0
    cascadeY = 0
    cascadeW = 0
    
    #distance of body part from camera
    recalibrate = True
    getTriggerWidth = False
    #variable for storing initial width of body part for distance based triggers

    setTriggerWidth = 0
    
    
    #sound settings
    startTime = datetime.datetime.now()
    

    #sound file import
    allSounds = [
        AudioSegment.from_wav('sound/silence.wav'),
        AudioSegment.from_wav('sound/coursework_2.wav'),
        AudioSegment.from_wav('sound/main_menu.wav'),
        AudioSegment.from_wav('sound/settings.wav'),
        AudioSegment.from_wav('sound/hello_world.wav'),
        AudioSegment.from_wav('sound/counter.wav'),
        AudioSegment.from_wav('sound/dark_mode.wav'),
        AudioSegment.from_wav('sound/+.wav'),
        AudioSegment.from_wav('sound/-.wav'),
        AudioSegment.from_wav('sound/cursor_size.wav'),
        AudioSegment.from_wav('sound/cursor_sensitivity.wav'),
        AudioSegment.from_wav('sound/recalibrate_triggers.wav'),
        AudioSegment.from_wav('sound/correct_choice.wav'),
        AudioSegment.from_wav('sound/incorrect_choice.wav'),
                ]
    
    soundOn = False
    
    #dark mode settings
    checkDarkMode = True
    darkMode = False
    
    # Creation of the start menu. This stays outside the loop so that currentMenu can be changed
    currentMenu = MainMenu()
    
    
    #main loop check
    mainLoop = True
    
    #video camera loop
    while mainLoop == True:
        #check to make sure colours are only set once when toggling darkmode or initialising program
        if checkDarkMode == True:
            #check to change colours based on dark mode setting
            if darkMode == True:
                #colours
                colOutlines = (232,232,232)
                colBackground = (52,52,52)
                colDrawingCheck = (0,0,255)
                colCursorOutline = (255,255,255)
                colTitleText = (0,0,0)
                colTraversalButton = (89,155,0)
                colInteractButton = (190,50,37)
                colTraversalHover = (149,231,206)
                colInteractHover = (255,150,37)
                colClickFill = (97,176,255)
            else:
                #colours
                colOutlines = (52,52,52)
                colBackground = (232,232,232)
                colDrawingCheck = (255,0,0)
                colCursorOutline = (0,0,0)
                colTitleText = (255,255,255)
                colTraversalButton = (149,231,206)
                colInteractButton = (255,150,37)
                colTraversalHover = (89,155,0)
                colInteractHover = (190,50,37)
                colClickFill = (97,176,255)
            checkDarkMode = False
        
        # Creating a black image
        img = np.zeros((windowSizeY,windowSizeX,windowColourSetting), np.uint8) 
        #setting up background colour of image
        img[:] = colBackground
        ret,frame = camera.read()
        
        textCheck = False
        
        if(ret):        
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cascade1 = detected_cascade1.detectMultiScale(frame, 1.1, 5)
            
            #cascade loop
            for (x,y,w,h) in cascade1:
                faceDetected = True
                #creating face position / width for use outside of loop
                cascadeX = int(x)
                cascadeY = int(y)
                cascadeW = w
                #print("Cascade W = ", cascadeW)
                textCheck = True
                
            if getTriggerWidth == True:
                setTriggerWidth = cascadeW
                getTriggerWidth = False
                
            #when distance check is true, create variable to allow for resetting width based triggers
            if recalibrate == True:
                getTriggerWidth = True
                print("Distance Checked")
                recalibrate = False
                print("setTriggerWidth = ", setTriggerWidth)
                    
            cascadeCenterX = cascadeX + (cascadeW / 2)
            cascadeCenterY = cascadeY + (cascadeW / 2)
            
            intCenterX = int(windowSizeX - ((cascadeCenterX - windowCentreX) * cursorSensitivity + windowCentreX))
            intCenterY = int((cascadeCenterY - windowCentreY) * cursorSensitivity + windowCentreY)
            
            #setting the max distance that the cursor can travel on the x axis
            intCenterX = min(windowSizeX,intCenterX)
            intCenterX = max(0,intCenterX)
            #setting the max distance that the cursor can travel on the y axis
            intCenterY = min(windowSizeY,intCenterY)
            intCenterY = max(0,intCenterY)
            
            #face detected text indicator
            if textCheck == True:
                cv2.putText(img,'Bodypart',(textLocationX, textLocationY),
                            font, textSize,colDrawingCheck,textThickness,cv2.LINE_AA)
                cv2.putText(img,'Detected',(textLocationX, textLocationY + 35),
                            font, textSize,colDrawingCheck,textThickness,cv2.LINE_AA)
            
            # Runs the currentMenu which will change to the corrisponding button when clicked
            currentMenu.Run()

            #drawing colour indicator circle
            cv2.circle(img, (100,45), 18, colCursorOutline, lineFill)
            
            #loop through the buttonDisplay
            for i in range(len(buttonDisplay)):
                #call button hover function, pushing appropriate colours through to allow for colours in buttonDisplay to be changed
                if (buttonDisplay[i].Hover(intCenterX - (-2 * cursorSizeX),(intCenterY - (20 * cursorSizeY)), colTraversalButton, colInteractButton, colTraversalHover, colInteractHover, colBackground, soundOn)) == True:
                    audioName = buttonDisplay[i].returnName
                    break
            
            #if face is far from screen...
            if cascadeW < (setTriggerWidth * 1.2):
                #if darkmode is turned on...
                if darkMode == True:
                    #set square indicator to new colour to indicate that face is far from screen
                    drawIndicatorB = 0
                    drawIndicatorG = 0
                    drawIndicatorR = 255
                else:
                    #set square indicator to new colour to indicate that face is far from screen
                    drawIndicatorB = 255
                    drawIndicatorG = 0
                    drawIndicatorR = 0
                    
                clickAnimCheck = False
                cursorOpen(img,  cursorSizeX, cursorSizeY, intCenterX, intCenterY, colCursorOutline)
                clickAnimCount = 0.1
            
            #if face is close to screen...
            if cascadeW >= (setTriggerWidth * 1.2):
                #if click hasn't been performed before...
                if clickAnimCheck == False:    
                    #if cursor animation is small than full cursor...
                    if clickAnimCount < cursorSizeX:
                        #increase cursor animation's size
                        clickAnimCount += 0.1 * (cursorSizeX / 2)
                        cursorFillCheck = True
                        #draw cursor animation
                        cursorPoint(img,  clickAnimCount, clickAnimCount, intCenterX, intCenterY, colClickFill, cursorFillCheck)
                    else:
                        #reset size of cursor animation
                        clickAnimCount = 0.1
                        clickAnimCheck = True
                        for i in range(len(buttonDisplay)):
                            if (buttonDisplay[i].Click(intCenterX - (-2 * cursorSizeX),(intCenterY - (20 * cursorSizeY)))) == True:
                                break
                        
                if darkMode == True:
                    #set indicator to black to indicate pressing
                    drawIndicatorB = 255
                    drawIndicatorG = 255
                    drawIndicatorR = 255
                else:
                    #set indicator to white to indicate pressing
                    drawIndicatorB = 0
                    drawIndicatorG = 0
                    drawIndicatorR = 0
                        
                cursorFillCheck = False
                cursorPoint(img,  cursorSizeX, cursorSizeY, intCenterX, intCenterY, colCursorOutline, cursorFillCheck)
            
                        
            #colour indicators
            #drawing indicator
            drawIndicatorColour = (drawIndicatorB,drawIndicatorG,drawIndicatorR)
            
            #drawing distance indicator rectangle
            cv2.rectangle(img, (60,60), (30,30), drawIndicatorColour, lineFill)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.circle(img, (950, 400), 50, (165, 100, 255), -1)
                for i in range(len(buttonDisplay)):
                    if buttonDisplay[i].Click(950, 400) == True:
                        break
                    
            if cv2.waitKey(10) & 0xFF == ord('a'):
                cv2.circle(img, (1100, 250), 50, (233, 233, 10), -1)
                for i in range(len(buttonDisplay)):
                    if buttonDisplay[i].Click(1100, 250) == True:
                        break
            if cv2.waitKey(10) & 0xFF == ord('b'):
                cv2.circle(img, (1100, 350), 50, (233, 233, 10), -1)
                for i in range(len(buttonDisplay)):
                    if buttonDisplay[i].Click(1100, 350) == True:
                        break
            if cv2.waitKey(10) & 0xFF == ord('c'):
                cv2.circle(img, (1100, 450), 50, (233, 233, 10), -1)
                for i in range(len(buttonDisplay)):
                    if buttonDisplay[i].Click(1100, 450) == True:
                        break
            
            #filtering image
            bilateral = cv2.bilateralFilter(img, 3, 200, 200)
            cv2.imshow('Coursework 2', bilateral)    
            
            
            k = cv2.waitKey(20)
            if k == 27:  # press ESC to exit
                break

    #while loop break   
        else:
            break
    #closing window
    camera.release()
    cv2.destroyAllWindows()