#encoding: utf8
# sites consultados pergunta 4: 
# https://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list
# https://www.guru99.com/python-counter-collections-example.html
# https://stackoverflow.com/questions/54664102/find-the-nth-most-common-word-and-count-in-python

# sites consultados pergunta 5: 
# https://stackoverflow.com/questions/1024847/how-can-i-add-new-keys-to-a-dictionary
# https://stackoverflow.com/questions/41063744/how-to-update-the-value-of-a-key-in-a-dictionary-in-python
#
#



from semantic_network import *
from bayes_net import *
from constraintsearch import *
from collections import Counter

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
        # guardamos as propriedades de cada associação
        prop = []
        result = []
        for d in self.declarations:  
            # se o relname for subtype ou member faz-se normalmente como na anterior
            if relname == "subtype" or relname == "member":      
                if d.relation.entity1==entity and isinstance(d.relation,Subtype) :
                    result.append(d.relation.entity2)
                elif d.relation.entity1==entity and isinstance(d.relation,Member):
                    result.append(d.relation.entity2)      
            # se o relname for association
            elif d.relation.name == relname:
                #guardamos as associações
                prop.append(d.relation.assoc_properties())
                #guardamos as contagens das associações mais comuns
                prop_mc = Counter(prop).most_common(1)[0][0]
                #print(prop)
                #print(prop_mc)
                # se for single não temos herança
                if prop_mc[0] == "single":
                    for c in self.query_cancel(entity,relname):
                        if c.relation.assoc_properties() == prop_mc:
                            result.append((Counter(c.relation.entity2).most_common(1)[0][0]))
                # se não for single
                else:
                    for i in self.query_inherit(entity,relname):
                        if i.relation.assoc_properties() == prop_mc:
                            result.append(i.relation.entity2) 
        return list(set(result))


    #função auxiliar adaptada das aulas práticas com o professor DG - função que similar à função query(), 
    # mas em que existe cancelamento de herança
    def query_cancel(self, entity, assoc_name):
        local = [self.query_cancel(d.relation.entity2,assoc_name ) \
        for d in self.declarations if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype)) and d.relation.entity1 == entity]

        local_decl = self.query_local(e1=entity, relname=assoc_name)

        local_rels = [d.relation.name for d in local_decl]

        return [item for sublist in local for item in sublist if item.relation.name not in local_rels] + local_decl


class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        # Pode usar o argumento 'xpto' para passar mais
        # informação, caso precise
        #
        # IMPLEMENTAR AQUI
        # guardar o resultado
        result = []
        # lista auxiliar
        aux = []
        #lista que contem os valores de cada chave
        key_val = []
        
        dic= {}

        if domains == None:
            domains = self.domains
        else:
            result = xpto
        # para cada chave
        for key_val in domains.values():
            # se alguma estiver vazia retorna none
            if any([key_val == []]):
                return None
            #se nenhuma chave tem pelo menos um valor atribuido
            elif all( [len(key_val)==1]):
                for (valor,key_val) in domains.items():
                    dic = {valor: key_val[0]}
                    if dic not in result:
                        result.append(dic)
                        return result
                    return None
        # para cada chave
        for keys in domains.keys():
            # se o comprimento do dominio de key > 1
            if len(domains[keys])>1: 
                #iteramos sobre o dominio das chaves
                domains_keys = domains[keys][1:]
                #para não haver repetições 
                aux_set = set(aux)
                #para cada varivavel do dominio no dominio das chaves
                for var in domains_keys:
                    # se a variável não está em aux
                    if var not in aux_set:
                        #a cada dominio de key adiciona-se a var
                        domains[keys] = [var]
                # se var está em domaisn[keys]
                for var in domains[keys]:
                    #dicionario com novos dominios
                    dic = dict(domains)
        return result
        





