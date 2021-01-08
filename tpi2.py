#encoding: utf8

from semantic_network import *
from bayes_net import *
from constraintsearch import *
from itertools import product


class MyBN(BayesNet):

    def individual_probabilities(self):
        # IMPLEMENTAR AQUI
        dic = {}
        for var in self.dependencies.keys():
            variables = [a for a in self.dependencies.keys() if a != var]
            dic[var] = sum ([self.jointProb([(var,True)] + b) for b in self.conjunctions(variables)])
        return dic

    def conjunctions(self, variables):
        lcomb = product([True, False], repeat=len(variables))
        return list(map(lambda c: list(zip(variables, c)), lcomb))

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def translate_ontology(self):
        #IMPLEMENTAR AQUI
        pass

    def query_inherit(self,entity,assoc):
        # IMPLEMENTAR AQUI
        pass

    def query(self,entity,relname):
        #IMPLEMENTAR AQUI
        local = [self.query(d.relation.entity, relname) \
        for d in self.declarations if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype)) and d.relation.entity == entity]

        return [item for sublist in local for item in sublist if isinstance(item.relation, Association)] +\
             self.query_local(entity=entity, relname=relname)

    #aux function to get var parents
    def parents (self,var):
        var_parents = self.dependencies[var]
        # Check for each value of the dictionary all the parent values
        return list(set([prt[0] for key in var_parents.keys() for prt in key]))

    #aux function to get ancestors
    def ancestors (self,var):
        tmpAnc = self.get

class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        pass


