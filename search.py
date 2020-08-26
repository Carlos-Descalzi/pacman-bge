import math
import random

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.g = 0
		self.f = 0

	def __getitem__(self,key):
		if key == 0: return self.x
		if key == 1: return self.y
		raise IndexError()
		
	def __eq__(self,other):
		return self.x == other.x and self.y == other.y
	
	def __hash__(self):
		return hash(self.x*1000+self.y)

	def distance(self,other):
		x = self.x-other.x
		y = self.y-other.y
		return math.sqrt(x*x+y*y)

	def __str__(self):
		return "%d,%d" % (self.x,self.y)

	def __sub__(self,other):
		return Point(self.x-other.x,self.y-other.y)

	def __repr__(self):
		return str(self)

	def neightbors(self):
		return [
			(self.x-1,self.y),
			(self.x+1,self.y),
			(self.x,self.y-1),
			(self.x,self.y+1)
		]

class LevelMap:
	def __init__(self,level_map):
		self.map = level_map
		self.paths = {}
		self.map_height = len(level_map)
		self.map_width = max([len(l) for l in level_map])
		self.outputs = []
		self.home = None
		self.free_places = []
		self.phantom_positions = {}

		for i,line in enumerate(self.map):
			for j,c in enumerate(line):
				pos = (j,i)
				self.paths[pos] = c in ' -.*+OX1234'
				if c in ' .*OX': self.free_places.append(pos)
				if c == 'O': self.outputs.append(pos)
				if c == '1': self.home = pos
				if c in '1234': self.phantom_positions[c] = pos

	def get_map():
		return self.map

	def get_phantom_positions(self):
		return self.phantom_positions

	def get_phantom_outputs(self):
		return self.outputs

	def path_to_home(self,s):
		return self.get_path(s,self.home)

	def random_path(self,s):
		target = random.choice(self.free_places)
		path = self.get_path(s,target)
		return path

	def get_path(self,b,t):
		begin = Point(b[0],b[1])
		target = Point(t[0],t[1])
		
		closed_set = set()
		open_set = set([begin])
		came_from = {}
		
		begin.g = 0
		begin.f = begin.distance(target)

		points = {}
		
		points[(begin.x,begin.y)] = begin
		points[(target.x,target.y)] = target

		while len(open_set):

			current = min(open_set,key=lambda p: p.f)
			
			if current == target:
				return self.build_path(came_from,target)

			open_set.remove(current)
			closed_set.add(current)
			
			for neightbor in self.neightbors(current,points):

				g = current.g + 1
				f = g + math.pow(neightbor.distance(target),2)

				if neightbor in closed_set and f >= neightbor.f:
					continue
				
				if not neightbor in open_set or f < neightbor.f:
					came_from[neightbor] = current
					neightbor.g = g
					neightbor.f = f
					open_set.add(neightbor)
		
		return None

	def neightbors(self,point,points):
		result = []

		for x,y in point.neightbors():
			if x >= 0 and y >= 0 and x < self.map_width and y < self.map_height and self.paths[(x,y)]:
				pos = (x,y)
				if pos in points:
					neightbor = points[pos]
				else:
					neightbor = Point(x,y)
					points[pos] = neightbor
				result.append(neightbor)
		return result

	def build_path(self,came_from,end):

		steps = [end]

		while end in came_from:
			p = came_from[end]			
			steps.insert(0,p)
			end = p		

		path = [steps.pop(0)]

		direction = None
		while len(steps) > 0:
			step = steps.pop(0)
			if not direction:
				direction = step - path[len(path)-1]
				path.append(step)
			else:
				current_direction = step - path[len(path)-1]
				if direction == current_direction:
					path.pop(len(path)-1)
				else:
					direction = current_direction
				path.append(step)

		return path

