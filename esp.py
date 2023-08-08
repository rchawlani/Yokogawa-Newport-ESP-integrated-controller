import serial
import time
class esp:
    def __init__(self, dev="COM4", b=921600,axis=3,reset=True, initpos = 0.0,useaxis=[]):
        self.dev = serial.Serial(dev,b)
        self.inuse = useaxis
        if(len(self.inuse)==0):
            self.inuse = [axis]
        self.defaxis = axis
        #self.dev.write(b"%dQM?\r"%self.defaxis)
        #time.sleep(.1)
        self.enable()
        time.sleep(1)
        self.setUnits(3)
        self.setSpeed(2)
        if(reset):
            for n in self.inuse:
                self.reset(n)
                r = self.check_errors()
                if(r!=0):
                    print("Error while setting up controller, error # %d"%r)
                if(initpos!=0):
                    self.setpos(initpos)
                    r = self.check_errors()
                    if(r!=0):
                        print("Error while setting up controller, error # %d"%r)
                        
    def reset(self,axis):
        self.dev.write(b"%dOR;%dWS1\r"%(axis,axis))
	
    def check_errors(self):
        self.dev.write(b"TE?\r")
        return float(self.dev.readline())

    def getpos(self,axis=None):
        a = self.defaxis
        if(axis and axis>0):
            a = axis
        self.dev.write(b"%dTP\r"%a)
        return float(self.dev.readline())
	
    def setpos(self,pos,axis=None):
        a = self.defaxis
        if(axis and axis>0):
            a = axis
        #print("setting to %f"%pos)
        self.dev.write(b"%dPA%.4f;%dWS1;%dTP\r"%(a,pos,a,a))
        return float(self.dev.readline())

    def position(self,pos=None,axis=None):
        if(isinstance(pos,(float,int))):
            self.setpos(pos,axis)
            self.getpos()
            self.setpos(pos,axis)
        return self.getpos(axis)
    def enable(self, axis=None):
        if (axis and axis>0):
            a = axis
        else:
            a = self.defaxis
        self.dev.write(b"%dMO\r"%(a))
    def close(self):
        self.dev.close()
        print('Driver Object has been closed')
    def QueryUnits(self, axis=None):
        a = self.defaxis
        if(axis and axis>0):
            a = axis
        self.dev.write(b"%dSN?\r"%(a))
        return float(self.dev.readline())          
    def setUnits(self, unit, axis=None):
        if (axis and axis>0):
            a = axis
        else:
            a = self.defaxis
        self.dev.write(b"%dSN%d\r"%(a,unit))
    def setSpeed(self, s, axis=None):
        if (axis and axis>0):
            a = axis
        else:
            a = self.defaxis
        self.dev.write(b"%dVA%d\r"%(a,s))
    def QuerySpeed(self, axis=None):
       a = self.defaxis
       if(axis and axis>0):
           a = axis
       self.dev.write(b"%dVA?\r"%(a))
       return float(self.dev.readline())     
'''ser = serial.Serial('COM4', 921600)
ser.close()'''
'''if not ser.isOpen():
    ser.open()'''
'''driver = esp()
time.sleep(1)
#driver.setUnits(3)
time.sleep(.2)
units = driver.QueryUnits()
print('units: ,',units)
speed = driver.QuerySpeed()
print('speed: ',speed)
curr_pos = driver.getpos()
print(curr_pos)
driver.setpos(.001)
curr_pos = driver.getpos()
print(curr_pos)
driver.close()'''
# Change units to microns, make this aclass and work in Jupyter
# In jupyter, sweep through values throughout range