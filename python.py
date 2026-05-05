import pygame
import math
import sys
import time
import datetime
import can


pygame.init()

WIDTH, HEIGHT = 1024,600
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

CENTER = (WIDTH/2, HEIGHT/2)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (60,60,60)


clock = pygame.time.Clock()

arcAngle = 24
centerWidth = 80
cwCeneter = True
cwRight = False
cwLeft = True


def draw_text(screen, text, size, color, center, isCentered, angle = 0):
    font = pygame.font.Font("./Hack-Regular.ttf", size)
    surface = font.render(str(text), True, color)

    surface = pygame.transform.rotate(surface, angle)

    if(isCentered):
        rect = surface.get_rect(center=center)
    else:
        rect = surface.get_rect(topleft=center)

    screen.blit(surface, rect)

def xOffsetTriangle(angle):
    return HEIGHT/2 * math.tan(math.radians(angle))
def centerLine(value,  minValue, maxValue):
    tempValue = value - minValue
    percentage = tempValue / (maxValue -minValue)

    degrees = 288 * percentage + 36
    radians = math.radians(degrees)

    outer = 310
    length = 80

    if(cwCeneter):
        radians = -radians
    
    x1 = int(outer*math.sin(radians) + WIDTH/2)
    y1 = int(outer*math.cos(radians) + HEIGHT/2)

    x2 = int((outer-length)*math.sin(radians) + WIDTH/2)
    y2 = int((outer-length)*math.cos(radians) + HEIGHT/2)

    pygame.draw.line(screen, WHITE, (x1,y1), (x2,y2), 6)

    draw_text(screen, value, 70, (255,255,255), (WIDTH/2, HEIGHT*0.9), True)
def centerGauge():
    pygame.draw.circle(screen, (20, 20, 20), (WIDTH/2, HEIGHT/2), HEIGHT/2 +20, centerWidth)

    pygame.draw.polygon(screen, (0,0,0,255), (CENTER, (WIDTH/2 - xOffsetTriangle(36), HEIGHT), (WIDTH/2 + xOffsetTriangle(36), HEIGHT)))

    centerMarkings(8,0,8000)
def centerMarkings(count, minValue, maxValue):
    for i in range (count + 1):

        tempValue = maxValue - minValue
        value = (tempValue/count) * i

        percentage = value / (maxValue -minValue)

        degrees = 288 * percentage + 36
        radians = math.radians(degrees)

        outer = 320
        textOffset = 30

        if(cwCeneter):
            radians = -radians

        x1 = int(outer*math.sin(radians) + WIDTH/2)
        y1 = int(outer*math.cos(radians) + HEIGHT/2)

        x2 = int((outer - centerWidth)*math.sin(radians) + WIDTH/2)
        y2 = int((outer - centerWidth)*math.cos(radians) + HEIGHT/2)

        x3 = int((outer - centerWidth - textOffset)*math.sin(radians) + WIDTH/2)
        y3 = int((outer - centerWidth - textOffset)*math.cos(radians) + HEIGHT/2)

        pygame.draw.line(screen, GRAY, (x1,y1), (x2,y2), 3)
        draw_text(screen, int(value/1000), 40, WHITE, (x3,y3), True)

def yOffsetTriangle(angle):
    return WIDTH/2 * math.tan(math.radians(angle))
def outerGauges():
    pygame.draw.circle(screen, (20,20,20), (WIDTH/2, HEIGHT/2), HEIGHT/2 +180, centerWidth)

    sideAngle = 9
    bottomAngle = 90 - sideAngle - arcAngle

    pygame.draw.polygon(screen, (0,0,0,255), (CENTER, (WIDTH, HEIGHT/2 - yOffsetTriangle(sideAngle)), (WIDTH, HEIGHT/2 + yOffsetTriangle(sideAngle)))) #r
    pygame.draw.polygon(screen, (0,0,0,255), (CENTER, (0, HEIGHT/2 - yOffsetTriangle(sideAngle)), (0, HEIGHT/2 + yOffsetTriangle(sideAngle)))) #l

    pygame.draw.polygon(screen, (0,0,0,255), (CENTER, (WIDTH/2 - xOffsetTriangle(bottomAngle), HEIGHT), (WIDTH/2 + xOffsetTriangle(bottomAngle), HEIGHT))) #b
    pygame.draw.polygon(screen, (0,0,0,255), (CENTER, (WIDTH/2 - xOffsetTriangle(bottomAngle), 0), (WIDTH/2 + xOffsetTriangle(bottomAngle), 0))) #b

    outerMarkings(arcAngle, sideAngle)
