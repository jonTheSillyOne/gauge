import pygame
import sys
import can
import time

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Gauge display")
pygame.mouse.set_visible(False)

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

class Gauge:

    #def __init__(self, x, y, min, max, redline, blueline, color):
    #    self.x = x
     #   self.y = y
      #  self.min = min
       # self.max = max
        #self.redline = redline
         #self.blueline = blueline
          #self.color = color

    color = (0,200,0)
    redlineColor = (200,0,0)
    bluelineColor = (0,0,200)
    barColor = (50,50,50)

    blueline = 0
    redline = 0

    redlinePercent = 0
    bluelinePercent = 0

    def __init__(self, xoffset, yoffset, height, width, min, max,name, padding):
        self.xpos = xoffset
        self.ypos = yoffset
        self.height = height
        self.width = width
        self.min = min
        self.max = max

        self.name = name
        self.padding = padding

        self.markings = [-1]



    def warningLimits(self, redline,blueline, redlineColor = (200,0,0), bluelineColor = (0,0,200)):
        self.redlineColor = redlineColor
        self.bluelineColor = bluelineColor

        self.redline = redline
        self.blueline = blueline

        if(redline >= self.min and redline <= self.max):
            tempMin = self.min - self.max
            tempValue = redline - self.max

            self.redlinePercent = tempValue / tempMin
        elif(redline > self.max):
            self.redlinePercent = 1
        elif(redline < self.min):
            self.redlinePercent = 0

        if(redline < 1):
            self.redlinePercent = redline


        if(blueline >= self.min and blueline <= self.max):
            tempMax = self.max - self.min
            tempValue = blueline - self.min

            self.bluelinePercent = tempValue / tempMax
        elif(blueline > self.max):
            self.bluelinePercent = 1
        elif(blueline < self.min):
            self.bluelinePercent = 0

        if(blueline < 1):
            self.bluelinePercent = blueline

    def update(self, value, decimalPlace = 0 ):


        if(value >= self.min and value <= self.max):
            tempMax = self.max - self.min
            tempValue = value - self.min

            self.percent = tempValue / tempMax
        elif(value > self.max):
            self.percent = 1
        elif(value < self.min):
            self.percent = 0

        if decimalPlace == 0:
            self.value = int(round(value))
        else:
            self.value = round(value, decimalPlace)

    def draw(self, screen):
        sizeDifference = 10
        gaugeHeight = HEIGHT * self.height - (self.padding * 2)
        gaugeHeight = int(gaugeHeight * self.percent)

        redlineHeight = HEIGHT * self.height - (self.padding * 2)
        redlineHeight = int(redlineHeight * self.redlinePercent)


        bluelineHeight = HEIGHT * self.height - (self.padding * 2)
        bluelineHeight = int(bluelineHeight * self.bluelinePercent)

        if(self.markings[0] != -1):
            xPos = int(self.xpos + (self.padding / 2))
            xPosValue = int(self.xpos + WIDTH * (self.width / 2) - (self.padding/2))
        else:
            xPos = int(self.xpos+ self.padding)
            xPosValue = int(self.xpos + WIDTH * self.width / 2)


        #background
        pygame.draw.rect(screen, self.color, (xPos, self.ypos + self.padding , int(WIDTH * self.width) - (self.padding * 2), int(HEIGHT * self.height) - self.padding *2))

        #redline
        pygame.draw.rect(screen, self.redlineColor , (xPos, self.ypos + self.padding, int(WIDTH * self.width) - (self.padding * 2), redlineHeight))

        #blueline
        pygame.draw.rect(screen, self.bluelineColor, (xPos, self.ypos + self.padding - bluelineHeight + int(HEIGHT * self.height) - self.padding *2, int(WIDTH * self.width) - (self.padding * 2), bluelineHeight))

        #bar
        pygame.draw.rect(screen, self.barColor, (xPos + sizeDifference, self.ypos + self.padding - gaugeHeight + int(HEIGHT * self.height) - self.padding *2, int(WIDTH * self.width) - (self.padding * 2) - (2 * sizeDifference), gaugeHeight))

        #draw value
        draw_text(screen, str(self.value), int(self.padding* (4/5)) , (255,255,255), (xPosValue, self.ypos + (self.padding / 2)), True)

        #draw name
        draw_text(screen, self.name, int(self.padding* (4/6)) , (255,255,255), (xPosValue, self.ypos - (self.padding / 2) + (HEIGHT * self.height)), True)


        if(self.markings[0] != -1):
            for value in self.markings:

                percent = (value - self.min) / (self.max - self.min)

                percent = 1 -percent

                font = pygame.font.Font("./Hack-Regular.ttf", 20)



                draw_text(screen, value, 20, (255,255,255), (self.xpos + int((WIDTH * self.width) - (self.padding*1.5)), self.ypos - (font.get_height()/2) + int((HEIGHT * self.height - (self.padding * 2)) * percent) + self.padding), False)





    def markingsAmount(self,amount):

        self.markings= []

        bottom = self.max - self.min

        i = 0

        while(i <= amount):
            self.markings.append(int((bottom * (i/amount)) + self.min))
            i = i +1


    #def markingsSpecific(self, one, two, three, four, five, six, seven, eight, nine, ten):



    def getwidth(self):
        return (WIDTH * self.width) + self.xpos

    def getheight(self):
        return (HEIGHT * self.height) + self.ypos



