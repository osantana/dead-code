#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

class No(object):
	def __init__(self, questao=None, sim=None, nao=None):
		self._sim = sim
		self._nao = nao
		self._questao = questao
	
	def start(self):
		resposta = self.ask("Esse animal %s" % self._questao)
		if resposta[0].upper() == 'S':
			self._sim = self._sim.start()
		else:
			self._nao = self._nao.start()
		return self
	
	def ask(self, questao):
		resposta = ""
		while resposta == "":
			resposta = raw_input("%s? " % questao)
		return resposta

class Animal(No):
	def __init__(self, nome):
		super(Animal, self).__init__(nome)
		self._nome = nome

	def start(self):
		resposta = self.ask("É um(a) %s" % self._nome)
		if resposta[0].upper() != 'S':
			animal = self.ask("Qual é o animal")
			questao = self.ask("O que um %s faz que %s não faz" % (animal, self._nome))
			return No(questao, Animal(animal), self)

		print "Acertei!"
		return self

def main():
	raiz = No("vive na água", Animal("baleia"), Animal("macaco"))

	resposta = ""
	while resposta != "N":
		raiz.start()
		resposta = ""
		while resposta == "":
			resposta = raw_input("Deseja jogar novamente? ").upper()
		print
		
if __name__ == '__main__':
	main()
