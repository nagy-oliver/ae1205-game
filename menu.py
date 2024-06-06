import pygame as pg
import common as c

class Menu:
    # State of app
    mainState = 1
    
    # Local state of menu
    state = 0
    # 0 = main
    # 1 = weight selection
    # 2 = leaderboard
    # 3 = finished
    # 4 = manual

    buttonIndex = 0
    buttonCount = None

    playerName = None
    weightEntry = 0
    weights = []
    maxweight = None

    leaders = []
    with open("leaderboard.txt", "r") as fp:
        for i in fp:
            name, weight = i.split()
            leaders.append((name, int(weight)))
            
    
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
            if event in range(10) :
                self.weightEntry = self.weightEntry*10 + event
                if self.weightEntry >= 100:
                    self.buttonClick()
                      
    def buttonClick(self):
        # Main menu
        if self.state == 0:
            # "New Game" button
            if self.buttonIndex == 0:
                self.state = 1
            # "Leaderboard" button        
            elif self.buttonIndex == 1:
                self.state = 2 
            # "Manual" button
            elif self.buttonIndex == 2:
                self.state = 3         
            # "Quit" button        
            elif self.buttonIndex == 3:
                self.mainState = 0
        # Weight selection
        elif self.state == 1:
            self.weights.append(self.weightEntry)
            self.weightEntry = 0 
        # Leaderboard
        elif self.state == 2:
            pass   
        # Manual     
        elif self.state == 3:
            pass
                             
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
        # Number Input
        if len(self.weights) == 0: entryNum = "first"
        elif len(self.weights) == 1: entryNum ="second"
        elif len(self.weights) == 2: entryNum ="third"
        # Go to game
        elif len(self.weights) == 3: 
            self.mainState = 2
            return

        text1 = c.mainFont.render("Input your " + entryNum + " weight:", True, c.black, c.grey)
        text1Rect = text1.get_rect()
        text1Rect.center = (c.screenX/2, c.screenY/2 - 20)

        screen.blit(text1, text1Rect)

    def leaderboard(self, screen: pg.Surface):
        pass
    def finished(self, screen: pg.Surface):
        pass
    def manual(self, screen: pg.Surface):
        pass

    # Draw the corresponding menu based on state var
    def generate(self, screen: pg.Surface):
        if self.state == 0: 
            self.mainMenu(screen)
        elif self.state == 1:
            self.weightSelection(screen)
        elif self.state == 2:
            self.leaderboard(screen)
        elif self.state == 3:
            self.finished(screen)
        elif self.state == 4:
            self.manual(screen)
        
        return self.mainState