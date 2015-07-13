#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import Image
import numpy

ESC = '\033'
DELTA = 60
CONFIG_DATA = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class Vector():
	def __init__(self, x0 = 0.0, x1 = 0.0, x2 = 0.0):
		self.x0 = x0
		self.x1 = x1
		self.x2 = x2

	def vectorProduct(self, v):
		u = Vector()
		# | i j k |
		# | a b c |
		# | d e f | = (bf -  ce)i +
		u.x0        = self.x1 * v.x2 - self.x2 * v.x1
					# (cd -  af)j +
		u.x1		= self.x2 * v.x0 - self.x0 * v.x2
					# (ae -  bd)k
		u.x2		= self.x0 * v.x1 - self.x1 * v.x0

		return u

	def vectorNormalize(self):
		u = Vector()
		norm = math.sqrt(self.x0*self.x0 + self.x1*self.x1 + self.x2*self.x2)
		u.x0 = self.x0/norm
		u.x1 = self.x1/norm
		u.x2 = self.x2/norm
		return u

	def vectorMulScalar(self, alpha):
		u = Vector()
		u.x0 = alpha*self.x0
		u.x1 = alpha*self.x1
		u.x2 = alpha*self.x2
		return u

	def vectorNorm(self):
		return math.sqrt(self.x0*self.x0 + self.x1*self.x1 + self.x2*self.x2)

class Texture():
	def __init__(self):
		self.texID = 0

	def loadFromFile(self, fileName):
		"""Load an image file as a 2D texture using PIL"""
		try:
			im = Image.open(fileName)
		except IOError:
			print ("Could not open %s"%fileName)
			if fileName == "jack.jpg":
				print (bcolors.FAIL + 
					"""Sorry, but Jack's been with us through the entire """
						""" project... We cannot go on without him"""
					+ bcolors.ENDC)
				sys.exit("\"Why is the rum gone?\"")
		else:
			if fileName == "jack.jpg":
				print (bcolors.OKGREEN + "Yo-ho-ho and a bottle of rum!" +
					  bcolors.ENDC)
			
				
		imData = numpy.array(list(im.getdata()), numpy.int8)
		texImage, w, h = imData, im.size[0], im.size[1]

		self.texID = glGenTextures(1)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glBindTexture(GL_TEXTURE_2D, self.texID)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB,
				     GL_UNSIGNED_BYTE, texImage)

	def setTexture(self):
		glBindTexture(GL_TEXTURE_2D, self.texID)

	def enableTextures(self):
		glEnable(GL_TEXTURE_2D)

	def disableTextures(self):
		glDisable(GL_TEXTURE_2D)

skyTexture1  = Texture()
skyTexture2  = Texture()
skyTexture3  = Texture()
skyTexture4  = Texture()
skyTexture5  = Texture()
trackTexture = Texture()
jackTexture  = Texture()
kartTexture  = Texture()

