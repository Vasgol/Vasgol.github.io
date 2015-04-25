import make_json_serializable
import sys
import copy
from physics import Physics


class State(object):

    # Class Functions
    def __init__(self,world,holding,prev_state,depth,ori_movement):
        self.world = world
        self.holding = holding
        self.prev_state = prev_state
        self.depth = depth
        self.ori_movement = ori_movement


    def neighbours(self):
        '''
        Given a state it generates all the possible states we can
        reach moving each object from the top of the stack to another one
        '''
        if self.holding:
            return self.droppingNeighbours()
        else:
            return self.pickingNeighbours()

    def droppingNeighbours(self):
        '''
        Given a picture of the world it generates
        all the possible states just by placing
        the "element" at the top of every step
        with respect to the physical laws
        '''
        element = self.holding
        n_set = []
        usedFloor = False
        for i,stack in enumerate(self.world):
            if len(stack)==0:
                if usedFloor:
                    continue
                usedFloor = True
            n_world = copy.deepcopy(self.world)
            n_world[i].append(element)
            n_state = State(n_world, None, self, self.depth + 1, ('drop',i))
            if n_state.valid(element, i):
                n_set.append(n_state)
        return n_set

    def pickingNeighbours(self):
        n_set = []
        notuseful = None
        if self.ori_movement:
            _,notuseful = self.ori_movement
        for i,stack in enumerate(self.world):
            if notuseful==i or len(stack) == 0:
                continue
            n_world = copy.deepcopy(self.world)
            held = self.take_top_of_stack(n_world[i])
            if held:
                n_set.append(State(n_world,held,self,self.depth+1,('pick',i)))
        return n_set

    def take_top_of_stack(self,stack):
        '''
        Given the wolrd and a stack it returns the object 
        at the top of the stack (inside a tuple along with
        a boolean indicating wether it is the moved object.
        None otherwise
        '''
        return stack.pop()

    # Checks if the neighbour state is valid invoking physics class
    def valid(self,element,target_index):
        # If stack is not empty
        if len(self.world[target_index]) > 1:
            # Check if physical laws are obeyed 
            return Physics().checkPhysicalLaws(element, self.world[target_index][len(self.world[target_index])-2], "dropped", False)
        return True

    def calcHValue(self,goals):
        self.h_value = min(map(lambda goal: goal.hValue(self),goals))


    #For detecting correctly duplicated states
    def compressedRepr(self):
        return [str(stack) for stack in self.world if len(stack)>0]

    def __eq__(self,other):
        return self.compressedRepr() == other.compressedRepr() and self.holding == other.holding

    def  __hash__(self):
        return hash(str((self.compressedRepr(),self.holding)))

    def __repr__(self):
        return str([self.holding,self.world,self.depth])

    def to_json(self):
        return self.world


        