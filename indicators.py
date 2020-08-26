import bge.logic

def update_score():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	msg_sensor = ctrl.sensors['Message']

	if msg_sensor.positive:
		score = int(msg_sensor.bodies[0])
		obj.text = '%06d' % (score,)

def update_lives():
	ctrl = bge.logic.getCurrentController()
	obj = ctrl.owner

	sensor = ctrl.sensors[0]

	if sensor.positive:
		lives = int(sensor.bodies[0])
		
		for child in obj.children:
			if child['live'] > lives:
				child.visible = False
