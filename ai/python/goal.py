def find(state, id):
    if id == state.holding:
        return [-1,0]
    for i,stack in enumerate(state.world):
        for j,obj in enumerate(stack):
            if obj == id:
                return [i,j]
    return None



class Goal(object):

    def __init__(self):
        self.relations = []
        self.restrictions = []
        self.counter = 0

    def addRelation(self, ori, dst, delta_pos):
        if isinstance(dst,basestring): dst = [dst]
        self.relations.append((ori,dst,delta_pos))

    def addRestriction(self, oid, pos):
        self.restrictions.append((oid,pos))

    def hValue(self, state):
        res = 0
        for relation in self.relations:
            res += self.hRelation(relation, state)
        for restriction in self.restrictions:
            res += self.hRestriction(restriction,state)
        if res != 0 and state.holding:
            res += 1
        return res
        
    def hRelation(self, relation, state):
        ori, dst, delta_pos = relation
        return min(map(lambda d: self.hRelation_ele(ori, d[1], delta_pos, state),enumerate(dst)))

    def hRelation_ele(self, ori, dst, delta_pos, state):
        delta_stack = delta_pos[0]
        delta_v = delta_pos[1]

        def nOnTop(stack,pos,addOne=False):
            if stack == -1:
                res = 0
            else:
                res = abs(len(state.world[stack]) - (pos + 1))
            if addOne:
                res += 1
            return 2*res


        ori_pos = find(state, ori)
        if dst == 'floor':
            dst_pos0,_ = min(enumerate(state.world),key=lambda s: len(s[1]))
            dst_pos = [dst_pos0,-1]
            if ori_pos[1] == 0 and ori_pos[0] != -1:
                return 0
        else:
            dst_pos = find(state, dst)

        if delta_v != 0:

            if delta_v > 0:
                pos1 = ori_pos
                pos2 = dst_pos
            else:
                pos1 = dst_pos
                pos2 = ori_pos

            if abs(delta_v) == 1:
                if pos1[0] == pos2[0] and pos1[1] == (pos2[1] + 1) :
                    return 0
                return nOnTop(pos1[0], pos1[1]+1, True) + nOnTop(pos2[0], pos2[1])
            else:
                if pos1[0] == pos2[0] and pos1[1] > pos2[1] :
                    return 0
                return nOnTop(pos1[0], pos1[1]+1, True)

        if delta_stack != 0:

            if delta_stack > 0:
                pos1 = ori_pos
                pos2 = dst_pos
            else:
                pos1 = dst_pos
                pos2 = ori_pos

            if pos1[0] == -1 or pos2[0] == -1:
                return 1

            if abs(delta_stack) == 1 and (pos1[0] == pos2[0] + 1 or pos1[0] == pos2[0] - 1):
                    return 0
            elif abs(delta_stack) == 2 and pos1[0] > pos2[0]:
                    return 0

            return nOnTop(pos1[0], pos1[1]+1, True)


    def hRestriction(self, restriction, state):

    	oid,stack = restriction
        pos = find(state, oid)

    	if pos[0] == stack:
    		return 0
    	else:
    		return 1 + (abs(len(state.world[pos[0]]) - (pos[1] + 1)))


    def __repr__(self):
        return str((self.relations,self.restrictions))

    def to_json(self):
        return [self.relations,self.restrictions]

        