class World():
	def __init__(self):
		self.trackPts = []
		self.normalMatrix = []
		self.CUBE_Xmin = 0.
		self.CUBE_Xmax = 400.
		self.CUBE_Ymin = 0.
		self.CUBE_Ymax = 400.
		self.CUBE_Zmin = 0.
		self.CUBE_Zmax = 400.
		self.trianglesAmountOnXAxis = 40 #
		self.trianglesAmountOnZAxis = 40 #
		self.sizeCubeX = self.CUBE_Xmax - self.CUBE_Xmin
		self.sizeCubeZ = self.CUBE_Zmax - self.CUBE_Zmin
		self.scaleZ = self.sizeCubeZ / self.trianglesAmountOnZAxis
		self.scaleX = self.sizeCubeX / self.trianglesAmountOnXAxis
		self.scaleY = 1.

	def drawSky(self):
		skyTexture1.enableTextures()
		skyTexture1.setTexture()
		glBegin(GL_QUADS)
		#face z = CUBE_Zmax
		glTexCoord2f(0.0, 0.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymin,
														   self.CUBE_Zmax);
		glTexCoord2f(1.0, 0.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymin,
														   self.CUBE_Zmax);
		glTexCoord2f(1.0, 1.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glTexCoord2f(0.0, 1.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glEnd()
		skyTexture1.disableTextures()

		skyTexture2.enableTextures()
		skyTexture2.setTexture()
		glBegin(GL_QUADS)
		#face y = CUBE_Ymax
		glTexCoord2f(0.0, 1.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glTexCoord2f(0.0, 0.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glTexCoord2f(1.0, 0.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glTexCoord2f(1.0, 1.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glEnd()
		skyTexture2.disableTextures()

		skyTexture3.enableTextures()
		skyTexture3.setTexture()
		glBegin(GL_QUADS)
		#face x = CUBE_Xmax
		glTexCoord2f(1.0, 0.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymin,
														   self.CUBE_Zmin);
		glTexCoord2f(1.0, 1.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glTexCoord2f(0.0, 1.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glTexCoord2f(0.0, 0.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymin,
														   self.CUBE_Zmax);
		glEnd()
		skyTexture3.disableTextures()

		skyTexture4.enableTextures()
		skyTexture4.setTexture()
		glBegin(GL_QUADS)
		#face x = CUBE_Xmin
		glTexCoord2f(0.0, 0.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymin,
														   self.CUBE_Zmin);
		glTexCoord2f(1.0, 0.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymin,
														   self.CUBE_Zmax);
		glTexCoord2f(1.0, 1.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmax);
		glTexCoord2f(0.0, 1.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glEnd()
		skyTexture4.disableTextures()

		skyTexture5.enableTextures()
		skyTexture5.setTexture()
		glBegin(GL_QUADS)
		#face z = CUBE_Zmin
		glTexCoord2f(1.0, 0.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymin,
														   self.CUBE_Zmin);
		glTexCoord2f(1.0, 1.0); glVertex3f(self.CUBE_Xmin, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glTexCoord2f(0.0, 1.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymax,
														   self.CUBE_Zmin);
		glTexCoord2f(0.0, 0.0); glVertex3f(self.CUBE_Xmax, self.CUBE_Ymin,
														   self.CUBE_Zmin);
		glEnd()
		skyTexture5.disableTextures()

	def drawTrack(self):
		#"face y = CUBE_Ymin"
		trackTexture.enableTextures()
		trackTexture.setTexture()
		# Triangles draw order.
		#    1-------3 (3->1 of next iteration)
		#    |      /|
		#    |     / |
		#    |    /  |
		#    |   /   |
		#    |  /    |
		#    | /     |
		#    2-------4 (4->2 of next iteration)
		#
		#	i=0,k=0 ___________________ i=0,k=m
		#		   | /| /| /| /| /| /|
		#		   |/_|/_|/_|/_|/_|/_|
		#		   | /| /| /| /| /| /|
		#		   |/_|/_|/_|/_|/_|/_|
		#		   | /| /| /| /| /| /|
		# +Z<______|/_|/_|/_|/_|/_|/_|
		#		   | /| /| /| /| /| /|
		#		   |/_|/_|/_|/_|/_|/_|
		#		   | /| /| /| /| /| /|
		#		   |/_|/_|/_|/_|/_|/_|
		#		   | /| /| /| /| /| /|
		#	i=n,k=0|/_|/_|/_|/_|/_|/_| i=n,k=n
		#					|
		#					|
		#					|
		#				   \/
		#				   +X
		for k in xrange(0, self.trianglesAmountOnZAxis):
			for i in xrange(0, self.trianglesAmountOnXAxis):
				glBegin(GL_TRIANGLE_STRIP)
				#1
				glTexCoord2f(i*self.scaleX/self.sizeCubeX,
							 k*self.scaleZ/self.sizeCubeZ)
				n = world.normalMatrix[i][k][1]
				glNormal3f(n.x0, n.x1, n.x2)
				glVertex3f(self.CUBE_Xmin + i*self.scaleX,
						   self.CUBE_Ymin + self.trackPts[i][k]/self.scaleY,
						   self.CUBE_Zmin + k*self.scaleZ)
				#2
				glTexCoord2f(i*self.scaleX/self.sizeCubeX,
							(k+1)*self.scaleZ/self.sizeCubeZ)
				n = world.normalMatrix[i][k][1]
				glNormal3f(n.x0, n.x1, n.x2)
				glVertex3f(self.CUBE_Xmin + i*self.scaleX,
						   self.CUBE_Ymin + self.trackPts[i][k+1]/self.scaleY,
						   self.CUBE_Zmin + (k+1)*self.scaleZ)
				#3
				glTexCoord2f((i+1)*self.scaleX/self.sizeCubeX,
							 k*self.scaleZ/self.sizeCubeZ)
				n = world.normalMatrix[i][k][1]
				glNormal3f(n.x0, n.x1, n.x2)
				glVertex3f(self.CUBE_Xmin + (i+1)*self.scaleX,
						   self.CUBE_Ymin + self.trackPts[i+1][k]/self.scaleY,
						   self.CUBE_Zmin + k*self.scaleZ)
				#4
				glTexCoord2f((i+1)*self.scaleX/self.sizeCubeX,
							 (k+1)*self.scaleZ/self.sizeCubeZ)
				n = world.normalMatrix[i][k][0]
				glNormal3f(n.x0, n.x1, n.x2)
				glVertex3f(self.CUBE_Xmin + (i+1)*self.scaleX,
						   self.CUBE_Ymin + self.trackPts[i+1][k+1]/self.scaleY,
						   self.CUBE_Zmin + (k+1)*self.scaleZ)
				glEnd()

		trackTexture.disableTextures()

	def drawAxes(self):
		glLineWidth(10.)
		glColor3f(1., 0., 0.)
		glBegin(GL_LINES)
		glVertex3f( self.CUBE_Xmin,
				   (self.CUBE_Ymax - self.CUBE_Ymin)/2.,
				   (self.CUBE_Zmax - self.CUBE_Zmin)/2.)
		glVertex3f( self.CUBE_Xmax,
					(self.CUBE_Ymax - self.CUBE_Ymin)/2.,
					(self.CUBE_Zmax - self.CUBE_Zmin)/2.)
		glEnd()

		glLineWidth(10.)
		glColor3f(0., 1., 0.)
		glBegin(GL_LINES)
		glVertex3f( (self.CUBE_Xmax - self.CUBE_Xmin)/2.,
					self.CUBE_Ymin,
					(self.CUBE_Zmax - self.CUBE_Zmin)/2.)
		glVertex3f( (self.CUBE_Xmax - self.CUBE_Xmin)/2.,
					self.CUBE_Xmax,
					(self.CUBE_Zmax - self.CUBE_Zmin)/2.)
		glEnd()

		glLineWidth(10.)
		glColor3f(0., 0., 1.)
		glBegin(GL_LINES)
		glVertex3f( (self.CUBE_Xmax - self.CUBE_Xmin)/2.,
					(self.CUBE_Ymax - self.CUBE_Ymin)/2.,
					self.CUBE_Zmin)
		glVertex3f( (self.CUBE_Xmax - self.CUBE_Xmin)/2.,
					(self.CUBE_Ymax - self.CUBE_Ymin)/2.,
					self.CUBE_Zmax)
		glEnd()

	def drawWorld(self):
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

		self.drawSky()
		self.drawTrack()
		self.drawAxes()
		for i in xrange(0, len(trees)):
			trees[i].drawTree()
		kart.drawKart()
		jack.drawJack()
world = World()

def getTrianglePosition(Px, Pz):
	i = int(math.floor(Px/world.scaleX))
	j = int(math.floor(Pz/world.scaleX))
	mantissaX, integerX = math.modf(Px) # we don't use integerX
	mantissaZ, integerZ = math.modf(Pz) # we don't use integerZ

	#avoiding tan(pi/2), which does not exist
	if mantissaZ < math.pow(10., -6): #our error limit
		return i, j, 1
	elif mantissaX < math.pow(10., -6):
		return i, j, 0

	t = math.degrees(math.atan(mantissaZ/mantissaX))
	if t < 45. :
		return i, j, 0
	elif t < 90. :
		return i, j, 1
	else :
		print "Error CameraTrianglePosition. Should not reach here. Aborting..."
		sys.exit(-2)

def fillNormalMatrix():
	global world
	for k in xrange(0, world.trianglesAmountOnZAxis):
		l=[]
		for i in xrange(0, world.trianglesAmountOnXAxis):
			#calculatin normals
			# <2-1, 3-1> #these number are vertices of the those
							#triangles described in drawTrack
			a = Vector( 0.,
					    (world.trackPts[i][k+1] -
					    	world.trackPts[i][k])/world.scaleY,
						world.scaleZ)
			b = Vector( world.scaleX,
						(world.trackPts[i+1][k] -
							world.trackPts[i][k])/world.scaleY,
						0.)
			u = a.vectorProduct(b)
			# <4-2, 3-2>
			a = Vector( world.scaleX,
						(world.trackPts[i+1][k+1] -
							world.trackPts[i][k+1])/world.scaleY,
						0.)
			b = Vector(	world.scaleX,
						(world.trackPts[i+1][k] -
							world.trackPts[i][k+1])/world.scaleY,
						world.scaleZ)
			v = a.vectorProduct(b)

			u = u.vectorNormalize()
			v = v.vectorNormalize()
			l.append((u, v))
		world.normalMatrix.append(l)

class Jack():
	def drawJack(self):
		Ht = 55
		base = 25
		jackTexture.enableTextures()
		jackTexture.setTexture()
		glPushMatrix()
		glTranslatef( (world.CUBE_Xmax - world.CUBE_Xmin)/2.,
				      0,
					  (world.CUBE_Zmax - world.CUBE_Zmin)/2.)
		glBegin(GL_QUADS)
		#base (y<) - not seen

		#walls
		#left - x<
		glNormal3f(-1, 0, 0)
		glTexCoord2f(0., 0.); glVertex3f(-base/2., 0,  -base/2.);
		glTexCoord2f(0., 1.); glVertex3f(-base/2., 0,   base/2.);
		glTexCoord2f(1., 1.); glVertex3f(-base/2., Ht,  base/2.);
		glTexCoord2f(1., 0.); glVertex3f(-base/2., Ht, -base/2.);

		#right - X>
		glNormal3f(1, 0, 0)
		glTexCoord2f(1., 1.); glVertex3f(base/2., 0,  -base/2.)
		glTexCoord2f(1., 0.); glVertex3f(base/2., 0,   base/2.)
		glTexCoord2f(0., 0.); glVertex3f(base/2., Ht,  base/2.)
		glTexCoord2f(0., 1.); glVertex3f(base/2., Ht, -base/2.)

		#far - z<
		glNormal3f(0, 0, -1)
		glTexCoord2f(0., 0.); glVertex3f(-base/2., 0,  -base/2.)
		glTexCoord2f(0., 1.); glVertex3f(-base/2., Ht, -base/2.)
		glTexCoord2f(1., 1.); glVertex3f( base/2., Ht, -base/2.)
		glTexCoord2f(1., 0.); glVertex3f( base/2., 0,  -base/2.)

		#near - Z>
		glNormal3f(0, 0, 1)
		glTexCoord2f(1., 1.); glVertex3f(-base/2., 0,   base/2.)
		glTexCoord2f(1., 0.); glVertex3f(-base/2., Ht,  base/2.)
		glTexCoord2f(0., 0.); glVertex3f( base/2., Ht,  base/2.)
		glTexCoord2f(0., 1.); glVertex3f( base/2., 0,   base/2.)
		glEnd()
		glPopMatrix()
		jackTexture.disableTextures()
jack = Jack()

class Tree():
	def __init__(self):
		self.Ht   = 0.
		self.Hc   = 0.
		self.base = 0.
		self.Rt   = 0.; self.Gt = 0.; self.Bt = 0.
		self.Rc   = 0.; self.Gc = 0.; self.Bc = 0.
		self.Px   = 0.; self.Py = 0.; self.Pz = 0.

	def treeSetValues(self, Px, Pz, Ht, Hc, Rt, Gt, Bt, Rc, Gc, Bc):
		Py = 0.
		self.base = 5.
		scaleT = 33.
		scaleC = 15.
		self.Ht   = Ht * scaleT
		self.Hc   = Hc * scaleC
		self.Rt   = Rt; self.Gt = Gt; self.Bt = Bt
		self.Rc   = Rc; self.Gc = Gc; self.Bc = Bc
		self.Px   = Px; self.Py = Py; self.Pz = Pz

	def drawTree(self):
		#base (y<) - not seen
		#trunk
		colorT = [self.Rt, self.Gt, self.Bt]
		glMaterialfv(GL_FRONT, GL_DIFFUSE, colorT);
		glPushMatrix()
		glTranslatef(self.Px, self.Py, self.Pz)
		glBegin(GL_QUADS)
		#left - x<
		glNormal3f(-1, 0, 0)
		glVertex3f(-self.base/2., 0,       -self.base/2.);
		glVertex3f(-self.base/2., 0,        self.base/2.);
		glVertex3f(-self.base/2., self.Ht,  self.base/2.);
		glVertex3f(-self.base/2., self.Ht, -self.base/2.);

		#right - X>
		glNormal3f(1, 0, 0)
		glVertex3f(self.base/2., 0,       -self.base/2.)
		glVertex3f(self.base/2., 0,        self.base/2.)
		glVertex3f(self.base/2., self.Ht,  self.base/2.)
		glVertex3f(self.base/2., self.Ht, -self.base/2.)

		#far - z<
		glNormal3f(0, 0, -1)
		glVertex3f(-self.base/2., 0,       -self.base/2.)
		glVertex3f(-self.base/2., self.Ht, -self.base/2.)
		glVertex3f( self.base/2., self.Ht, -self.base/2.)
		glVertex3f( self.base/2., 0,       -self.base/2.)

		#near - Z>
		glNormal3f(0, 0, 1)
		glVertex3f(-self.base/2., 0,        self.base/2.)
		glVertex3f(-self.base/2., self.Ht,  self.base/2.)
		glVertex3f( self.base/2., self.Ht,  self.base/2.)
		glVertex3f( self.base/2., 0,        self.base/2.)

		#top - Y>
		glNormal3f(0, 1, 0)
		glVertex3f(-self.base/2., self.Ht,  self.base/2.)
		glVertex3f(-self.base/2., self.Ht, -self.base/2.)
		glVertex3f( self.base/2., self.Ht, -self.base/2.)
		glVertex3f( self.base/2., self.Ht,  self.base/2.)
		glEnd()

		#crown
		colorC = [self.Rc, self.Gc, self.Bc]
		glMaterialfv(GL_FRONT, GL_DIFFUSE, colorC);
		glTranslatef(0, self.Ht, 0)
		glRotatef(-90, 1, 0, 0)
		glutSolidCone(self.base, self.Hc, 50, 50);

		glPopMatrix()
trees = []

def loadTrees(t):
	global trees
	for i in xrange(0, len(t)):
		trees.append(Tree())
		trees[i].treeSetValues(t[i][1], t[i][2], t[i][3], t[i][4], t[i][5],
				               #Px      Py       Ht       Hc       Rt
							   t[i][6], t[i][7], t[i][8], t[i][9], t[i][10])
							   #Gt      Bt       Rc       Gc        Bc
def animacao( id ):
	glutPostRedisplay()
	glutTimerFunc(DELTA, animacao, 0)
	kart.kartMove()

def loadTextures():
	skyTexture1.loadFromFile(CONFIG_DATA[0])
	skyTexture2.loadFromFile(CONFIG_DATA[1])
	skyTexture3.loadFromFile(CONFIG_DATA[2])
	skyTexture4.loadFromFile(CONFIG_DATA[3])
	skyTexture5.loadFromFile(CONFIG_DATA[4])
	trackTexture.loadFromFile(CONFIG_DATA[7])
	jackTexture.loadFromFile('jack.jpg')
	kartTexture.loadFromFile('bola.jpg')

def init(configFile = 'config.txt'):
	global world
	global kart
	global CONFIG_DATA
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

	glutInitWindowSize(500, 500)
	glutInitWindowPosition(600, 200)
	glutCreateWindow(sys.argv[0])

	glClearColor(0.5, 0.5, 0.5, 0.0)
	#glShadeModel(GL_FLAT)
	glEnable(GL_DEPTH_TEST) #this IS important

	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutKeyboardFunc(keyboard)
	glutTimerFunc(DELTA, animacao, 0)

	CONFIG_DATA = carregueConfig(configFile)

	trackTexName, texData, w, h, world.trackPts = carreguePista(CONFIG_DATA[5],
																False)
	k, trees = carregueDetalhes(CONFIG_DATA[6], False)
	loadTrees(trees)
	fillNormalMatrix()
	k = k[0]
	kart = Kart(k[1], k[2], k[3], k[4], k[5], k[6], k[7])
	kart.resetKart()
	CONFIG_DATA.append(trackTexName)
	loadTextures()
def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	LIGHT0_POSITION = [0.0, 0.0, 9999.0, 0.0]
	glLightfv(GL_LIGHT0, GL_POSITION, LIGHT0_POSITION);

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(camera.Ex, camera.Ey, camera.Ez,
			  camera.Px, camera.Py, camera.Pz,
			  camera.Ux, camera.Uy, camera.Uz)
	world.drawWorld()
	glutSwapBuffers()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1.0*w / h, 0.05, 700)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(camera.Ex, camera.Ey, camera.Ez,
			  camera.Px, camera.Py, camera.Pz,
			  camera.Ux, camera.Uy, camera.Uz)

class Camera():
	def __init__(self):
		self.RO = 80.
		self.yDist = 35.
		self.Ex = 0.
		self.Ey = 0.
		self.Ez = 0.
		self.Px = 0.
		self.Py = 0.
		self.Pz = 0.
		self.Ux = 0.
		self.Uy = 0.
		self.Uz = 0.

	def defineCamera(self,
			         eyeX, eyeY, eyeZ,
					 centerX, centerY,
					 centerZ, upX, upY, upZ):

		correctionXmin =  3.
		correctionXmax = -3.
		correctionYmin =  3.
		correctionYmax = -3.
		correctionZmin =  3.
		correctionZmax = -3.
		
		#camera cannot get out from world. God of War effect. Hell yeah! ì.í
		if eyeX < world.CUBE_Xmin:
			print "avoiding camera going out on X<"
			eyeX = world.CUBE_Xmin + correctionXmin
		elif eyeX > world.CUBE_Xmax:
			print "avoiding camera going out on X>"
			eyeX = world.CUBE_Xmax + correctionXmax

		if eyeY < world.CUBE_Ymin:
			print "Avoiding camera going out on Y<"
			eyeY = world.CUBE_Ymin + correctionYmin
		elif eyeY > world.CUBE_Ymax:
			print "Avoiding camera going out on Y>"
			eyeY = world.CUBE_Ymax + correctionYmax
			
		if eyeZ < world.CUBE_Zmin:
			print "Avoiding camera going out on Z<"
			eyeZ = world.CUBE_Zmin + correctionZmin

		elif eyeZ > world.CUBE_Zmax:
			print "Avoiding camera going out on Z>"
			eyeZ = world.CUBE_Zmax + correctionZmax

		self.Ex = eyeX
		self.Ey = eyeY
		self.Ez = eyeZ
		self.Px = centerX
		self.Py = centerY
		self.Pz = centerZ
		self.Ux = upX
		self.Uy = upY
		self.Uz = upZ

	def setCameraHeight(self, h):
		self.yDist = h

	def resetCamera(self):
		u    = Vector(kart.Vd.x0, 0., kart.Vd.x2)
		u    = u.vectorNormalize()
		u.x0 = kart.Px - self.RO*u.x0
		u.x2 = kart.Pz - self.RO*u.x2

		Ex, Ey, Ez = u.x0,    kart.Py + self.yDist, u.x2
		Px, Py, Pz = kart.Px, kart.Py,              kart.Pz
		Ux, Uy, Uz = .0,      1.,                   .0

		self.defineCamera(Ex, Ey, Ez,
						  Px, Py, Pz,
						  Ux, Uy, Uz)
camera = Camera()

class Kart():
	def __init__(self, Px = 0., Pz = 0., R = 3.,
			           Rk = 0., Gk = 0., Bk = 0., THETA = 0.):
		self.ROTHETA = math.radians(THETA) # read only
		self.THETA   = math.radians(THETA)

		self.ROPx = Px # read only
		self.Px   = Px

		self.Py   = 0.

		self.ROPz = Pz # read only
		self.Pz   = Pz

		self.Rk = Rk
		self.Gk = Gk
		self.Bk = Bk

		self.Vd = Vector()
		self.V  = self.Vd.vectorNorm()
		self.R  = R
		self.distUpFromTrack = self.R
		if self.V > 0.0:
			self.resetKart()

	def drawKart(self):
		qObj = gluNewQuadric();
		gluQuadricNormals(qObj, GLU_SMOOTH);
		gluQuadricTexture(qObj, GL_TRUE);

		#kartTexture.enableTextures()
		#kartTexture.setTexture()
		colorT = [self.Rk, self.Gk, self.Bk]
		glMaterialfv(GL_FRONT, GL_DIFFUSE, colorT);

		glPushMatrix()
		glTranslatef(self.Px, self.Py, self.Pz)
		gluSphere(qObj, self.R, 100, 100);
		glPopMatrix()
		#kartTexture.disableTextures()

		glLineWidth(10.)
		glColor3f(0., 1., 0.)
		glBegin(GL_LINES)
		glVertex3f(self.Px, self.Py, self.Pz)
		glVertex3f(self.Px + self.V * self.Vd.x0,
				   self.Py + self.V * self.Vd.x1,
				   self.Pz + self.V * self.Vd.x2)
		glEnd()

	def resetKart(self):
		self.THETA = self.ROTHETA
		i, k, c = getTrianglePosition(self.ROPx, self.ROPz) #??
		hv1 = world.trackPts[i][k]
		hv2 = world.trackPts[i][k+1]
		hv3 = world.trackPts[i+1][k]
		self.Px = self.ROPx
		self.Py = (hv1 + hv2 + hv3)/3. + self.R
		self.Pz = self.ROPz
		self.V  = 0.
		self.Vd.x0 = math.cos(self.THETA)
		self.Vd.x2 = math.sin(self.THETA)
		camera.resetCamera()

	def accel(self, a, b):
		self.V = self.V * a + b
		
	def kartMove(self):
		if self.V > 0.0001 and self.V < -0.0001: #avoid division by 0
			return
		Kx = self.Px + self.Vd.x0 * self.V
		Kz = self.Pz + self.Vd.x2 * self.V
		i, k, j = getTrianglePosition(Kx, Kz)
		j = (world.trackPts[i][k] +
				world.trackPts[i][k+1] +
				world.trackPts[i+1][k])/3.
		Ky = self.distUpFromTrack + j
		self.Px, self.Py, self.Pz = Kx, Ky, Kz
		camera.resetCamera()

	def kartTurnRight(self):
		self.THETA = (self.THETA + 0.1) % (2*math.pi)
		u = Vector()
		u.x0 = self.Px*math.cos(self.THETA) - self.Pz*math.sin(self.THETA)
		u.x2 = self.Px*math.sin(self.THETA) + self.Pz*math.cos(self.THETA)
		u.x1 = 0.
		u = u.vectorNormalize()
		self.Vd.x0 = u.x0
		self.Vd.x2 = u.x2
		camera.resetCamera()

	def kartTurnLeft(self):
		self.THETA = (self.THETA - 0.1) % (2*math.pi)
		u = Vector()
		u.x0 = self.Px*math.cos(self.THETA) - self.Pz*math.sin(self.THETA)
		u.x2 = self.Px*math.sin(self.THETA) + self.Pz*math.cos(self.THETA)
		u.x1 = 0.
		u = u.vectorNormalize()
		self.Vd.x0 = u.x0
		self.Vd.x2 = u.x2
		camera.resetCamera()
kart = Kart()

def keyboard(key, x, y):
	if (key == ESC) or (key == 'q'):
		sys.exit(0)

	elif key == 'j':
		kart.kartTurnLeft()
	elif key == 'l':
		kart.kartTurnRight()
	elif key == 'i':
		camera.yDist += 1.
	elif key == 'k':
		camera.yDist -= 1.

	elif key == 'a':
		kart.accel(1., 0.04)
	elif key == 'z':
		kart.accel(1., -0.04)

	elif key == 'v':
		camera.resetCamera()
	elif key == 'b':
		kart.resetKart()

#####################################################
#####################################################

T = 0   # top
N = 1   # north
E = 2   # east
S = 3   # south
W = 4   # west
P = 5   # course
D = 6   # detail

# ----------------------------------------------------------------------

def carregueConfig(fileName):
    """ (file) -> list of file names
    retorna uma lista com os nomes dos arquivos contidos no
	arquivo de configuração.
    """
    try:
        fp = open(fileName)
    except IOError:
        print ("Não consegui abrir o arquivo %s"%(fileName))
        sys.exit(-1)

    name = []
    for line in fp:
        name.append(line.strip())

    fp.close()
    return name

# ----------------------------------------------------------------------

def carregueDetalhes( fileName, verbose = False ):
    """ (file) -> names
    retorna listas, cada lista com os objetos de um tipo
    contidos no arquivo de detalhes.
    """
    try:
        fp = open(fileName)
    except IOError:
        print ("Não consegui abrir o arquivo %s"%(fileName))
        sys.exit(-1)

    kart = []
    tree = []
    for line in fp:
        l = line.strip().split()
        for i in range(1, len(l)):
            l[i] = float(l[i])
        if l[0] == 'K':
            if verbose:
                print ("Achei um kart", l)
            kart.append(l)
        elif l[0] == 'A':
            if verbose:
                print ("Achei uma arvore", l)
            tree.append(l)
        else:
            if verbose:
                print("Nao entendi a linha", l)

    fp.close()
    return kart, tree

# ----------------------------------------------------------------------

def carreguePista( fileName, verbose = False ):
    """ (file) -> texData, texWidth, texHeight, trackPts
    retorna a textura (data, largura e altura)
    e uma matriz com o mapa de elevação da pista.
    """
    try:
        fp = open(fileName)
    except IOError:
        print ("Não consegui abrir o arquivo %s"%(fileName))
        sys.exit(-1)

    nameTextureTrack = fp.readline().strip()
    img  = Image.open(nameTextureTrack)
    texData = numpy.array(list(img.getdata()), numpy.int8)
    w, h = img.size[0], img.size[1]

    xmin, ymin = fp.readline().strip().split()
    xmax, ymax = fp.readline().strip().split()
    xmin = int(xmin)
    xmax = int(xmax)
    ymin = int(ymin)
    ymax = int(ymax)

    trackPts = []
    for line in fp:
        l = [float(x) for x in line.strip().split()]
        trackPts.append(l)
    fp.close()

    if verbose:
        print("Carreguei a textura de %s"%(fileName))
        print("Retangulo: inf esq (%d x %d) x sup dir (%d x %d)"
				%(xmin, ymin, xmax, ymax))
        print("Texture dimension: %d x %d"%(w, h))
        print("Track elevation dim: %d x %d"%(len(trackPts), len(trackPts[0])))
    return nameTextureTrack, texData, w, h, trackPts


#####################################################
#####################################################

if __name__ == "__main__":
	if len(sys.argv) > 1:
		init(sys.argv[1])
	else:
		init('config.txt')
	print "ESC or 'q' to quit this master game"
	glutMainLoop()
