import bge.logic
import math
import mathutils
import random
import search
from common import *
from levelmap import LEVEL_MAP
import maze

class LevelDef:
	def __init__(self,levelmap,wall,phantom_speed,phantom_state_lenght):
		self.levelmap = levelmap
		self.wall = wall
		self.phantom_speed = phantom_speed
		self.phantom_state_lenght = phantom_state_lenght

	def apply(self,phantom):
		phantom['speed'] = self.phantom_speed
		phantom['state_lenght'] = self.phantom_state_lenght

LEVELS = [
	LevelDef(LEVEL_MAP,'Brick1',12.0,8),
	LevelDef(LEVEL_MAP,'Brick2',12.5,7),
	LevelDef(LEVEL_MAP,'Brick3',12.5,6),
	LevelDef(maze.create_maze(),'Brick4',12.7,5)
]

def build_map():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	
	level = LEVELS[obj['level']-1]
	
	levelmap = search.LevelMap(level.levelmap)
	
	brick = scene.objectsInactive[level.wall]

	pills = {
		'.': scene.objectsInactive['SmallPill'],
		'*': scene.objectsInactive['BigPill']
	}

	pacman_pos = None
	
	corner = scene.objectsInactive['Corner']
	output = scene.objectsInactive['Output']

	pill_count = 0

	level_phantoms = []

	for y,line in enumerate(level.levelmap):
		for x,c in enumerate(line):
			if c in 'X .*+':
				dirs = get_paths(level.levelmap,x,y,c == 'X')
				if dirs:
					new_corner = scene.addObject(corner,obj)
					new_corner['start'] = c == 'X'
					for d in DIRECTIONS.keys():
						new_corner[d] = d in dirs
					new_corner.worldPosition = get_scene_pos(x,y,0)
					if c == '+':
						new_corner['transport'] = True
			if c == '#':
				new_brick = scene.addObject(brick,obj)
				new_brick.worldPosition = get_scene_pos(x,y,2.5)
			elif c in pills:
				new_pill = scene.addObject(pills[c],obj)
				new_pill.worldPosition = get_scene_pos(x,y,0)
				pill_count+=1
			elif c in PHANTOMS:
				phantom = create_phantom(obj,scene,c)
				phantom.worldPosition = get_scene_pos(x,y,1.15)
				level_phantoms.append(phantom)
			elif c == 'X':
				pacman_pos = get_scene_pos(x,y,1)
			elif c == 'O':
				new_output = scene.addObject(output,obj)
				new_output.worldPosition = get_scene_pos(x,y,0.3)

	obj['pills'] = pill_count
	obj['start_point'] = pacman_pos
	obj['levelmap'] = levelmap

	for phantom in level_phantoms:
		level.apply(phantom)

def next_level():
	pass

def create_phantom(obj,scene,num):
	phantom = scene.addObject('Phantom',obj)
	phantom['number'] = num
	return phantom

def map_reset():
	scene = bge.logic.getCurrentScene()
	phantoms = find_obj_by_prop(scene,'phantom')

	levelmap = get_levelmap()
	phantom_positions = levelmap.get_phantom_positions()
	
	for phantom in phantoms:
		number = phantom['number']
		phantom['turn'] = number
		pos = phantom_positions[str(number)]
		phantom.worldPosition = get_scene_pos(pos[0],pos[1],1)
		phantom.state = 1	

def pacman_init():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	pacman_pos = obj['start_point']

	pac = scene.objectsInactive['Pacman']
	new_pac = scene.addObject(pac,obj)
	new_pac.worldPosition = pacman_pos
	set_pacman_visible(new_pac,False)

	tel = scene.objectsInactive['Teleport']
	new_tel = scene.addObject(tel,obj)
	new_tel.worldPosition = [pacman_pos[0],pacman_pos[1],0]

def pacman_show():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	set_pacman_visible(obj,True)

def set_pacman_visible(obj,visible):
	obj.children['PacmanArmature'].children['PacmanBody'].visible = visible
	obj.children['PacmanArmature'].children['PacmanBodyBack'].visible = visible