def outerMarkings(arcAngle, sideAngle):
    count = 8
    rs = True #right side, true if right side
    top = True #top or bottom, true if top
    innerLine = True #horisontally inner or outer lines, true if inner line

    value = 0

    textOffset = 25

    trMin = 65
    trMax = 105

    tlMin = 10
    tlMax = 15

    brMin = 0
    brMax = 40

    blMin = 0
    blMax = 100

    for i in range(count):
        # 0 top right, 1 bottom right, 2 top left, 3 bottom left
        match i:
            case 0:
                rs = True
                top = True
                innerLine = True
            case 1:
                rs = True
                top = False
                innerLine = True
            case 2:
                rs = False
                top = True
                innerLine = True
            case 3:
                rs = False
                top = False
                innerLine = True
            case 4:
                rs = True
                top = True
                innerLine = False
            case 5:
                rs = True
                top = False
                innerLine = False
            case 6:
                rs = False
                top = True
                innerLine = False
            case 7:
                rs = False
                top = False
                innerLine = False

        outer = HEIGHT/2 + 180

        degree = 90 - sideAngle

        textDegree = 0 

        if(rs and top):
            degree = degree + sideAngle * 2
            value = trMin
            if(not innerLine):
                degree = degree + arcAngle
                value = trMax
            textDegree = degree -90
        elif(rs and not top):
            degree = degree
            value = brMax
            if(not innerLine):
                degree = degree - arcAngle
                value = brMin
            textDegree = degree -90
        elif(not rs and top):
            degree = -degree - sideAngle * 2
            value = tlMin
            if(not innerLine):
                degree = degree - arcAngle
                value = tlMax
            textDegree = degree +90
        elif(not rs and not top):
            degree = -degree
            value = blMax
            if(not innerLine):
                degree = degree + arcAngle
                value = blMin
            textDegree = degree +90
        
        x1 = int(outer*math.sin(math.radians(degree)) + WIDTH/2)
        y1 = int(outer*math.cos(math.radians(degree)) + HEIGHT/2)

        x2 = int((outer - centerWidth)*math.sin(math.radians(degree)) + WIDTH/2)
        y2 = int((outer - centerWidth)*math.cos(math.radians(degree)) + HEIGHT/2)

        x3 = int((outer - centerWidth - textOffset)*math.sin(math.radians(degree)) + WIDTH/2)
        y3 = int((outer - centerWidth - textOffset)*math.cos(math.radians(degree)) + HEIGHT/2)

        pygame.draw.line(screen, GRAY, (x1,y1), (x2,y2), 3)
        draw_text(screen, value, 20, WHITE, (x3,y3), True, textDegree)

