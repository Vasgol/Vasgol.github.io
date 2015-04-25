import sys
from output import OUT

class PhysicsChecker(object):

    def __init__(self,objects):
        self.objects = objects

    # Checks Physical Laws
    def checkPhysicalLaws(self, mobject_id, tobject_id, relation, outErrors=True):
        if tobject_id == "floor":
            return (relation=="ontop" or relation=="inside" or relation=="dropped")
    
        mobject = self.objects[mobject_id]
        tobject = self.objects[tobject_id]
        # Balls can be inside only in boxes
        if (mobject['form']=="ball" and relation=="inside") and tobject['form']!="box":
            if (outErrors):
                OUT.setErr("Balls can only be inside boxes.")
            return False
        # Balls cannot be under anything
        if (mobject['form']=="ball" and relation=="under"):
            return False
        # Objects are considered inside boxes and not ontop
        if relation == "ontop" and tobject['form']=="box":
            return False
        # Objects can be inside only boxes
        if relation == "inside" and tobject['form']!="box":
            return False
        # Balls are supported only by boxes
        if (mobject['form']=="ball" and (relation=="ontop" or relation=="inside" or relation=="dropped")) and tobject['form']!="box":
            return False
        # Balls can't support anything ontop
        if (relation =="ontop" or relation=="inside" or relation=="above" or relation=="dropped") and tobject['form']=="ball":
            return False
        # Small objects cannot support large objects
        if (relation == "ontop" or relation=="inside" or relation=="above" or relation=="dropped") and (mobject['size']=="large" and tobject['size'] == "small"):
            return False
        if (relation == "under") and (mobject['size']=="small" and tobject['size'] == "large"): 
            return False
        # Boxes cannot contain pyramids or planks of the same size
        if ((mobject['form']=="plank" or mobject['form']=="pyramid") and tobject['form']=="box") and (mobject['size']==tobject['size']) and (relation == "inside" or relation=="dropped"):
            return False
        # Large boxes can be supported by large bricks, planks and tables of the same size, if not large only by planks and tables
        if (relation == "ontop" or relation=="inside" or relation=="above" or relation=="dropped") and (mobject['form']=="box" and tobject['form']!="table" and tobject['form']!="plank"):
            if mobject['size'] == "large" and (tobject['form']!="brick" or tobject['size']!="large"):
               return False
        elif (relation == "ontop" or relation=="inside" or relation=="above" or relation=="dropped") and (mobject['form']=="box" and (tobject['form']=="table" or tobject['form']=="plank")):
            if mobject['size'] != tobject['size']:
               return False
        
        return True

physics_instance = None

def PhysicsInit(objects):
    global physics_instance
    physics_instance = PhysicsChecker(objects)

def Physics():
    return physics_instance