def get_paths(level,x,y,is_start):
	valid = ' .*XO+'
	dirs = []
	if x > 0 and level[y][x-1] in valid: dirs.append('left')
	if x < 27 and level[y][x+1] in valid: dirs.append('right')
	if y > 0 and level[y-1][x] in valid: dirs.append('up')
	if y < 30 and level[y+1][x] in valid: dirs.append('down')

	if len(dirs) == 2 and not is_start:
		if 'left' in dirs and 'right' in dirs:
			return []
		if 'up' in dirs and 'down' in dirs:
			return []

	return dirs

def follow_pacman():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	pos = mathutils.Vector((0,0,0))
	try:
		pacman = scene.objects['Pacman']
		pos = pacman.worldPosition
	except:
		world = scene.objects['World']
		start_point = world['start_point']
		if start_point:
			pos = mathutils.Vector(start_point)
	obj.worldPosition = pos + mathutils.Vector([21.46,-17.39,15.38])


def on_player_left():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['K_Left'].positive:
		obj = ctrl.owner
		set_dir(ctrl,obj,'left')

def on_player_right():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['K_Right'].positive:
		obj = ctrl.owner
		set_dir(ctrl,obj,'right')

def on_player_up():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['K_Up'].positive:
		obj = ctrl.owner
		set_dir(ctrl,obj,'up')

def on_player_down():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['K_Down'].positive:
		obj = ctrl.owner
		set_dir(ctrl,obj,'down')
	

def set_dir(ctrl,obj,direction):
	if obj['dir'] != direction and obj[direction]:
		dir_data = DIRECTIONS[direction]
		obj.worldOrientation = dir_data.rot
		if DIRECTIONS[direction].back != obj['dir']:
			obj.worldPosition.x = obj['cx']
			obj.worldPosition.y = obj['cy']
		obj['dir'] = direction
		obj['left'] = direction in ['left','right']
		obj['right'] = direction in ['left','right']
		obj['up'] = direction in ['up','down']
		obj['down'] = direction in ['up','down']

def player_init():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner


def player_loop():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors['Player_Loop'].positive:
		if obj['dir'] != 'none':
			direction = DIRECTIONS[obj['dir']]
			obj.worldPosition += direction.vect * obj['speed'] * delta_time()
			

def player_on_corner():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	sensor = ctrl.sensors['Collision']
	if sensor.positive:
		corner = sensor.hitObject
		
		if corner['transport']:
			scene = bge.logic.getCurrentScene()
			corners = find_obj_by_prop(scene,'transport',True)
			for c in corners:
				if c != corner:
					obj.worldPosition.x = c.worldPosition.x
					obj.worldPosition.y = c.worldPosition.y
					break
		else:
			for d in DIRECTIONS.keys():
				obj[d] = corner[d]
			obj['cx'] = corner.worldPosition.x
			obj['cy'] = corner.worldPosition.y
			if obj['dir'] != 'none' and not corner[obj['dir']]:
				obj['dir'] = 'none'

def update_score():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	for sensor in ctrl.sensors:
		if sensor.positive:
			if sensor.subjects[0] == 'smallPillEaten':
				obj['pills'] = obj['pills'] - 1
			points = int(sensor.bodies[0])
			obj['score']+=points
			obj.sendMessage('updateScore',str(obj['score']))

	
def show_bonus():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	options = ['Bonus1','Bonus2','Bonus3','BonusPill']

	if ctrl.sensors['BonusRandom'].positive and ctrl.sensors['BonusDelay'].positive:
		chosen = random.choice(options)

		bonus = scene.addObject(chosen,obj)
		bonus.worldPosition = obj['start_point']
		obj.sendMessage('bonusAvailable','')

def pacman_touched():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	sensor = ctrl.sensors[0]

	if sensor.positive:
		hit = sensor.hitObject

		if not hit['scared']:
			obj.suspendDynamics(True)
			obj.state = 2

def pacman_dead():
	# restart all
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	if ctrl.sensors[0].positive:
		obj['lives']-=1
		obj.sendMessage('updateLives',str(obj['lives']))
		if obj['lives'] > 0:
			obj.state = 2
			map_reset()
		else:
			ctrl.activate(ctrl.actuators[0])

def level_done():
	pass

def next_done():
	
	obj['level']+=1
	all_objs = [o for o in scene.objects if o.name != 'World']
	map(KX_GameObject.endObject,all_objs)
	obj.state = 1
	
