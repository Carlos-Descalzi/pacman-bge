import bge.logic

def create_points():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner
	scene = bge.logic.getCurrentScene()
	
	new_points = scene.addObject('Points',obj)
	new_points.worldPosition = obj.worldPosition
	new_points['points'] = obj['points']


def init_points():
	scene = bge.logic.getCurrentScene()
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	text = str(obj['points']).replace(' ','0')

	letters = []
	x = 0
	for c in text:
		letter = scene.addObject('Text_'+c,obj)
		letter.setParent(obj)	
		letter.localPosition.x+=x+letter['w']/2
		x+=letter['w']+0.05
		letters.append(letter)

	offset = (x-0.05)/2

	for letter in letters:
		letter.localPosition.x-=offset

