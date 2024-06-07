import pygame as pg
import common as c

class Game:
    state = 0
    # 0 = playing
    # 1 = attempt successful
    # 2 = attempt failed
    
    # Game settings variables
    weights = []
    attempt = 0
    maxWeight = 0

    # Difficulty settings
    difficulties = []
    k = 4

    # Clicking variables
    score = 0
    clicks = 0
    prevclicks = 0 
    clickrate = 0   
    
    # Clickrate refresh variables
    refreshtime = 1
    t = 0
    dt = None

    # End game wait
    waitTime = 1
    attemptTime = 30

    # Character images
    posList = []
    for i in range(4):
        posList.append(pg.transform.scale(pg.image.load(f"assets/{i}.png"), (500, 500)))

    # Progress bar
    progress = pg.transform.scale(pg.image.load("assets/BAR.png"), (50, 500))
    progressRect = progress.get_rect()
    progressRect.center = (25, c.screenY/2)

    # Attempt Counter
    textAttempt = c.mainFont.render(f"Attempt {attempt + 1}", True, c.white)
    textAttemptRect = textAttempt.get_rect()
    textAttemptRect.center = (c.screenX/2, c.screenY/4)


    def __init__(self, weights, dt):
        self.weights = weights
        for weight in weights:
            self.difficulties.append(weight/20)

        self.dt = dt
    
    # Move to next attempt
    def restart(self):
        self.attempt += 1
        self.score = 0
        self.clicks = 0
        self.clickrate = 0
        self.prevclicks = 0
        self.t = 0
        self.waitTime = 1
        self.attemptTime = 30
        # End game after third attempt
        if self.attempt == 3:
            self.attempt = 0
            return 1
        return 2

    def playing(self, events):
        # Registering of clicks
        for event in events:
            if event == pg.K_SPACE:
                self.clicks += 1
            # Development tools
            # elif event == pg.K_COMMA:
            #     self.score = 100
        
        # Clickrate counter, round timer
        self.t += self.dt
        if self.t > self.refreshtime:
            self.t = 0
            curclicks = self.clicks - self.prevclicks
            self.prevclicks = self.clicks
            self.clickrate = curclicks/self.refreshtime
            # Change to game over if time runs out
            self.attemptTime -= self.refreshtime
            if self.attemptTime <= 0:
                self.state = 2
                return
        # Score counter
        if self.score < 100:
            if self.clickrate >= self.difficulties[self.attempt]:
                self.score = self.score + (self.clickrate-self.difficulties[self.attempt]) * self.k * self.dt
            elif self.clickrate < self.difficulties[self.attempt] and self.score > 0:
                self.score = self.score - 10*self.dt
            else:
                self.score = 0
        else:
            self.score = 100
            self.state = 1
    
    def successful(self, screen: pg.Surface):
        #Text after attempt success
        self.endText = "Attempt succesful!"
        textWin = c.mainFont.render(self.endText, True, c.white)
        textWinRect = textWin.get_rect()
        textWinRect.center = (c.screenX/2+25, c.screenY/4)
        screen.blit(textWin, textWinRect)

        #Adjusting highest weight
        if self.weights[self.attempt] > self.maxWeight: self.maxWeight = self.weights[self.attempt]
        
        #End game wait time
        if self.waitTime > 0: 
            self.waitTime -= self.dt
        else:
            self.state = 0
            return self.restart()
        
    def failed(self, screen: pg.Surface):
        #Text after attempt failure
        self.endText = "Attempt failed"
        textLoss = c.mainFont.render(self.endText, True, c.white)
        textLossRect = textLoss.get_rect()
        textLossRect.center = (c.screenX/2+25, c.screenY/4)
        screen.blit(textLoss, textLossRect)

        #End game wait time
        if self.waitTime > 0: 
            self.waitTime -= self.dt
        else:
            self.state = 0
            return self.restart()

    def generate(self, screen: pg.Surface, events):
        if self.state == 0: self.playing(events)
        elif self.state == 1: 
            if self.successful(screen) == 1:
                return 1
        elif self.state == 2:
            if self.failed(screen) == 1:
                return 1

        # Draw position
        if self.score < 33:
            pos = self.posList[0]
        elif self.score == 33:
            pos = self.posList[0] #OTHER MECHANICS MAY BE ADDED
        elif 66 > self.score > 33:
            pos = self.posList[1]
        elif self.score == 66:   
            pos = self.posList[1] #OTHER MECHANICS MAY BE ADDED
        elif 100 > self.score > 66:
            pos = self.posList[2]
        # Winning state 
        elif self.score >= 100:
            pos = self.posList[3]
            
        #Progress bar pixelation
        def myround(x, base=5):
            return base * (x//base)
            
        #Progress bar drawing
        height = myround(5*self.score)
        pg.draw.rect(screen, c.red, pg.Rect(0, abs(500 - height), 50, height))
        screen.blit(self.progress, self.progressRect)
        # Attempt counter render
        textAttempt = c.mainFont.render(f"Attempt {self.attempt + 1}: {self.weights[self.attempt]}kg", True, c.black)
        textAttemptRect = textAttempt.get_rect()
        textAttemptRect.center = (c.screenX/2+25, c.screenY - 20)
        screen.blit(textAttempt, textAttemptRect)    
        # Attempt time render
        if self.state == 0: 
            timeText = c.mainFont.render(str(self.attemptTime), True, c.black, c.grey if self.attemptTime > 5 else c.red)
            timeTextRect = timeText.get_rect()
            timeTextRect.topright = (c.screenX, 0)
            screen.blit(timeText, timeTextRect)
        #Character drawing
        posrect = pos.get_rect()
        posrect.centerx = c.screenX/2+25
        posrect.centery = c.screenY/2
        screen.blit(pos, posrect)
        
        return 2