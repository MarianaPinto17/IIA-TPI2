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

    # função auxiliar adaptada das aulas com o professor DG
    def conjunctions(self, variables):
        if variables == []:
            return [[]]

        aux = []
        for conj in self.conjunctions(variables[1:]):
            aux.append([(variables[0], True)] + conj)
            aux.append([(variables[0], False)] + conj)

        return aux

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def translate_ontology(self):
        #IMPLEMENTAR AQUI
        dic = {}
        result = []
        for d in self.declarations:
            if isinstance(d.relation,Subtype):
             #fazemos um dicionario em que as keys são as entity2 e os valores são os valores entity1 ligados a entity2
                if d.relation.entity2 not in dic:   
                    dic[d.relation.entity2] = [d.relation.entity1]
                elif d.relation.entity1 not in dic[d.relation.entity2]:
                    dic[d.relation.entity2] += [d.relation.entity1]
        # dicionario ordenado alfabeticamente
        for idx in sorted(dic.keys()):
            #construção das traduções
            formula = "Qx "
            ordered = sorted(dic[idx])
            for val in ordered:
                if val != ordered[-1]: 
                   formula += val.title() + "(x) or "
                else:
                    formula += val.title() + "(x) "
            formula += "=> " + val.title() + "(x)"
            result.append(formula)

        return result


    def query_inherit(self,entity,assoc):
        # IMPLEMENTAR AQUI
        local = [self.query(d.relation.entity2,assoc) for d in self.declarations if d.relation.name in ["member","subtype"] and d.relation.entity1==entity]

        return [item for sublist in local for item in sublist] + [d for d in self.declarations if d.relation.entity1 == entity and d.relation.name == assoc]

    def query(self,entity,relname):
        #IMPLEMENTAR AQUI
        local = [self.query(d.relation.entity2, relname) for d in self.declarations \
        if (isinstance(d.relation, Member) and isinstance(d.relation, Subtype)) and isinstance(d.relation,Association) and d.relation.entity == entity]

        return [item for sublist in local for item in sublist if isinstance(item.relation, relname)] + self.query_local(e1=entity, relname=relname)

class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        pass


