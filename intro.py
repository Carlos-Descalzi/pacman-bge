import bge.logic
import math
import mathutils
import random

INTRO_OPTIONS = {
	1:'Start',
	2:'Options',
	3:'Exit'
}

def init():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	obj['option'] = 1

	update_options(obj)

def update_options(obj):
	scene = bge.logic.getCurrentScene()

	for o,n in INTRO_OPTIONS.items():
		opt = scene.objects[n]
		if obj['option'] == o:
			opt.meshes[0].materials[0].diffuseIntensity = 1
			opt.state = 2
		else:
			opt.meshes[0].materials[0].diffuseIntensity = 0.1
			opt.state = 1

def inc_option():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['Key_Down'].positive:
		obj = ctrl.owner
		option = obj['option']
		option+=1
		if option > 3:
			option = 1
		obj['option'] = option
		update_options(obj)

def dec_option():
	ctrl = bge.logic.getCurrentController()
	if ctrl.sensors['Key_Up'].positive:
		obj = ctrl.owner
		option = obj['option']
		option-=1
		if option < 1:
			option = 3
		obj['option'] = option
		update_options(obj)
	
def option_selected():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	option = obj['option']

	if option == 1:
		obj.state = 2


def intro_fade_out():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	light1 = scene.objects['Light1']
	light2 = scene.objects['Light2']

	if light1.energy > 0:
		light1.energy*=0.75

	if light2.energy > 0:
		light2.energy*=0.75

	if light1.energy < 0.0001 and light2.energy < 0.0001:
		obj.state = 4
