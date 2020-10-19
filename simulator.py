from planet import Planet
from vector import Vector
import json
import turtle
import random
import datetime
import matplotlib.pyplot as plt


fakeG = 10
realG = 6.673 * 10**(-11)
G = fakeG


energyLog = []

massOfEarth = 5.972 * 10**24
massOfSun = 1.989 * 10**30
massOfMoon = 7.35 * 10**22
distEarthMoon = 3.844 * 10**8
distSunEarth = 1.50 * 10**11
speedEarth_Sun = 3 * 10**4
speedMoon_Earth = 1.022 * 10**3

bodies1 = [
    Planet(name='Earth1', mass=1, position=[-100, 0, 0], velocity=[0, 0, 0]),
    Planet(name='Earth2', mass=60, position=[0, 0, 0], velocity=[0, 2, 0]),
    Planet(name='Earth3', mass=1, position=[100, -30, 0], velocity=[0, 0, 0])
]
bodies2 = [
    Planet(name='Earth1', mass=1,
           position=[0, 250, 0], velocity=[-6, -3, 0]),
    Planet(name='Earth2', mass=1000, position=[
           0, 0, 0], velocity=[0, 0, 0]),
    # Planet(name='Earth3', mass=1, position=[86.6, -50, 0], velocity=[0, 0, 0])
]
bodies2_1 = [
    Planet(name='Earth1', mass=1,
           position=[0, 250, 0], velocity=[-6.5, 0, 0]),
    Planet(name='Earth2', mass=1000, position=[
           0, 0, 0], velocity=[0, 0, 0]),
]
bodies2_2 = [
    Planet(name='Earth1', mass=1,
           position=[0, 250, 0], velocity=[0, 0, 0]),
    Planet(name='Earth2', mass=1000, position=[
           0, 0, 0], velocity=[0, 0, 0]),
]
bodies3 = [
    Planet(name='Earth1', mass=10,
           position=[-100, 100, 0], velocity=[1, 0, 0]),
    Planet(name='Earth2', mass=10, position=[
           100, 100, 0], velocity=[0, -1, 0]),
    Planet(name='Earth3', mass=10, position=[
           100, -100, 0], velocity=[-1, 0, 0]),
    Planet(name='Earth4', mass=10,
           position=[-100, -100, 0], velocity=[0, 1, 0])
]
bodies4 = [
    Planet(name='Earth1', mass=10,
           position=[-60, 100, 50], velocity=[1, 0, 0]),
    Planet(name='Earth2', mass=10, position=[
           100, 30, 0], velocity=[0, -1, 0]),
    Planet(name='Earth3', mass=10, position=[
           20, -100, -50], velocity=[-1, 0, 0]),
    Planet(name='Earth4', mass=10,
           position=[-100, -100, 100], velocity=[0, 1, 0])
]
bodies5 = [
    Planet(name='Earth1', mass=30,
           position=[0, 250, 0], velocity=[-6, -3, 0]),
    Planet(name='Earth2', mass=400, position=[
           0, 0, 0], velocity=[0, 0, 0]),
    Planet(name='Earth3', mass=50, position=[86.6, -50, 0], velocity=[-5, -7, 0])
]
sunEarthMoon = [
    Planet(name='Sun', mass=massOfSun,
           position=[0, 0, 0], velocity=[0, 0, 0]),
    Planet(name='Earth', mass=massOfEarth, position=[
           distSunEarth, 0, 0], velocity=[0, speedEarth_Sun, 0]),
    Planet(name='Moon', mass=massOfMoon, position=[
           distSunEarth+distEarthMoon, 0, 0], velocity=[0, speedEarth_Sun+speedMoon_Earth, 0]),
]


def findAcceleration(of, wrt, time):  # wrt = with respect to
    m = wrt.getMass()
    rVec = wrt.getPosition(time) - of.getPosition(time)
    rMag = rVec.norm()
    acc = (G*m*rVec)/(rMag**3)
    return acc

def calculateEnergy(bodies, time):
    kenetic = 0
    potential = 0
    for i in range(len(bodies)):
        # acc = Vector([0, 0, 0])
        for j in range(len(bodies)):
            if i != j:
                acc = findAcceleration(of=bodies[i],
                                        wrt=bodies[j], time=time)
                potential -= bodies[i].getMass() * acc.norm() * (bodies[i].getPosition() - bodies[j].getPosition()).norm()
                
        kenetic += 0.5 * bodies[i].getMass() *  bodies[i].getVelocity().norm()**2
    energyLog.append(kenetic+potential)
    return [kenetic, potential, kenetic+potential]