def draw_text(screen, text, size, color, center, isCentered):
    font = pygame.font.Font("./Hack-Regular.ttf", size)
    surface = font.render(str(text), True, color)
    if(isCentered):
        rect = surface.get_rect(center=center)
    else:
        rect = surface.get_rect(topleft=center)

    screen.blit(surface, rect)

def getSingleByte(pid):
    sendRequest(pid)
    data = recvResponce(pid)
    return data[0] if data else 0
    if data:
        return data[0]
    else:
        return 0

def getTwoBytes(pid):
    sendRequest(pid)
    data = recvResponce(pid)
    if data and len(data) >= 2:
        return (data[0] << 8) | data[1]
    return 0

padding = 40;

#rpm = Gauge(100, 50, 0, 6000, 5000, 0 , (125,125,125))
rpm = Gauge(0,0, 1, 1/6, 0, 8000,"RPM",padding)
rpm.warningLimits(6400, 500)
rpm.markingsAmount(8)

speed = Gauge(rpm.getwidth(), 0, 1 ,1/6, 0, 150, "km/h" , padding)
speed.warningLimits(140,0)
speed.markingsAmount(15)

engine = Gauge(speed.getwidth(), 0 , 1, 1/6,  0, 100, "Load", padding)
engine.markingsAmount(10)

throttle = Gauge(engine.getwidth(), 0 , 1, 1/6, 0, 100, "Throttle", padding)
throttle.markingsAmount(10)

#maf = Gauge(throttle.getwidth(), 0, 1, 1/6, 0, 400, "g/s", 30)
#maf.markingsAmount(8)

#fuel = Gauge(advance.getwidth(), 0 , 1, 1/6,  0, 100, "Gas", 30)
#fuel.markingsAmount(10)

battery = Gauge(throttle.getwidth(), 0 , 1/2 , 1/6,  5, 20, "V", padding)
battery.warningLimits(15, 10)
battery.markingsAmount(3)

advance = Gauge(throttle.getwidth(), battery.getheight() , 1/2 ,1/6,  -50, 50, "advance", padding)
advance.markingsAmount(8)

temp = Gauge(battery.getwidth(), 0 , 1/2, 1/6, 75, 115, "Coolant", padding)
temp.warningLimits(105, 85)
temp.markingsAmount(4)


airTemp = Gauge(battery.getwidth(), temp.getheight() , 1/2, 1/6, 0, 40, "Intake", padding)
airTemp.markingsAmount(4)





REQ_ID = 0x7E0
RESP_ID = 0x7E8

can_bus = can.Bus(channel="can0", interface="socketcan")

def sendRequest(pid):
    msg = can.Message(
        arbitration_id=REQ_ID,
        is_extended_id=False,
        data=[0x02, 0x01, pid, 0, 0, 0, 0, 0]
    )
    can_bus.send(msg)

def recvResponce(pid, timeout=0.2):
    start = time.time()
    while time.time() - start < timeout:
        msg = can_bus.recv(timeout=0.05)
        if msg and msg.arbitration_id == RESP_ID:
            data = msg.data
            if len(data) >= 3 and data[1] == 0x41 and data[2] == pid:
                return data[3:]
    return None


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    airTemp.update(getSingleByte(0x0F) - 40)
    airTemp.draw(screen)

    throttle.update(getSingleByte(0x11) * 100 / 255, 2)
    throttle.draw(screen)

    advance.update(getSingleByte(0x0E) /2 - 64, 2)
    advance.draw(screen)

    #fuel.update((getSingleByte(0x2F) * 100 / 255), 2)
    #fuel.draw(screen)

    battery.update(getTwoBytes(0x42) / 1000, 2)
    battery.draw(screen)

    engine.update(getSingleByte(0x04) * 100 / 255)
    engine.draw(screen)

    sendRequest(0x0C)
    rawRpm = recvResponce(0x0C)
    if rawRpm and len(rawRpm) >= 2:
        rpmValue = ((rawRpm[0] << 8) | rawRpm[1]) / 4
    else:
        rpmValue = 0
    rpm.update(rpmValue, 0)
    rpm.draw(screen)

    speed.update(getSingleByte(0x0D))
    speed.draw(screen)

    temp.update(getSingleByte(0x05)-40)
    temp.draw(screen)

    #data = recvResponce(0x10)
    #f data and len(data) >= 2:
    #    maf_val = ((data[0] << 8) | data[1]) / 100
    #else:
    #    maf_val = 0
    #maf.update(maf_val, 0)
    #maf.draw(screen)


    pygame.display.flip()
    clock.tick(15)
