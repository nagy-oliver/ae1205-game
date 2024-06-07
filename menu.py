import pygame as pg
import common as c
import time

class Menu:
    # State of app
    mainState = 1
    
    # Local state of menu
    state = 4
    # 0 = main
    # 1 = weight selection
    # 2 = finished
    # 3 = leaderboard
    # 4 = manual

    buttonIndex = 0
    buttonCount = None

    playerName = ""
    weightEntry = 0
    weights = []
    maxWeight = 0
    
    dt = None
    waitTime = 1

    leaders = []
    with open("leaderboard.txt", "r") as fp:
        for i in fp:
            name, weight = i.split()
            leaders.append((name, int(weight)))
            
    # Load manual
    manualImage = pg.image.load("assets/MANUAL.png")
    manualImage = pg.transform.scale(manualImage, (450, 450))
    manualRect = manualImage.get_rect()            
    
    def buttonColor(self, reqIndex):
        if reqIndex == self.buttonIndex:
            color = c.red
        else:
            color = None
        return color

    def eventHandler(self, events):
        # Menu moving
        if pg.K_UP in events:
            self.buttonIndex = (self.buttonIndex - 1) % (self.buttonCount)
        if pg.K_DOWN in events:
            self.buttonIndex = (self.buttonIndex + 1) % (self.buttonCount)
        # Choice accept
        if pg.K_RETURN in events:
            self.buttonClick()
        for event in events:
            if event in range(10) and self.state == 1 :
                self.weightEntry = self.weightEntry*10 + event
                if self.weightEntry >= 100:
                    self.buttonClick()
            elif isinstance(event, str) and self.state == 2:
                self.playerName += event
                      
    def buttonClick(self):
        # Main menu
        if self.state == 0:
            # "New Game" button
            if self.buttonIndex == 0:
                self.state = 1
                self.playerName = ""
            # "Leaderboard" button        
            elif self.buttonIndex == 1:
                self.state = 3 
            # "Manual" button
            elif self.buttonIndex == 2:
                self.state = 4         
            # "Quit" button        
            elif self.buttonIndex == 3:
                self.mainState = 0
        # Weight selection
        elif self.state == 1:
            self.weights.append(self.weightEntry)
            self.weightEntry = 0
            
        # Finished
        elif self.state == 2:
            for index, i in enumerate(self.leaders):
                if self.maxWeight > i[1]:
                    self.leaders.insert(index, (self.playerName, self.maxWeight))
                    break
            with open("leaderboard.txt", "w") as fp:
                fp.writelines([f"{i[0]}\t{i[1]}\n" for i in self.leaders])
            self.weights = []
            self.state = 3
        # Leaderboard     
        elif self.state == 3:
            self.state = 0
        # Manual
        elif self.state == 4:
            self.state = 0
                             
    def mainMenu(self, screen: pg.Surface):
        self.buttonCount = 4
        # New Game Button
        but1 = c.mainFont.render("New Game", True, c.black, self.buttonColor(0))
        but1Rect = but1.get_rect()
        but1Rect.center = (c.screenX/2, c.screenY/2 - 80)

        screen.blit(but1, but1Rect)

        # Leaderboard Button
        but2 = c.mainFont.render("Leaderboard", True, c.black, self.buttonColor(1))
        but2Rect = but2.get_rect()
        but2Rect.center = (c.screenX/2, c.screenY/2 - 20)

        screen.blit(but2, but2Rect)

        # Manual Button
        but3 = c.mainFont.render("Manual", True, c.black, self.buttonColor(2))
        but3Rect = but3.get_rect()
        but3Rect.center = (c.screenX/2, c.screenY/2 + 40)

        screen.blit(but3, but3Rect)

        # Quit Button
        but4 = c.mainFont.render("Quit Game", True, c.black, self.buttonColor(3))
        but4Rect = but4.get_rect()
        but4Rect.center = (c.screenX/2, c.screenY/2 + 100)

        screen.blit(but4, but4Rect)

    def weightSelection(self, screen: pg.Surface):
        #Go to game when having 3 weights
        
        
        #Weight selection title
        text1 = c.titleFont.render("Weight\nSelection", True, c.black, c.grey)
        text1Rect = text1.get_rect()
        text1Rect.center = (c.screenX/2, 50)
        screen.blit(text1, text1Rect)
        
        #Attempt titles
        for i in range(3):
            textWeightI = c.mainFont.render(f"Attempt {i+1}", True, c.black, c.red if len(self.weights) == i else c.grey)
            textWeightIRect = textWeightI.get_rect()
            textWeightIRect.center = (170, c.screenY/2 - 80 + i*80)
            screen.blit(textWeightI, textWeightIRect)
            
            #showing the inputed weight
            if len(self.weights) == i:
                chosenWeighttextI = self.weightEntry
            elif len(self.weights) < i:
                chosenWeighttextI = 0
            else:
                chosenWeighttextI = self.weights[i]
                        
            chosenWeightI = c.mainFont.render(str(chosenWeighttextI), True, c.black, c.grey)
            chosenWeightIRect = chosenWeightI.get_rect()
            chosenWeightIRect.center = (c.screenX - 170, c.screenY/2 - 80 + i*80)
            screen.blit(chosenWeightI, chosenWeightIRect)
        
        if len(self.weights) == 3:
            self.waitTime -= self.dt
            if self.waitTime <= 0:
                self.waiTime = 1
                self.mainState = 2
            return


    def finished(self, screen: pg.Surface):
        #Finished text
        text2 = c.mainFont.render("Enter your name and pres ENTER: ", True, c.black, c.grey)
        text2Rect = text2.get_rect()
        text2Rect.center = (c.screenX/2, c.screenY/2 - 20)

        screen.blit(text2, text2Rect)

        #Enter player name
        playerNameText = c.mainFont.render(self.playerName, True, c.black, c.grey)
        playerNameTextRect = playerNameText.get_rect()
        playerNameTextRect.center = (c.screenX/2, c.screenY/2 - 20)

        screen.blit(playerNameText, playerNameTextRect)
        
    def leaderboard(self, screen: pg.Surface):
        pg.draw.rect(screen, c.grey, pg.Rect(50, 25, 450, 450))

        textLeader = c.mainFont.render("NAME      WEIGHT", True, c.black)
        textLeaderRect = textLeader.get_rect()
        textLeaderRect.center = (c.screenX/2, 50)

        screen.blit(textLeader, textLeaderRect)
        
        for i in range(len(self.leaders[:8])):
            textLeaderName = c.mainFont.render(self.leaders[i][0][:10], True, c.black)
            textLeaderNameRect = textLeaderName.get_rect()
            textLeaderNameRect.topleft = (70, 70 + i*50)
            textLeaderScore = c.mainFont.render(str(self.leaders[i][1]), True, c.black)
            textLeaderScoreRect = textLeaderScore.get_rect()
            textLeaderScoreRect.topright = (450, 70 + i*50)
            
            screen.blit(textLeaderScore, textLeaderScoreRect)
            screen.blit(textLeaderName, textLeaderNameRect)

    def manual(self, screen: pg.Surface):
        # Manual image
        self.manualRect.center = (c.screenX/2, c.screenY/2)
        screen.blit(self.manualImage, self.manualRect)

    # Draw the corresponding menu based on state var
    def generate(self, screen: pg.Surface, dt):
        self.dt = dt
        
        if self.state == 0: 
            self.mainMenu(screen)
        elif self.state == 1:
            self.weightSelection(screen)
        elif self.state == 2:
            self.finished(screen)
        elif self.state == 3:
            self.leaderboard(screen)
        elif self.state == 4:
            self.manual(screen)
        
        return self.mainState