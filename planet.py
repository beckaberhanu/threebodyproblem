from vector import Vector


class Planet:
    def __init__(self, name="", mass=0, position=[0,0,0], velocity=[0,0,0]):
        self.name = name
        self.mass = mass
        self.positions = [Vector(position)]
        self.velocities = [Vector(velocity)]

    def getName(self):
        return self.name
    def getMass(self):
        return self.mass

    def getPosition(self, time=-1):
        return self.positions[time]

    def getVelocity(self, time=-1):
        return self.velocities[time]

    def getHistory(self):
        history = {
            'position': self.positions,
            'velocity': self.velocities
        }
        return history
    
    def getJsonSerialized(self):
        positions = [i.toList() for i in self.positions]
        velocities = [i.toList() for i in self.velocities]
        return {
            'name':self.name,
            'mass':self.mass,
            'history':{
                'position': positions,
                'velocity': velocities
            }
        }
    
    def loadSerialized(self, serialized):
        self.name = serialized['name']
        self.mass = serialized['mass']
        self.positions = [Vector(i) for i in serialized['history']['position']]
        self.velocities = [Vector(i) for i in serialized['history']['velocity']]

    def setPosition(self, position):
        self.positions.append(position)

    def setVelocity(self, velocity):
        self.velocities.append(velocity)

    def pop(self):
        self.velocities.pop()
        self.positions.pop()

    def __str__(self):
        return '{name} | mass:{mass} | position:{position} | velocity:{velocity}'.format(name=self.name, mass=self.mass, position=self.positions[-1], velocity=self.velocities[-1])


def main():
    m1 = 5
    pos1 = (2.4, 4.5, 4)
    vel1 = (10, 8, 4)
    name1 = 'earth'
    p1 = Planet(name1, m1, pos1, vel1)
    print(p1)


if __name__ == "__main__":
    main()
