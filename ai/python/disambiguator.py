from output import OUT
import copy
import sys

class Disambiguator(object):
    """docstring for Disambiguator"""

    def __init__(self, objects, world, answers):
        self.objects = objects
        self.world = world
        self.answersBackup = copy.deepcopy(answers)
        self.answers = answers

    def getAnswer(self):
        if len(self.answers):
            return self.answers.pop(0)
        else:
            return None

    def answersBackupF(self, offset):
        if offset == -1:
            return self.answersBackup[:-1]
        else:
            return self.answersBackup

    def decode_relation(self, coderel, objid):
        if coderel == [0,1]:
            if objid == "floor":
                return "on"
            if self.objects[objid]['form'] == "box":
                return "inside"
            else:
                return "ontop of" 
        elif coderel == [0,2]:
            return "above"
        elif coderel == [0,-2]:
            return "under"
        elif coderel == [-2,0]:
            return "left"
        elif coderel == [2,0]:
            return "right"
            
        return "beside"
    
    def pddlGoalsDisplay(self, goals):
        pddlgoals = []
        for i,k in enumerate(goals):
          if i != 0:
            pddlgoals.append(str("-----------------"))
          for j,_ in enumerate(goals[i]):            
            if goals[i][j].relations and not goals[i][j].restrictions:
                for g in goals[i][j].relations:
                    rel = self.decode_relation(g[2],g[1][0])
                    pddlgoals.append(str((rel,g[0],g[1])))
                if j < len(k) - 1:
                    pddlgoals.append(str(" or"))
            elif goals[i][j].relations and goals[i][j].restrictions:
                for g1 in goals[i][j].relations:
                    rel = self.decode_relation(g1[2],g1[1][0])
                    pddlgoals.append(str((rel,g1[0],g1[1])))
                pddlgoals.append(str((" holding",goals[i][j].restrictions[0][0])))
                if j < len(k) - 1:
                    pddlgoals.append(str(" or"))
            else:
                pddlgoals.append(str(("hold",goals[i][j].restrictions[0][0])))
                
        return pddlgoals
        
    def characteristicsOfGoal(self,goal):

        l=[]

        if goal.relations:
           G = goal.relations
           r = False
        else:
           G = goal.restrictions
           r = True
           
        for g in G:

            
            
            ori = g[0]
            if not r:
                dst = g[1]

            ori_count = 0
            dst_count = 0
            dic = {}

            if isinstance(ori, basestring): ori = [ori]
            if not r: 
                if isinstance(dst, basestring): dst = [dst]

            ori_form = None
            ori_color = None
            ori_size = None              

            for o in ori:
                ori_count +=1
                ori_form = self.objects[o]['form']
                ori_color = self.objects[o]['color']
                ori_size = self.objects[o]['size']



            dst_form = None
            dst_color = None
            dst_size = None    

            relation = '-'          
            
            if not r:
                for d in dst:
                    dst_count +=1
                    relation = self.decode_relation(g[2],d)
                    if d == 'floor':
                        dst_form = 'floor'
                        dst_size = '-'
                        dst_color = '-'
                    elif dst_form == None and dst_color == None and dst_size == None:
                        dst_form = self.objects[d]['form']
                        dst_color = self.objects[d]['color']
                        dst_size = self.objects[d]['size']
                    elif dst_form != self.objects[d]['form']: dst_form = '-'
                    elif dst_size != self.objects[d]['size']: dst_size = '-'
                    elif dst_color != self.objects[d]['color']: dst_color = '-'

            dic['ori_count']=ori_count
            dic['ori_form']=ori_form
            dic['ori_color']=ori_color
            dic['ori_size']=ori_size

            dic['dst_count']=dst_count
            dic['dst_form']=dst_form
            dic['dst_color']=dst_color
            dic['dst_size']=dst_size

            dic['relation']=relation

            l.append(dic)

        return reduce(self.merge,l)

        # given a goal return
        #   {
        #    ori_count: 1,
        #    ori_form: 'brick',
        #    ori_color: 'yellow',
        #    ori_size: 'large',
        #    dst_count: 3,
        #    dst_form: '-',
        #    dst_color: 'red',
        #    dst_size: '-'
        #   }

    def merge(self,chars1,chars2):
        #
        # ex:   chars1         +       chars2        =>      res
        #   {                     {                     {
        #    ori_count: 1,         ori_count: 1,         ori_count: 1,
        #    ori_form: 'brick',    ori_form: 'brick',    ori_form: 'brick', 
        #    ori_color: 'yellow',  ori_color: 'yellow',  ori_color: 'yellow',  
        #    ori_size: 'large',    ori_size: 'small',    ori_size: '-',    
        #    dst_count: 3,     +   dst_count: 2,     =>  dst_count: '-',         
        #    dst_form: '-',        dst_form: '-',        dst_form: '-',        
        #    dst_color: 'red',     dst_color: 'red',     dst_color: 'red',     
        #    dst_size: '-'         dst_size: '-'         dst_size: '-'         
        #   }                     }                     }
        #
        #  Also chars + None => chars and None + chars => chars
        if chars1 == None:
            return chars2
        elif chars2 == None:
            return chars1
            
        res =  copy.deepcopy(chars1)
        
        parameters = ['relation','ori_count','ori_form','ori_color','ori_size','dst_count','dst_form','dst_color','dst_size']
        
        for p in parameters:        
            if chars1[p] != chars2[p]:
                res[p] = '-'
                
        return res

    def partition(self,goalsWithChars):
        # input: [ ([goal1a,goal1b],chars), ([goal2a,goal2b,goal2c], chars), ([goal3a], chars) ]
        # find a characteristic that splits most of them
        # result ('ori_color', [ ([[goal1a,goal1b],[goal3a]], 'red' ), ([[goal2a,goal2b,goal2c]], 'blue') ] )
   
        parameters = ['ori_form','ori_color','ori_size','dst_form','dst_color','dst_size','relation']

        # Finds the parameter that splits the goals in the maximum number of partitions
        def getPartition(parameter):
            values = map(lambda gc: (copy.deepcopy(gc), gc[1][parameter]),goalsWithChars)
            valueSet = set(map(lambda v: v[1], values))
            if '-' in valueSet: return None
            return (parameter,len(valueSet),values)

        p,l,values = max( filter(lambda e: e != None, map(getPartition ,parameters)), key= lambda e: e[1])

        common_chars = reduce(self.merge, map(lambda gc: gc[1],goalsWithChars))
        
        dic = {}
        for (goals,v) in values:
            if v in dic:
                dic[v].append(goals)
            else:
                dic[v] = [goals]

        tree = [(v,k) for k,v in dic.iteritems()]

        def doRecursion(node):
            subtree,value = node
            if len(subtree) > 1:
                res = self.partition(copy.deepcopy(subtree))
                if len(res[0]) > 1:
                    return (res,value)
            return node

        if l>1:
            tree = map(doRecursion, tree)

        return (p, tree, common_chars)


    def buildQuestion(self,goalTree,tree):
    
        #given the "tree-like" output of partition
        #print goalTree
        options = map(lambda e: e[1],goalTree[1])
        answer = self.getAnswer()

        if len(options)<2:
            OUT.addError("buildQuestion","cannot tell the remaining goals appart")
            return []

        offset = 0
        gtree = None
        if answer:
            for word in answer:
                if word in options:
                    gtree = goalTree[1][options.index(word)][0]

        if gtree:
            if not isinstance (gtree[0], basestring):
                return gtree[0]
            else:
                return self.buildQuestion(gtree,tree)
        elif not gtree and answer:
            OUT.getErr("pickGoals",reset=True)
            OUT.addError("buildQuestion","answer not recognised")
            offset = -1
                      
        if tree[0] == "put":
            destination = tree[1]
            relation = destination[1]            
        elif tree[0] != "take":
            destination = tree[2]
            relation = destination[1]

        if goalTree[2]["relation"] and goalTree[2]["relation"] != '-':
            relation = goalTree[2]["relation"]
            
        ori_form = "object"
        dst_form = "object"
        if goalTree[2]["ori_form"] and goalTree[2]["ori_form"] != '-':
            ori_form = goalTree[2]["ori_form"]
        if goalTree[2]["dst_form"] and goalTree[2]["dst_form"] != '-':
            dst_form = goalTree[2]["dst_form"]

        sep = ','
        # Destination or Origin
        if goalTree[0][0] == "d":
            if goalTree[0][4] == "c":
                question = "Which color is the " + dst_form + " you want to " + tree[0] + " it " + relation + ": "
            elif goalTree[0][4] == "s":
                question =  "Which size is the " + dst_form + " you want to " + tree[0] + " it " + relation + ": "
            else:
                question = relation.capitalize() + " which " + dst_form + " do you want to " + tree[0] + " it " + ": "
                sep = 'a'
        else:
            if goalTree[0][4] == "c":
                question = "Which color is the " + ori_form + " you want to " + tree[0] + ": "
            elif goalTree[0][4] == "s":
                question = "Which size is the " + ori_form + " you want to " + tree[0] + ": "
            elif goalTree[0][4] == "t":
                question = "How should the objects be placed: "
            else:
                question = "Which " + ori_form + " do you want to " + tree[0] + ": " 
                sep = 'a'

        for i,o in enumerate(options):
            sep_t = sep
            if o == "floor":
                sep_t = "the"
            if len(options)>1 and i==(len(options)-1):
                if sep == 'a':
                    question += " or " + sep_t + " " + o
                else:
                    question += " or " + o
            else:
                if sep == 'a':
                    question += sep_t + " " + o
                    if i < (len(options)-2):
                        question += ", "
                else:
                    question += o
                    if i < (len(options)-2):
                        question += ", "
            
        question += "?"
        OUT.prevAnswers = self.answersBackupF(offset)
        OUT.question = question

        return None



    def pickGoals(self,goals,tree):
        ''' call other functions to pick'''
     
            
        if not goals:
            return None
        if len(goals) == 1:
            return goals[0]
        
        OUT.addError("pickGoals","ambiguity error!! ")
        goalchars = map(lambda l: (l,reduce(self.merge,map(self.characteristicsOfGoal,l))),goals)

        res = self.buildQuestion(self.partition(goalchars),tree)
        if res:
            # remove characteristics
            return res[0]
        else:
            OUT.addError("pickGoals",OUT.joinErr("buildQuestion"))
        return res


# TODOS:
#
#  - improve partition_r so that it partitions deeper levels
#  - improve partition_r so that it avoids partitioning on properties with dashes
#  - add a language for answers
#  - create smarter questions

#





        