def trLine(value, minimum, maximum):

    outer = 480

    tempValue = value - minimum
    percentage = tempValue / (maximum -minimum)

    degrees = arcAngle * percentage + 90 + 9

    x1 = int((outer-10)*math.sin(math.radians(degrees)) + WIDTH/2)
    y1 = int((outer-10)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x2 = int((outer-10-centerWidth)*math.sin(math.radians(degrees)) + WIDTH/2)
    y2 = int((outer-10-centerWidth)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x3 = int((outer-centerWidth/2)*math.sin(math.radians(90 + 9/2)) + WIDTH/2)
    y3 = int((outer-centerWidth/2)*math.cos(math.radians(90 + 9/2)) + HEIGHT/2)

    x4 = int((outer - centerWidth - 40)*math.sin(math.radians(arcAngle * 0.5 + 90 + 9)) + WIDTH/2)
    y4 = int((outer - centerWidth - 40)*math.cos(math.radians(arcAngle * 0.5 + 90 + 9)) + HEIGHT/2)

    pygame.draw.line(screen, WHITE, (x1,y1), (x2,y2), 3)
    draw_text(screen, str(int(value)) + "°C", 30, WHITE, (x3,y3), True) 
    draw_text(screen, "WATER", 20, WHITE, (x4,y4), True, ((arcAngle * .5) + 9)) 
def brLine(value, minimum, maximum):

    outer = 480

    percentage = (value-minimum) / (maximum-minimum)

    degrees = (arcAngle * percentage) + 90 - 9 - arcAngle

    x1 = int((outer-10)*math.sin(math.radians(degrees)) + WIDTH/2)
    y1 = int((outer-10)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x2 = int((outer-10-centerWidth)*math.sin(math.radians(degrees)) + WIDTH/2)
    y2 = int((outer-10-centerWidth)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x3 = int((outer-centerWidth/2)*math.sin(math.radians(90 - 9/2)) + WIDTH/2)
    y3 = int((outer-centerWidth/2)*math.cos(math.radians(90 - 9/2)) + HEIGHT/2)

    x4 = int((outer - centerWidth - 40)*math.sin(math.radians((arcAngle * .5) + 90 - 9 - arcAngle)) + WIDTH/2)
    y4 = int((outer - centerWidth - 40)*math.cos(math.radians((arcAngle * .5) + 90 - 9 - arcAngle)) + HEIGHT/2)

    pygame.draw.line(screen, WHITE, (x1,y1), (x2,y2), 3)
    draw_text(screen, str(int(value)) + "°", 30, WHITE, (x3,y3), True)
    draw_text(screen, "ADV", 20, WHITE, (x4,y4), True , -((arcAngle * .5) + 9))
def tlLine(value, minimum, maximum):

    outer = 480

    tempValue = value - minimum
    percentage = tempValue / (maximum -minimum)

    degrees = -arcAngle * percentage - 90 - 9

    x1 = int((outer-10)*math.sin(math.radians(degrees)) + WIDTH/2)
    y1 = int((outer-10)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x2 = int((outer-10-centerWidth)*math.sin(math.radians(degrees)) + WIDTH/2)
    y2 = int((outer-10-centerWidth)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x3 = int((outer-centerWidth/2)*math.sin(math.radians(-90 - 9/2)) + WIDTH/2)
    y3 = int((outer-centerWidth/2)*math.cos(math.radians(-90 - 9/2)) + HEIGHT/2)

    x4 = int((outer - centerWidth - 25)*math.sin(math.radians((arcAngle * .5) - 90 - 9 - arcAngle)) + WIDTH/2)
    y4 = int((outer - centerWidth - 25)*math.cos(math.radians((arcAngle * .5) - 90 - 9 - arcAngle)) + HEIGHT/2)

    pygame.draw.line(screen, WHITE, (x1,y1), (x2,y2), 3)
    draw_text(screen, str(int(value)) + "V", 30, WHITE, (x3,y3), True)
    draw_text(screen, "V", 20, WHITE, (x4,y4), True , -((arcAngle * .5) + 9))
def blLine(value, minimum, maximum):

    outer = 480

    tempValue = value - minimum
    percentage = tempValue / (maximum -minimum)

    degrees = -arcAngle * percentage - 90 + 9 + arcAngle

    x1 = int((outer-10)*math.sin(math.radians(degrees)) + WIDTH/2)
    y1 = int((outer-10)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x2 = int((outer-10-centerWidth)*math.sin(math.radians(degrees)) + WIDTH/2)
    y2 = int((outer-10-centerWidth)*math.cos(math.radians(degrees)) + HEIGHT/2)

    x3 = int((outer-centerWidth/2)*math.sin(math.radians(-90 + 9/2)) + WIDTH/2)
    y3 = int((outer-centerWidth/2)*math.cos(math.radians(-90 + 9/2)) + HEIGHT/2)

    x4 = int((outer - centerWidth - 40)*math.sin(math.radians((arcAngle * .5) - 90 + 9)) + WIDTH/2)
    y4 = int((outer - centerWidth - 40)*math.cos(math.radians((arcAngle * .5) - 90 + 9)) + HEIGHT/2)

    pygame.draw.line(screen, WHITE, (x1,y1), (x2,y2), 3)
    draw_text(screen, str(int(value)) + "%", 30, WHITE, (x3,y3), True)
    draw_text(screen, "LOAD", 20, WHITE, (x4,y4), True, ((arcAngle * .5) + 9))

def middleNumbers(speed):

    draw_text(screen, int(speed), 100, WHITE, (WIDTH/2, HEIGHT/2 - 50), True)
    draw_text(screen, "KM/H", 20, WHITE, (WIDTH/2, HEIGHT/2 + 10), True)
    if(speed ==0):
        speed = 1
    minsPer100KM = 1/speed*100*60
    if(minsPer100KM/60 >= 999):
        draw_text(screen, ">999", 40, WHITE, (WIDTH/2, HEIGHT/2 + 50), True)
        draw_text(screen,  "H/100KM", 20, WHITE, (WIDTH/2, HEIGHT/2 + 20+40 + 20), True)
    elif(minsPer100KM > 120):
        draw_text(screen, str(round(minsPer100KM/60,1)), 40, WHITE, (WIDTH/2, HEIGHT/2 + 50), True)
        draw_text(screen,  "H/100KM", 20, WHITE, (WIDTH/2, HEIGHT/2 + 20+40 + 20), True)
    else:
        draw_text(screen, str(round(minsPer100KM,1)), 40, WHITE, (WIDTH/2, HEIGHT/2 + 50), True)
        draw_text(screen,  "Min/100KM", 20, WHITE, (WIDTH/2, HEIGHT/2 + 20+40 + 20), True)
def outsideText(tl, speed, rpm):

    if(rpm == 0 or speed == 0):
        gear = "N"
    else:
        ratio = rpm/speed
    
    g1r = 118
    g2r = 64
    g3r = 44
    g4r = 33
    g5r = 27 


    gear = "N"
    if(speed == 0):
        gear = "N"
    elif(ratio >= g1r - 5 and ratio <+ g1r + 5):
        gear = "1"
    elif(ratio >= g2r - 5 and ratio <+ g2r + 5):
        gear = "2"
    elif(ratio >= g3r - 5 and ratio <+ g3r + 5):
        gear = "3"
    elif(ratio >= g4r - 5 and ratio <+ g4r + 5):
        gear = "4"
    elif(ratio >= g5r - 5 and ratio <+ g5r + 5):
        gear = "5"


    time = datetime.datetime.now().strftime("%H:%M")

    draw_text(screen,time, 25, WHITE, ((WIDTH/2) + (HEIGHT/2) - (centerWidth/2), 30), True)

    draw_text(screen,str(int(tl))+ "°C", 25, WHITE, ((WIDTH/2) - (HEIGHT/2) + (centerWidth/2), 30), True)

    draw_text(screen,gear, 25, WHITE, ((WIDTH/2) + (HEIGHT/2) - (centerWidth/2), HEIGHT - 30), True)


REQ_ID = 0x7E0
RESP_ID = 0x7E8

can_bus = can.Bus(channel="can0", interface="socketcan")

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


i = 0
up = True
c = 85
cUp = True


while (True):
    screen.set_alpha(128)
    screen.fill(BLACK)

    outerGauges()

    trLine(getSingleByte(0x05)-40,65,105)#coolant
    brLine(getSingleByte(0x0E) /2 - 64,0,50)#advance

    tlLine(getTwoBytes(0x42) / 1000,10,15)#volts
    blLine(getSingleByte(0x04) * 100 / 255,0,100)#engine load

    sendRequest(0x0C)
    rawRpm = recvResponce(0x0C)
    if rawRpm and len(rawRpm) >= 2:
        rpmValue = ((rawRpm[0] << 8) | rawRpm[1]) / 4
    else:
        rpmValue = 0
    centerGauge()
    centerLine(int(rpmValue), 0, 8000)#rpm

    kmph = getSingleByte(0x0D)
    middleNumbers(kmph)#speed

    outsideText(getSingleByte(0x0F) - 40, kmph, rpmValue)#intake temp

    pygame.display.flip()
    clock.tick(20)
