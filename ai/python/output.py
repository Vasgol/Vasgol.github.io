import pprint
import re

class AIOutput(dict):
    """class meant as a singleton for helping with the output"""
    
    def init(self):
        self.log("")
        self.log("")
        self.log("")
        self.log("")
        self.log("---------------------------------------------------------------------------------")
        self.log("")
        self.log("")
        self.error_dic = {}

    # Error outout handling functions

    def addError(self, k,v, reset=False):
        if not v.strip():
            return
        if not reset and k in self.error_dic:
            self.error_dic[k].append(v)
        else:
            self.error_dic[k] = [v]

    def getErr(self, k, reset=False):
        if not k in self.error_dic:
            return []
        res = self.error_dic[k]
        if reset:
            del self.error_dic[k]
        return res

    def joinErr(self, k, separator=" and ", reset=False):
        errors = self.getErr(k,reset) or []
        return separator.join(errors)

    def setErr(self,string):
        self['error'] = string


    # General ouput functions

    def output(self):
        self.output = re.sub(r'(\s)\1+', r'\1', self['output'].strip() + ".").capitalize()
        return self

    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        return self[k]
        
    def log(self, v):
        f = open('./log.txt','a')
        pp = pprint.PrettyPrinter(indent=4,stream = f)
        pp.pprint(v)


    # Parse tree to string

    def treeStr(self,tree):
        action, mo, dst = None,None,None
        if tree[0] == "take":
            action, mo = tree
        elif tree[0] == "put":
            action, dst = tree
        else:
            action, mo, dst = tree

        return " ".join([action, self.entityStr(mo), self.movementStr(dst)])

    def entityStr(self,entity,begin=False):
        if entity == None:
            return ""

        if entity == "floor":
            return "the floor"

        etype, quant, obj, rel = None,None,None,None
        if entity[0] == "basic_entity":
            etype, quant, obj = entity
        else:
            etype, quant, obj, rel = entity

        plural = False
        if quant == "all":
            plural = True 

        return " ".join([quant,self.charStr(obj,plural),self.relationStr(rel,plural)])


    def charStr(self, characteristics, plural):
        _, form, size, color = characteristics
        if form == "anyform":
            form = "object"
        if size == "-":
            size = ""
        if color == "-":
            color = ""

        if plural:
            if form == "box":
                form += "e"
            form += "s"

        return " ".join([size,color,form])

    def relationStr(self,relation,plural,begin=False):
        if relation == None:
            return ""
        _, relPos, related = relation
        begining = "that is"
        if plural:
            begining = "that are"

        return " ".join([begining,relPos,self.entityStr(related)])

    def movementStr(self, movement,begin=False):
        if movement == None:
            return ""
        _, relPos, related = movement
        return " ".join([relPos,self.entityStr(related)])
        

OUT = AIOutput()
OUT.init()
    
        