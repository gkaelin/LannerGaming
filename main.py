import lannerpsp
import os
import time
import threading
import random

import music


#########################################################################
### Global variables                                                    #
#########################################################################

lcdManager = lannerpsp.LCM()

score = 0
dead = False
posPlayer = 0                                                                           # 0 = top, 1 = bottom

arrayPosTop = ['','','','','','','','','','','','','','','','','','','','','','']       # '' = void, '>' = player, '*' = wall
arrayPosDown = ['','','','','','','','','','','','','','','','','','','','','','']      # 0 = void, 1 = player, 2 = wall


#########################################################################
### Function                                                            #
#########################################################################

def refreshLCD(textUp, textDown):
    # Clear LCD
    lcdManager.clear()
    
    # Move cursor to line up
    lcdManager.set_cursor(1,1)
    
    # Write first line
    lcdManager.write(textUp)
    
    # Move cursor to line down
    lcdManager.set_cursor(2,1)
    
    # Write first line
    lcdManager.write(textDown)
    

def playMusic(idMusique):
    # Play music
    if(idMusique == 0):
        # Welcome music
        music.playMortalKombat()
        
    if(idMusique == 1):
        # Musique in game
        while(1==1):
            music.playNyanMusic()
            
            # Check if player dead
            if(dead == True):
                break
                
    if(idMusique == 2):
        # Welcome music
        music.playPacman()
                
                
            
def inputControl():
    while(1==1):
        numberButtonPressed = lcdManager.get_keys_status()
        
        if(numberButtonPressed == 8):
            # Left button pressed
            # Move up
            posPlayer = 0
            
        elif(numberButtonPressed == 1):
            # Right button pressed
            # Move down
            posPlayer = 1
            
        else:
            # No button pressed
            voidData = 0
            
        # Pause process until next process
        time.sleep(0.1)
        
        
        
def convertArrayToText(array):
    outputText = ''

    for cel in array:
        if(cel == ''):
            outputText = outputText + ' '
            
        else:
            outputText = outputText + cel
            
            
    return outputText
        
        
        
def mainContentGame():
    newGame = True
    counterBeforeDecreaseTime = 0
    timeBeforeRefresh = 800
    counterBeforeCreatingWall = 0
    
    # Start thread for input control
    threadInput = threading.Thread(target=inputControl, args=())
    threadInput.start()

    while(1==1):
        # Set by default, will be decrease during game
        if(newGame == True):
            # Creating new game
            arrayPosTop = ['>','','','','','','','','','','','','','','','','','','','','','']
            arrayPosDown = ['','','','','','','','','','','','','','','','','','','','','','']
            
            # Convert array to text
            textTop = convertArrayToText(arrayPosTop)
            textDown = convertArrayToText(arrayPosDown)
            
            # Display text on LCD
            refreshLCD(textTop, textDown)
            
        else:
            # Move player based on variables
            if(posPlayer == 0):
                arrayPosTop[0] = '>'
                arrayPosDown[0] = ''
                
            else:
                arrayPosTop[0] = ''
                arrayPosDown[0] = '>'
            
            # Move wall to left and check if player dead
            for x in xrange(0, 20, 1):
                if(x == 0):
                    # First block, check if player dead
                    if(arrayPosTop[0] == '>' and arrayPosTop[1] == '*'):
                        # Player dead
                        dead = True
                        
                    if(arrayPosDown[0] == '>' and arrayPosDown[1] == '*'):
                        # Player dead
                        dead = True
                        
                
                # Move to left
                arrayPosTop[x] = arrayPosTop[x+1]
                arrayPosDown[x] = arrayPosDown[x+1]
                
            # Clear last cell
            arrayPosTop[21] = ''
            arrayPosDown[21] = ''
            
            
            # Generate new wall if needed
            if(counterBeforeCreatingWall > 2):
                # Create new wall
                numberObtained = random.randint(1,100)
                
                if(numberObtained > 50):
                    # Wall on top line
                    arrayPosTop[21] = '*'
                    arrayPosDown[21] = ''
                
                else:
                    # Wall on top line
                    arrayPosTop[21] = ''
                    arrayPosDown[21] = '*'
                
            else:
                # Increase counter
                counterBeforeCreatingWall = counterBeforeCreatingWall + 1
            
            # Break if player dead
            if(dead == True):
                break;
            
            # Convert array to text
            textTop = convertArrayToText(arrayPosTop)
            textDown = convertArrayToText(arrayPosDown)
            
            # Display text on LCD
            refreshLCD(textTop, textDown)
            
            # Decrease time before refresh, and increase score
            score = score + 1
            
            if(counterBeforeDecreaseTime > 9):
                timeBeforeRefresh = timeBeforeRefresh - 1
                counterBeforeDecreaseTime = 0
            else:
                counterBeforeDecreaseTime = counterBeforeDecreaseTime + 1
            
            # Sleep until next refresh
            time.sleep(timeBeforeRefresh)
        

        
        
    
#########################################################################
### Main execution                                                      #
#########################################################################


# Starting soft
threadMusicStart = threading.Thread(target=playMusic, args=(0))
threadMusicStart.start()
refreshLCD('Welcome', 'to')
time.sleep(2)
refreshLCD('Lanner', 'Gaming')
time.sleep(2)
refreshLCD('The next generation', 'of gaming')
time.sleep(2)
threadMusicStart.join()

while(1==1):
    # Start new game
    threadMusic = threading.Thread(target=playMusic, args=(1))
    threadMusic.start()

    threadGame = threading.Thread(target=mainContentGame, args=())
    threadMusic.start()
    
    # Wait the thread to be done
    threadGame.join()
    threadMusic.join()

    # Player dead, new loop
    threadGameDead = threading.Thread(target=playMusic, args=(2))
    threadGameDead.start()
    refreshLCD('You lost', 'the game')
    time.sleep(3)
    refreshLCD('Your score is', str(score))
    time.sleep(3)
    threadGameDead.join()