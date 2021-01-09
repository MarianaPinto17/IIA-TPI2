#encoding: utf8

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MyBN(BayesNet):

    def individual_probabilities(self):
        # IMPLEMENTAR AQUI
        # resultado tem de ser dado na forma de dicionário
        dic = {}
        # para cada variavel presente na rede
        for var in self.dependencies.keys():
            variables = [a for a in self.dependencies.keys() if a != var]
            # calcula-se a probabilidade de cada var usando o jointProb -> Probabilidade conjunta de uma dada 
            # conjuncao de valores de todas as variaveis da rede (só as true)
            dic[var] = sum ([self.jointProb([(var,True)] + b) for b in self.conjunctions(variables)])
            #retornar um dicionário
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
            #fazemos um dicionario em que as keys são as entity2 e os valores são os valores entity1 ligados 
            # a entity2
                # se a entity2 não está no dic criamos uma nova entrada
                if d.relation.entity2 not in dic:   
                    dic[d.relation.entity2] = [d.relation.entity1]
                # se houver uma entrada já e entity1 não tiver ainda relação com entity2 adiciona-se a relação
                elif d.relation.entity1 not in dic[d.relation.entity2]:
                    dic[d.relation.entity2] += [d.relation.entity1]
        # dicionario ordenado alfabeticamente
        # para cada indice (entity2) do dicionário
        for idx in sorted(dic.keys()):
            #construção das traduções
            # formula é inicializada com o quantificador
            formula = "Qx "
            # ordena-se os indices do dicionário para ambos os subtipos e supertipos ficaram ordenados por 
            # ordem alfabética
            ordered = sorted(dic[idx])
            # se o val está em ordered (ou seja, se há relação entre entity2 e entity1)
            for val in ordered:
                # enquanto val não for igual ao ultimo valor correspondente da key ao valor
                if val != ordered[-1]: 
                    # há mais entity1 para entrar
                   formula += val.title() + "(x) or "
                #quando for o último é porque não há mais entity1 para entrar
                else:
                    formula += val.title() + "(x) "
            #adiciona-se o indíce do dicionário (Resultado da fórmula)
            formula += "=> " + idx.title() + "(x)"
            result.append(formula)
        #retorna-se o resultado
        return result

    # tive a ajuda do meu colega diogo correia para me guiar. adaptei a questão 11b) das aulas práticas e 
    # fazendo os ajustes para ter em conta as relações inversas e associações com os prodeceddores
    def query_inherit(self,entity,assoc):
        # IMPLEMENTAR AQUI
        result = []
        
        for d in self.declarations:
            # se trata uma relação inversa
            if (d.relation.entity1 == entity or d.relation.entity2 == entity) and (d.relation.name == assoc \
            or isinstance(d.relation, Association) and d.relation.inverse == assoc):
                result.append(d)
            # se é predecessor (ou seja, existe relação (TRUE) entre entity2 e entity) e ainda não está no  
            # result (para não repetir resultados)
            if self.predecessor(d.relation.entity2, entity) and not result:
                result.extend(self.query_inherit(d.relation.entity2,assoc))    
        return result

    # função auxiliar adaptada das aulas práticas com o professor DG - função que, dadas duas entidades devolva 
    # True se a primeira for predecessora da segunda, e False caso contrário.
    def predecessor(self, e1, e2):
        # procura os local predecessor
        local_predecessor = [d.relation.entity2 for d in self.query_local() \
        if isinstance (d.relation, (Member,Subtype)) and d.relation.entity1 == e2]  
        # se a entidade 1 estiver nos local_predecessor a primeira é predecessora da segunda
        if e1 in local_predecessor:
            return True
            #retorna todos os predecessores
        return any([self.predecessor(e1 , pred) for pred in local_predecessor])

    def query(self,entity,relname):
        #IMPLEMENTAR AQUI
        


class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        pass


