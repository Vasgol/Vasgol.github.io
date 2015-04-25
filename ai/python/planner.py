from state import State
from output import OUT

class Planner(object):

	def __init__(self, init_state, goals):
		init_state.calcHValue(goals)
		self.frontier = {}
		self.frontier[init_state] = init_state
		self.goals = goals
		self.visited = {}
		self.visited[init_state] = init_state
	

	def aSearch(self):
		frontier = self.frontier
		visited = self.visited

		while len(frontier):
			current = min(frontier,key=lambda o: o.depth + o.h_value)
			if current.h_value == 0:
				return self.planOutput(self.getPathTo(current))

			#OUT.log((self.getPathTo(current),current.depth,current.h_value))
			del frontier[current]
			visited[current] = True
			for state in current.neighbours():
				if state in visited: continue
				if state in frontier:
					state_prime = frontier[state]
					if state.depth < state_prime.depth:
						state.calcHValue(self.goals)
						frontier[state] = state

				else:
					state.calcHValue(self.goals)
					frontier[state] = state
		OUT.setErr("It is impossible to reach the goal.")
		return []

	def getPathTo(self, node):
		path = []
		while node.prev_state:
			path.append(node.ori_movement)
			node = node.prev_state
		path.append(node.ori_movement)
		return path[::-1]


	def planOutput(self, path):
		plan = []
		for mov in path:
			if mov:
				mov_type,dst = mov
				if mov_type == "pick":
					plan.extend(["I pick up from %d . . ." % dst, 'pick %d' % dst])
				else:
					plan.extend([". . . and I drop down in %d" % dst, 'drop %d' % dst])
		#OUT.log("plan found")
		return plan





