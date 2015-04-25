import copy
from state import State
from goal import Goal
from physics import Physics
from output import OUT


# CONSTANTS TO PARSE THE UTERANCE

TREE_ACTION_FIELD = 0
TREE_ENTITY_FIELD = 1
TREE_DESTINATION_FIELD = 2

TREE_ENTITY_TYPE_FIELD = 0
TREE_ENTITY_QUANTIFIER_FIELD = 1
TREE_ENTITY_CHARS_FIELD = 2
TREE_ENTITY_REL_FIELD = 3

TREE_RELATION_DESC_FIELD = 1
TREE_RELATION_OTHER_FIELD = 2

TREE_CHARS_FORM_FIELD = 1
TREE_CHARS_SIZE_FIELD = 2
TREE_CHARS_COLOR_FIELD = 3


class Interpreter(object):
    """Class in charge of interpreting the user's uterance and
       coming up with the appropiate goals for the planner."""

    def __init__(self, world, holding, objects):
        super(Interpreter, self).__init__()
        self.world = copy.deepcopy(world)
        self.holding = holding
        self.objects = objects
    

    def movedObject(self,tree):
        ''' Find the disambiguation list of possible objects
            to be moved, as described by the users utterance '''
        if tree[TREE_ACTION_FIELD] == "put":
            if not self.holding:
                OUT.addError("movedObject","I don't have any object on the arm.")
                return ([],'the')
            return ([[(self.holding,[0,0])]],'the')  
        tree_entity = tree[TREE_ENTITY_FIELD]
        res =  self.findObject(tree_entity)       
        if not res[0]:
            OUT.addError("movedObject","cannot find " + OUT.entityStr(tree_entity))
        return res
    

    def checkCharacteristics(self,object, characteristics):
        '''Checks if an objects fits the charasteristics (form,size,color)'''
        if characteristics[TREE_CHARS_FORM_FIELD] != '-' and characteristics[TREE_CHARS_FORM_FIELD] != object['form'] and characteristics[TREE_CHARS_FORM_FIELD]!= "anyform":
            return False
        if characteristics[TREE_CHARS_SIZE_FIELD] != '-' and characteristics[TREE_CHARS_SIZE_FIELD] != object['size']:
            return False
        if characteristics[TREE_CHARS_COLOR_FIELD] != '-' and characteristics[TREE_CHARS_COLOR_FIELD] != object['color']:
            return False
        return True


    def checkRelation(self,pos1,pos2,relation):
        '''Checks that the objects on two given positions match the relation specified'''
        if pos2 == 'floor':
            return pos1[1] == 0

        if pos1[0] == -1 or pos2[0] == -1:
            return 0

        rel_pos = relation[TREE_RELATION_DESC_FIELD]

        if rel_pos == "ontop" or rel_pos == "inside":
            return pos2[0] == pos1[0] and pos1[1] == pos2[1] + 1
            
        elif rel_pos == "under":
            return pos2[0] == pos1[0] and pos1[1] < pos2[1]
        # Above 
        elif rel_pos == "above":
            return pos2[0] == pos1[0] and pos1[1] > pos2[1]
        # Right of 
        elif rel_pos == "rightof":
            return pos1[0] > pos2[0]
        # Left of 
        elif rel_pos == "leftof":
            return pos1[0] < pos2[0]
        # Beside
        elif rel_pos == "beside":                
            return abs(pos2[0] - pos1[0]) == 1

        return False


    def checkObject(self,description,obj_id,position):
        ''' Checks if an Object fits a description and returns True if yes, either false '''
        if obj_id == 'none':
            return None
        # Basic or Relative Entity
        entity_type = description[TREE_ENTITY_TYPE_FIELD]
        # Form, Size, Color
        characteristics = description[TREE_ENTITY_CHARS_FIELD]
        # Initialize boolean for the physical laws
        laws = True
        
        if not self.checkCharacteristics(self.objects[obj_id],characteristics):
            return None

        # If it is relative entity, the relative object is checked
        if entity_type == "relative_entity":
            # Relative object
            relation = description[TREE_ENTITY_REL_FIELD]
            related_description = relation[TREE_RELATION_OTHER_FIELD]

            possibly_related, quantifier = self.findObject(related_description)
            dic = {}
            for l in possibly_related:
                for rel,pos in l:
                    dic[rel] = (rel,pos)
            possibly_related = [dic[k] for k in dic]

            res = [self.checkRelation(position,rel[1],relation) for rel in possibly_related]
            
            if quantifier == "all":
                if all(res):
                    return ["all"]
                else:
                    return None
            elif quantifier == "any":
                if any(res):
                    return ["any"]
                else:
                    return None
            else:
                # List of ids for wich checkRelation has been true.
                return [possibly_related[i][0] for i,b in enumerate(res) if b]


        return ["norel"]
        

    # 
    def findObject(self,description):
        '''Finds and returns a disambiguation list of objects in the World that fit a destination description'''
        # the, any or all
        quantifier = description[TREE_ENTITY_QUANTIFIER_FIELD]
        # Check every object in the world
        if description == "floor":
            return ([[('floor','floor')]],"the")
        
        dic = {}
        extendedWorld = self.world
        if self.holding:
            extendedWorld = self.world + [self.holding]
        #OUT.log(extendedWorld)
        for i,stack in enumerate(extendedWorld):
            for j,obj in enumerate(stack):
                pos = [i,j]
                if i == len(self.world):
                    pos = [-1,0]
                rIds = self.checkObject(description,obj, pos)
                if rIds:
                    for rId in rIds:
                        if not rId in dic:
                            dic[rId] = []
                        dic[rId].append((obj, pos))

        def unique(seq):
            seen = set()
            seen_add = seen.add
            def keyf(x): return ''.join(sorted(map(lambda e: e[0],x)))
            return [ x for x in seq if keyf(x) not in seen and not seen_add(keyf(x))]

        res = unique([dic[a] for a in dic])
        return (res, quantifier)
 
    def goals(self,mobjects,tree):
        '''Creates a disambiguation list with the possible goals for the planner'''
        mobject_list, mo_quantifier = mobjects
        mobject_list = [[obj for obj,_ in l] for l in mobject_list]

        res = []

        if mo_quantifier == "all":
            res = [[op] for op in mobject_list]
        elif mo_quantifier == "any":
            res = mobject_list
        else: #the
            res = [[ob] for ls in mobject_list for ob in ls]

        restriction = None

        # Grasp with the arm only
        if tree[TREE_ACTION_FIELD] == "take":
            if mo_quantifier == "all":
                OUT.addError("goals","cannot take more than one object")
                return []
            res_final = [[ Goal() for e in l ] for l in res]
            for i,l in enumerate(res_final):
                for j,e in enumerate(l):
                    e.addRestriction(res[i][j][0], -1)
            return res_final

        # drop the held object
        elif tree[TREE_ACTION_FIELD] == "put":
            destination = tree[1]
            
        else:
            destination = tree[2]
            if self.holding:
                restriction = (self.holding,-1) 
            


        # Load destination objects 
        relation = destination[1]
        description = destination[2]
        dest_list, dest_quantifier = self.findObject(description)
        dest_list = [[obj for obj,_ in l] for l in dest_list]

        if not dest_list:
            OUT.addError("goals", "cannot find any " + OUT.entityStr(description) + " to " + tree[TREE_ACTION_FIELD] + " it/them " + relation)
            return []

        # Process the second cuantifier

        if dest_quantifier == "all":
            # mobject_list = [['e'],['a']] || [['e','a']]
            # res = [[('e',list)],[('a',list)]] || [[('e',list),('a',list)]]
            #dest_list = [ e for l in dest_list for e in l ] #flatten
            res = [ [(e,l2,'all') for e in l] for l2 in dest_list for l in res]

        elif dest_quantifier == "any":
            # mobject_list = [['e'],['a']] || [['e','a']] || [ [['e','a']],[['e']] ]
            res = [ [(e,l2,'any') for e in l] for l2 in dest_list for l in res]

        else: #the
            res = [ [(e,e2,'the') for e in l] for l2 in dest_list for e2 in l2 for l in res]


        # Calc movement delta

        delta_x,delta_y = 0,0

        if relation == "ontop" or relation == "inside":
            delta_y = 1

        elif relation == "above":
            delta_y = 2
                
        elif relation == "under":
            delta_y = -2
            
        elif relation == "leftof":
            delta_x = -2

        elif relation == "rightof":
            delta_x = 2
            
        elif relation == "beside":
            delta_x = 1 # 1 == -1 in this case

        delta_pos = [delta_x,delta_y]
            
        # Build a goal for each possibility
        res = map(lambda l: map(lambda e: self.buildGoal(e,delta_pos,relation,restriction), l),res)
        res = [[e for e in l if e] for l in res if len([e for e in l if e])]
        if not res:
            OUT.addError("goals","it is impossible to "+OUT.treeStr(tree))
        return res


    def buildGoal(self, e, pos, relation, restriction):
        ''' create a goal based on a pair of objects or lists of objects
            by adding relations to a new goal'''
        ori,dst,q = e

        if isinstance(ori, basestring): ori = [ori]
        if isinstance(dst, basestring): dst = [dst]

        g = Goal()

        if restriction and (restriction[0] not in ori + dst):
            g.addRestriction(restriction[0],restriction[1])
        
        if q == 'any' and "".join(sorted(ori)) == "".join(sorted(dst)):
            dst.pop()
        
        for o in ori:
            if q == 'any':
                n_dst = copy.deepcopy(dst)
                nn_dst = copy.deepcopy(n_dst)
                for d in n_dst:
                    if d == o or not Physics().checkPhysicalLaws(o, d, relation, False):
                        nn_dst.remove(d)
                if len(nn_dst) > 0:
                    g.addRelation(o,nn_dst,pos)
            else:
                for d in dst:
                    if d == o or not Physics().checkPhysicalLaws(o, d, relation, False):
                        return None
                    g.addRelation(o,d,pos)

        if not len(g.relations):
            return None
       
        return g

    def interpret(self,tree):
        moved_objects = self.movedObject(tree) # return a list of possible objects to move.
        if not moved_objects[0]:
            OUT.addError("interpret",OUT.joinErr("movedObject",reset=True))
            return []
        goals = self.goals(moved_objects,tree)
        if not goals:
            OUT.addError("interpret",OUT.joinErr("goals"))
            return []
        return goals
