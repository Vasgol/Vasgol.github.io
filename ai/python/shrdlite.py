#!/usr/bin/env python

# Test from the command line:
# python shrdlite.py < ../examples/medium.json

from __future__ import print_function

import sys
import json
import copy

from interpreter import Interpreter
from planner import Planner
from state import State
from output import OUT
from physics import PhysicsInit
from disambiguator import Disambiguator

GRAMMAR_FILE = "shrdlite_grammar.fcfg"


# IMPORTANT NOTE:
# 
# If you are using NLTK 2.0b9 (which is the one that is installed 
# by the standard Ubuntu repository), then nltk.FeatureChartParser
# (in the parse function) fails to parse some sentences! In this 
# case you can use nltk.FeatureTopDownChartParser instead.
# You can check if it is working by calling this:
# 
#   python shrdlite.py < ../examples/small.json
# 
# The program should return "Ambiguity error!". If it instead
# returns "Parse error!", then the NLTK parser is not correct, 
# and you should change to nltk.FeatureTopDownChartParser instead.

def get_tree_label(result):
    """Returns the label of a NLTK Tree"""
    try:
        # First we try with NLTKv3, the .label() method:
        return result.label()
    except AttributeError, TypeError:
        # If that doesn't work we try with NLTKv2, the .node attribute:
        return result.node

def get_all_parses(parser, utterance):
    """Returns a sequence of all parse trees of an utterance"""
    try:
        # First we try with NLTKv2, the .nbest_parse() method:
        return parser.nbest_parse(utterance)
    except AttributeError, TypeError:
        try:
            # Then we try with NLTKv3, the .parse_all() method:
            return parser.parse_all(utterance)
        except AttributeError, TypeError:
            # Finally we try with NLTKv3, the .parse() method:
            return parser.parse(utterance)

def parse(utterance):
    import nltk
    grammar = nltk.data.load("file:" + GRAMMAR_FILE, cache=False)
    parser = nltk.FeatureChartParser(grammar)
    try:
        return [get_tree_label(result)['sem'] 
                for result in get_all_parses(parser, utterance)]
    except ValueError:
        return []


def solve(goals, world, holding, objects):
    
    planner = Planner(State(copy.deepcopy(world),holding,None,0,None), goals)
    return planner.aSearch()
    


def main(utterance, world, holding, objects, **other_params):
    answers = []
    answer = None
    if other_params:    
        if "prevAnswers" in other_params:
            prevAnswers = eval(json.dumps(other_params["prevAnswers"]))
            answers.extend(prevAnswers)
        if "answer" in other_params:
            answer = eval(json.dumps(other_params["answer"]))
            answers.append(answer)

    # Try to parse answer to see if user wnats some other thing
    if answer: 
        if parse(answer):
            utterance = answer
            answer = None
            answers = []

        
    OUT['utterance'] = utterance

    world = eval(json.dumps(world))
    objects = eval(json.dumps(objects))
    if holding:
        holding = eval(json.dumps(holding))
    PhysicsInit(objects)

    ### -- PARSE --

    trees = parse(utterance)
    OUT['trees'] = [str(t) for t in trees]

    if not trees:
        OUT['output'] = "Parse error!"
        return OUT.output()

    OUT.log("Parsed!!")


    ### -- INTERPRET --
    
    interpreter = Interpreter(world, holding, objects)
    goals = [goal for tree in trees for goal in interpreter.interpret(tree)]

    if not goals:
        OUT['output'] = OUT.joinErr("interpret") or "Cannot %s!" % ' '.join(map(str,eval(json.dumps(utterance))))
        return OUT.output()   
        
    OUT.log('Interpreted!!')


    ### -- DISAMBIGUATE --

    disambiguator = Disambiguator(objects, world, answers)
    OUT.goals = disambiguator.pddlGoalsDisplay(goals)  
    goals = disambiguator.pickGoals(goals,tree)

    if not goals:
        OUT['output'] = OUT.joinErr("pickGoals") or "Cannot %s!" % ' '.join(map(str,eval(json.dumps(utterance))))
        return OUT.output()

    OUT.log('Disambiguated!!')
    OUT.goals = disambiguator.pddlGoalsDisplay([goals])


    ### -- PLAN --

    OUT['plan'] = plan = solve(goals, world, holding, objects)

    if not len(plan):
        OUT['output'] = "Already done."
        return OUT.output()
    elif not plan:
        OUT['output'] = "Planning error!"
        return OUT.output()


    OUT.log('Planned!!!')
    OUT['output'] = "Success!"
    return OUT.output()


if __name__ == '__main__':
    input = json.load(sys.stdin)
    output = main(**input)
    # json.dump(output, sys.stdout)
    # json.dump(output, sys.stdout, sort_keys=True, indent=4)
    print("{", ",\n  ".join('%s: %s' % (json.dumps(k), json.dumps(v))
                            for (k, v) in output.items()), "}")
