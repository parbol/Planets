from tkinter import *
import numpy as np
import math
from optparse import OptionParser
import time


##################################################################################################
##################################################################################################
class Planet:

    def __init__(self, x, v, m, color, radio):

        p = orig2D + x[0]*ux + x[1]*uy + x[2]*uz
        self.object = canvas.create_oval(p[0] - radio, p[1] - radio, p[0] + radio, p[1] + radio, fill=color)
        self.x = x
        self.v = v
        self.m = m
        self.color = color
        self.lastDrawnPosition = self.x

    def updateDynamics(self, DeltaT, F):

        a = 1.0/self.m * F
        xinc = self.v * DeltaT
        self.x = self.x + xinc
        self.v = self.v + a * DeltaT

    def Draw(self):

        vectorMove = self.x - self.lastDrawnPosition
        p = vectorMove[0]*ux + vectorMove[1]*uy + vectorMove[2]*uz
        canvas.move(self.object, p[0], p[1])
        p2 = orig2D + self.x[0]*ux + self.x[1]*uy + self.x[2]*uz
        canvas.create_line(p2[0], p2[1], p2[0]+1, p2[1], fill=self.color)
        self.lastDrawnPosition = self.x

##################################################################################################
##################################################################################################


##################################################################################################
########################################### Methods ##############################################
##################################################################################################
def drawAxis(canvas, gui, orig2D, max2D):

    canvas.create_line(orig2D[0], orig2D[1], orig2D[0], orig2D[1] - max2D[1]/2.0, fill='white')
    canvas.create_line(orig2D[0], orig2D[1], orig2D[0] + math.tan(60.0*math.pi/180.0) * max2D[1]/2.0, orig2D[1] + max2D[1]/2.0, fill='white')
    canvas.create_line(orig2D[0], orig2D[1], orig2D[0] - math.tan(60.0*math.pi/180.0) * max2D[1]/2.0, orig2D[1] + max2D[1]/2.0, fill='white')


def estimateF(planets, i):

    F = np.array([0, 0, 0])
    for n in range(0, len(planets)):
        if n != i:
            vd = planets[n].x - planets[i].x
            d = np.linalg.norm(vd)
            F = F + G_mod * planets[i].m * planets[n].m * vd / (d * d * d)
    return F


#################################################################################################
##################################################################################################
if __name__ == "__main__":


    parser = OptionParser(usage="%prog --help")
    parser.add_option("-c", "--canvassize",            dest="canvassize",              type='string',          default='600x800',               help="Size of the canvas")
    (options, args) = parser.parse_args()
   
    #Important constants
    earthmassconstant = 5.972e24
    G = 6.67430e-11
    sun_earth = 151300e6
    earthmass = 1
    sunmass = 1.989e30/earthmassconstant
    timeUnit = 1.0
    constant =  1.0 /earthmassconstant * 500. / sun_earth * (timeUnit*24.*60.*60.)**2 

    global G_mod
    global ux, uy, uz
    G_mod = G * earthmassconstant**2 / (sun_earth**2/500**2) * constant
    ux = np.array([-math.cos(30.0*math.pi/180.0), math.sin(30.0*math.pi/180.0)])
    uy = np.array([math.cos(30.0*math.pi/180.0), math.sin(30.0*math.pi/180.0)])
    uz = np.array([0, -1])

    #Canvas setup
    global gui
    gui = Tk()
    gui.geometry(options.canvassize)
    gui.title("Universe")
    twidth = float(options.canvassize.split("x")[0])
    theight = float(options.canvassize.split("x")[1])
    global canvas
    canvas = Canvas(gui, width=twidth, height=theight, bg='black')
    canvas.pack(fill="both", expand=True)

    global orig2D
    orig2D = np.array([twidth / 2.0, theight / 2.0])
    
    global max2D
    max2D = np.array([twidth, theight])


    planets = []
    
    distances = 20.0 * np.array([0.39, 0.72, 1.00, 1.52, 5.20, 9.54, 19.19, 30.06, 39.44]) 
    #masses = (1.0/earthmassconstant) * np.array([3.28e23, 4.83e24, 5.972e24, 6.40e23, 1.9e27, 5.98e26, 8.67e25, 1.05e26, 1.25e22])
    masses = (1.0/earthmassconstant) * np.array([3.28e23, 4.83e24, 5.972e24, 6.40e23, 1.9e27, 5.98e30, 8.67e25, 1.05e26, 1.25e22])
    color = ['orange', 'white', 'blue', 'red', 'tomato', 'purple', 'cyan', 'green', 'papaya whip']
    radius = [2, 2, 2, 2, 4, 4, 4, 3, 2]
    totalmomentum = np.array([0., 0., 0.])
    for i in range(0, len(distances)):
        d = distances[i]
        m = masses[i]
        v = math.sqrt(G_mod * sunmass / d)
        phi = np.random.uniform(0, math.pi)
        position = d * np.array([math.cos(phi), math.sin(phi), 0])
        velocity = v * np.array([-math.sin(phi), math.cos(phi), 0])
        planets.append(Planet(position, velocity, m, color[i], radius[i])) 
        totalmomentum += m * velocity  

    sunvelocity = -totalmomentum /sunmass
    planets.append(Planet(np.array([0, 0, 0]), sunvelocity, sunmass, 'yellow', 10)) 

    DeltaT = 0.005
    drawingPeriod = 0.1
    timeCounter = 0
    for iteracion in range(0,100000):
        F = []
        for i in range(0, len(planets)):
            F.append(estimateF(planets, i))
        for i in range(0, len(planets)):
            planets[i].updateDynamics(DeltaT, F[i])
        timeCounter += DeltaT
        if timeCounter > drawingPeriod:
            for i in range(0, len(planets)):
                drawAxis(canvas, gui, orig2D, max2D)
                planets[i].Draw()
                timeCounter = 0 
                gui.update()
                #time.sleep(0.01)

    gui.mainloop()



    
