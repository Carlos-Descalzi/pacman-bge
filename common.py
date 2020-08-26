import bge.logic
import mathutils
import math

PHANTOMS = {
	'1': 'BluePhantomBody',
	'2': 'OrangePhantomBody',
	'3': 'GreenPhantomBody',
	'4': 'RedPhantomBody'
}

class Direction:
	def __init__(self,rot,vect,back):
		self.rot = mathutils.Euler((0,0,math.radians(rot)),'XYZ').to_matrix()
		self.vect = mathutils.Vector(vect)
		self.back = back

DIRECTIONS = {
	'left':	Direction(90.0,[-1,0,0],'right'),
	'right':Direction(270.0,[1,0,0],'left'),
	'up':	Direction(0,[0,1,0],'down'),
	'down':	Direction(180.0,[0,-1,0],'up')
}
X_OFFSET = 13.5
Y_OFFSET = 14.5
VECTOR_X3D = mathutils.Vector((1,0,0))
VECTOR_X2D = mathutils.Vector((1,0))
VECTOR_Y3D = mathutils.Vector((0,1,0))
VECTOR_Y2D = mathutils.Vector((0,1))

def get_map_pos(v):
	return (int(round(v.x / 2 + X_OFFSET)),int(round(Y_OFFSET - v.y / 2)))

def get_scene_pos(x,y,z):
	return [(x-X_OFFSET)*2,(Y_OFFSET-y)*2,z]

def character_get_dirs(obj):
	return [d for d in DIRECTIONS.keys() if obj[d]]

def find_obj_by_prop(scene,prop,val=None):
	return [obj for obj in list(scene.objects) if (prop in obj.getPropertyNames() and ((not val) or obj[prop]==val))]

def delta_time():
	return 1.0 / bge.logic.getLogicTicRate() 

def get_levelmap():
	scene = bge.logic.getCurrentScene()
	world = scene.objects['World']
	return world['levelmap']

def distance(p1,p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return math.sqrt(dx*dx+dy*dy)

def set_state(obj,state):
	obj.state |= state

def unset_state(obj,state):
	obj.state &= ~state


