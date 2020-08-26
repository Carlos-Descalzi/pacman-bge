import bge.logic
import math
import mathutils
import random
import search
from common import *
from levelmap import LEVEL_MAP

STATE_AT_HOME 		= 1 << 0
STATE_LEAVING_HOME 	= 1 << 1
STATE_IN_GAME 		= 1 << 2
STATE_RANDOM 		= 1 << 3
STATE_CHASING 		= 1 << 4
STATE_SCARED 		= 1 << 15
STATE_EATEN 		= 1 << 16
STATE_ZOMBIE		= 1 << 17

def phantom_init():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	number = obj['number']
	obj['turn'] = int(number)

	obj.children['PhantomBody'].replaceMesh(PHANTOMS[number])

def phantom_wake_up():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	obj['turn']-=1
	if obj['turn'] > 0:
		return

	loc = get_map_pos(obj.worldPosition)
	levelmap = get_levelmap()
	target = get_nearest_output(scene,levelmap,loc)

	map_path = levelmap.get_path(loc,target)
	path = [mathutils.Vector(get_scene_pos(p[0],p[1],1)) for p in map_path]

	set_path(obj,path)

	obj.state = STATE_LEAVING_HOME

def get_nearest_output(scene,levelmap,loc):
	outputs = find_obj_by_prop(scene,'output')
	outputs = levelmap.get_phantom_outputs()
	outputs.sort(key=lambda o:distance(loc,o))
	return outputs[0]

def phantom_leave_home():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	if ctrl.sensors[0].positive:
		done = phantom_walk(ctrl,obj)
		if done:
			obj.state = STATE_IN_GAME 

def phantom_walk(ctrl,obj):
	stop = obj['next_stop']
	pos = obj.worldPosition

	distance = (stop - pos).to_2d()
	if (distance.length > 0.1):
		speed = obj['speed']

		if obj.state & STATE_SCARED:
			speed *= 0.33
		elif obj.state & STATE_ZOMBIE:
			speed *= 0.75

		movement = distance.normalized() * speed * delta_time()
		obj.worldPosition += movement.to_3d()
		return False
	else:
		obj.worldPosition = stop

		path = obj['path']
		
		if len(path) > 0:
			set_path(obj,path)
			return False
		else:
			return True

def phantom_set_random_walk():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	levelmap = get_levelmap()

	loc = get_map_pos(obj.worldPosition)
	map_path = levelmap.random_path(loc)

	path = [mathutils.Vector(get_scene_pos(p[0],p[1],1)) for p in map_path]
	set_path(obj,path)
	

def phantom_random_walk():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors[0].positive:
		done = phantom_walk(ctrl,obj)
		if done:
			phantom_set_random_walk()

def phantom_set_chasing():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	phantom_set_path(ctrl,obj)
	

def phantom_set_path(ctrl,obj):
	scene = bge.logic.getCurrentScene()

	world = scene.objects['World']
	pacman = scene.objects['Pacman']

	levelmap = world['levelmap']

	phantom_pos = get_map_pos(obj.worldPosition)
	pacman_pos = get_map_pos(pacman.worldPosition)

	map_path = levelmap.get_path(phantom_pos,pacman_pos)
	path = [mathutils.Vector(get_scene_pos(p[0],p[1],1)) for p in map_path]
	set_path(obj,path)
	

def phantom_chase():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors[0].positive:
		done = phantom_walk(ctrl,obj)
		if done:
			phantom_set_path(ctrl,obj)
	

def phantom_check_state():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	
	obj['state_ticks'] = obj['state_ticks'] + 1

	if obj['state_ticks'] == obj['state_lenght']:
		obj['state_ticks'] = 0
		if obj.state & STATE_RANDOM:
			unset_state(obj,STATE_RANDOM)
			set_state(obj,STATE_CHASING)
		else:
			set_state(obj,STATE_RANDOM)
			unset_state(obj,STATE_CHASING)
			

def set_path(obj,path):
	next_stop = path.pop(0)
	dist = (next_stop - obj.worldPosition).normalized().to_2d()
	obj['next_stop'] = next_stop
	obj['path'] = path
	if dist.length > 0:
		angle = -VECTOR_Y2D.angle_signed(dist)
		obj.worldOrientation = mathutils.Matrix.Rotation(angle,3,'Z')

def phantom_set_scared():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	obj['scared'] = True
	obj.children[0].replaceMesh('ScaredPhantomBody')
	levelmap = get_levelmap()

	loc = get_map_pos(obj.worldPosition)
	map_path = levelmap.random_path(loc)

	path = [mathutils.Vector(get_scene_pos(p[0],p[1],1)) for p in map_path]
	set_path(obj,path)

def phantom_set_normal():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	obj['scared'] = False
	mesh = PHANTOMS[obj['number']]
	obj.children[0].replaceMesh(mesh)
	obj.state = STATE_IN_GAME

def phantom_set_eaten():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	obj['scared'] = False
	obj.children[0].replaceMesh('EatenPhantomBody')
	obj.children[0].children[0].visible = False

	levelmap = get_levelmap()
	pos = get_map_pos(obj.worldPosition)
	map_path = levelmap.path_to_home(pos)
	path = [mathutils.Vector(get_scene_pos(p[0],p[1],1)) for p in map_path]
	set_path(obj,path)

	obj.state = STATE_EATEN

def phantom_back_home():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors[0].positive:
		done = phantom_walk(ctrl,obj)
		if done:
			mesh = PHANTOMS[obj['number']]
			obj.children[0].replaceMesh(mesh)
			obj.children[0].children[0].visible = True
			obj.state = STATE_LEAVING_HOME

def phantom_set_zombie():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	obj.children[0].replaceMesh('ZombiePhantomBody')
	phantom_set_path(ctrl,obj)
	

def phantom_zombie_chase():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors[0].positive:
		done = phantom_walk(ctrl,obj)
		if done:
			phantom_set_path(ctrl,obj)