def simulateMotion(bodies, timeStep, timeRange, notifyProgEveryXSec=None):
    untilNotif = 0
    for time in range(round(timeRange/timeStep)):
        for i in range(len(bodies)):
            acc = Vector([0, 0, 0])
            for j in range(len(bodies)):
                if i != j:
                    acc += findAcceleration(of=bodies[i],
                                            wrt=bodies[j], time=time)
            pos = bodies[i].getPosition()
            vel = bodies[i].getVelocity()
            newPos = pos + vel * timeStep
            newVel = vel + acc * timeStep
            bodies[i].setPosition(newPos)
            bodies[i].setVelocity(newVel)
        if notifyProgEveryXSec:
            if untilNotif >= notifyProgEveryXSec or time == 0:
                # print(time*timeStep/timeRange, 'percent complete')
                untilNotif = 0
                
                print(calculateEnergy(bodies,-1))

        untilNotif += timeStep

def simulateSemiImplicitMotion(bodies, timeStep, timeRange, notifyProgEveryXSec=None):
    untilNotif = 0
    for time in range(round(timeRange/timeStep)):
        for i in range(len(bodies)):
            acc = Vector([0, 0, 0])
            for j in range(len(bodies)):
                if i != j:
                    acc += findAcceleration(of=bodies[i],
                                            wrt=bodies[j], time=time)
            pos = bodies[i].getPosition()
            vel = bodies[i].getVelocity()
            newVel = vel + acc * timeStep
            newPos = pos + newVel * timeStep
            bodies[i].setPosition(newPos)
            bodies[i].setVelocity(newVel)
        if notifyProgEveryXSec:
            if untilNotif >= notifyProgEveryXSec or time == 0:
                # print(time*timeStep/timeRange, 'percent complete')
                untilNotif = 0
                
                print(calculateEnergy(bodies,-1))

        untilNotif += timeStep

def simulateImprovedMotion(bodies, timeStep, timeRange, notifyProgEveryXSec=None):
    untilNotif = 0
    for time in range(round(timeRange/timeStep)):
        for i in range(len(bodies)):
            acc = Vector([0, 0, 0])
            for j in range(len(bodies)):
                if i != j:
                    acc += findAcceleration(of=bodies[i],
                                            wrt=bodies[j], time=time)
            pos = bodies[i].getPosition()
            vel = bodies[i].getVelocity()
            newPos = pos + vel * timeStep/2
            newVel = vel + acc * timeStep/2
            bodies[i].setPosition(newPos)
            bodies[i].setVelocity(newVel)
        for i in range(len(bodies)):
            acc = Vector([0, 0, 0])
            for j in range(len(bodies)):
                if i != j:
                    acc += findAcceleration(of=bodies[i],
                                            wrt=bodies[j], time=time)
            vel = bodies[i].getVelocity()
            bodies[i].pop()
            newPos = bodies[i].getPosition() + vel * timeStep
            newVel = bodies[i].getVelocity() + acc * timeStep
            bodies[i].setPosition(newPos)
            bodies[i].setVelocity(newVel)
        if notifyProgEveryXSec:
            if untilNotif >= notifyProgEveryXSec or time == 0:
                # print(time*timeStep/timeRange, 'percent complete')
                untilNotif = 0
                print(calculateEnergy(bodies,-1))

        untilNotif += timeStep


def drawPaths(bodies, turtles, skip):
    numTimeSteps = len(bodies[0].getHistory()['position'])
    colors = ["red", "green", "blue", "black", "purple", "pink"]

    for (index, turtle) in enumerate(turtles):
        color = colors[index]
        turtle.fillcolor(color)
        turtle.speed(10)
        turtle.pencolor(color)

    for time in range(0, numTimeSteps, skip):
        for (index, body) in enumerate(bodies):
            # print(body)
            if time == 0:
                turtles[index].up()
            # turtles[index].pensize(
            #     body.getHistory()['velocity'][time].norm()/8)
            turtles[index].goto(
                body.getHistory()['position'][time].toList()[0:2])
            if time == 0:
                turtles[index].down()

def downSampleList(listIn, every):
    out = []
    for i in range(0,len(listIn),every):
        out.append(listIn[i])
    return out

