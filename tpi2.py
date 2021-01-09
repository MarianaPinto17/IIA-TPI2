#encoding: utf8

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MyBN(BayesNet):

    def individual_probabilities(self):
        # IMPLEMENTAR AQUI
        #resultado tem de ser dado na forma de dicionário
        dic = {}
        # para cada variavel presente na rede
        for var in self.dependencies.keys():
            variables = [a for a in self.dependencies.keys() if a != var]
            #calcula-se a probabilidade de cada var usando o jointProb -> Probabilidade conjunta de uma dada conjuncao de valores de todas as variaveis da rede (só as true)
            dic[var] = sum ([self.jointProb([(var,True)] + b) for b in self.conjunctions(variables)])
        return dic

    # função auxiliar adaptada das aulas com o professor DG
    def conjunctions(self, variables):
        # se está vazia retorna lista vazia
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
            formula += "=> " + idx.title() + "(x)"
            result.append(formula)

        return result

    # tive a ajuda do meu colega diogo correia 
    def query_inherit(self,entity,assoc):
        # IMPLEMENTAR AQUI
        result = []
        
        for d in self.declarations:
            if (d.relation.entity1 == entity or d.relation.entity2 == entity) and (d.relation.name == assoc or isinstance(d.relation, Association)\
            and d.relation.inverse == assoc):
                result.append(d)
            if self.predecessor(d.relation.entity2, entity) and not result:
                result.extend(self.query_inherit(d.relation.entity2,assoc))
        return result

    # função auxiliar adaptada das aulas práticas com o professor DG
    def predecessor(self, e1, e2):

        local_predecessor = [d.relation.entity2 for d in self.query_local() if isinstance (d.relation, (Member,Subtype)) \
        and d.relation.entity1 == e2]  

        if e1 in local_predecessor:
            return True
        
        return any([self.predecessor(e1 , pred) for pred in local_predecessor])

    def query(self,entity,relname):
        #IMPLEMENTAR AQUI
        pass
class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        pass