def plot3dpath(bodies, skip=1):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xpositions = []
    ypositions = []
    zpositions = []
    step = 5
    for i in bodies:
        xpositions.append([])
        ypositions.append([])
        zpositions.append([])
        history = i.getHistory()['position']
        for j in range(0, len(history), step):
            xpositions[-1].append(history[j].get(0))
            ypositions[-1].append(history[j].get(1))
            zpositions[-1].append(history[j].get(2))

    colors = ["red", "green", "blue", "pink"]

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    downSampleList
    for i in range(len(bodies)):
        ax.plot3D(downSampleList(xpositions[i],skip), downSampleList(ypositions[i],skip),
                   downSampleList(zpositions[i],skip), c=colors[i])

    plt.show()

def savePaths(bodies, filename=None):
    if not filename:
        filename = str(datetime.datetime.utcnow())+".json"

    output = []
    for body in bodies:
        output.append(body.getJsonSerialized())
    with open(filename, "w") as outfile:
        json.dump(output, outfile)

def loadPaths(filename):
    with open(filename, "r") as infile:
        data = json.load(infile)
    # print(data)
    bodies = []
    for i in data:
        body = Planet()
        body.loadSerialized(i)
        bodies.append(body)
    return bodies

def getBounds(bodies):
    minim = [0,0,0]
    maxim = [0,0,0]
    for body in bodies:
        for pos in body.getHistory()['position']:
            for index, i in enumerate(pos.toList()):
                if i > maxim[index]:
                    maxim[index] = i
                elif i < minim[index]:
                    minim[index] = i
    x_range = maxim[0]-minim[0]
    y_range = maxim[1]-minim[1]
    print(x_range,y_range)
    if y_range > x_range:
        maxim[0] = minim[0] + y_range
    else:
        maxim[1] = minim[1] + x_range
    minim.extend(maxim)
    return minim


if __name__ == "__main__":
    # bodies = loadPaths("bodies1|t=0.1|l=3000.json")
    bodies = bodies2_1
    simulateMotion(bodies, 1, 30000, 1)
    # simulateSemiImplicitMotion(bodies, 1, 30000, 1)
    # simulateImprovedMotion(bodies, 0.1, 1000, 5)
    # savePaths(bodies, "bodies1|t=0.1|l=3000.json")
    # print(bodies)

    # win = turtle.Screen()

    # # # win.setworldcoordinates(-1.5*distSunEarth, -1.5*distSunEarth,
    # # #                         1.5*distSunEarth, 1.5*distSunEarth)

    # # # win.setworldcoordinates(-0.5*distSunEarth, -1.3*distSunEarth,
    # # #                         0.5* distSunEarth, 1.3*distSunEarth)

    # # # win.setworldcoordinates(distSunEarth-5*distEarthMoon, -5*distEarthMoon,
    # # #                         distSunEarth+5*distEarthMoon, 5*distEarthMoon)

    # # # win.setworldcoordinates(distSunEarth-100*distEarthMoon, -20*distEarthMoon,
    # # #                         distSunEarth+2*distEarthMoon, 200*distEarthMoon)

    # # win.setworldcoordinates(-3000, -3000, 500, 500)

    # print(getBounds(bodies))
    # bounds = getBounds(bodies)

    # win.setworldcoordinates(bounds[0]-0.05*(bounds[3]-bounds[0]), bounds[1]-0.05*(bounds[4]-bounds[1]), bounds[3]+0.05*(bounds[3]-bounds[0]), bounds[4]+0.05*(bounds[4]-bounds[1]))

    # turtles = [turtle.Turtle() for body in bodies]

    # # # print(bodies[2].getHistory())

    # drawPaths(bodies, turtles, 50)

    # win.exitonclick()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # xpositions = []
    # ypositions = []
    # zpositions = []
    # step = 5
    # for i in bodies:
    #     xpositions.append([])
    #     ypositions.append([])
    #     zpositions.append([])
    #     history = i.getHistory()['position']
    #     for j in range(0, len(history), step):
    #         xpositions[-1].append(history[j].get(0))
    #         ypositions[-1].append(history[j].get(1))
    #         zpositions[-1].append(history[j].get(2))

    # colors = ["red", "green", "blue", "pink"]

    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')

    # for i in range(len(bodies)):
    #     ax.scatter(xpositions[i], ypositions[i],
    #                zpositions[i], c=colors[i], marker='o')
    print("len", len(energyLog))
    plt.plot(list(range(len(energyLog))),energyLog)
    plt.show()

    # plot3dpath(bodies, 12)
    # print(len(xpositions))
