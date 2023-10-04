from sys import argv
import rdflib.plugins.sparql as sq
from owlready2 import *

world = World()
world.get_ontology("./tree2.owl").load()
graph = world.as_rdflib_graph()

class OwlList:
	def __init__(self):
		self.arr = []
		self.has_method = True
	def append(self, row, has_method = True):
		self.has_method = has_method
		owl = OwlClass(row, has_method)
		if owl not in self.arr:
			self.arr.append(owl)
	def __len__(self):
		return len(self.arr)

	def __repr__(self):
		ret = ""
		if(len(self.arr) > 0):
			ret += "\n---------------------------------------------------------\n"

			if self.has_method:
				ret += "".join(["Class Name".ljust(20), "Method Name".ljust(20), "Counter"])
				ret += "\n"
			else:
				ret += "".join(["Class Name".ljust(20), "Counter"])
				ret += "\n"

			for item in self.arr:
				ret += repr(item)
		else:
			ret = "Empty"
		return ret



class OwlClass:
	def __init__(self, row, has_method = True):
		self.name   = str(row.class_name)
		self.col_width = 20
		if has_method:
			self.method = str(row.method_name)
		else:
			self.method = ""
		self.count  = int(row.counter)

	def __eq__(self, other):
		return (self.method == other.method) and (self.count == other.count) and (self.name == other.name)

	def __repr__(self):
		if len(self.method) != 0:
			return f"{self.name.ljust(self.col_width)} {self.method.ljust(self.col_width)} {self.count}\n"
		else:
			return f"{self.name.ljust(self.col_width)}  {self.count}\n"



#classes with 10 or more methods
def large_class(graph):
	query = f""" SELECT ?class_name (COUNT(*) AS ?counter)
		WHERE {{
		?c a tree:ClassDeclaration .
		?c tree:jname ?class_name .
		?c tree:body ?m .
		?m a tree:MethodDeclaration .
		}} GROUP BY ?c """
	ret = OwlList()
	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >= 10):
			ret.append(row, False)
	return ret


#methods with 20 or more statements
def long_methods(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter)
				WHERE {{
				?c a tree:ClassDeclaration .
				?c tree:jname ?class_name .
				?c tree:body ?m .
				?m a tree:MethodDeclaration .
				?m tree:jname ?method_name .
				?m tree:body ?statements .
				}} GROUP BY ?m """
	long_methods = OwlList()
	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >= 20):
			long_methods.append(row)
	return long_methods

def long_constructors(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter)
				WHERE {{
				?c a tree:ClassDeclaration .
				?c tree:jname ?class_name .
				?c tree:body ?m .
				?m a tree:ConstructorDeclaration .
				?m tree:jname ?method_name .
				?m tree:body ?statements .
				}} GROUP BY ?m """
	ret = OwlList()
	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >= 20):
			ret.append(row)
	return ret

#methods with 5 or more parameters
def long_parameter_method(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter)
				WHERE {{
				?c a tree:ClassDeclaration .
				?c tree:jname ?class_name .
				?c tree:body ?m .
				?m a tree:MethodDeclaration .
				?m tree:jname ?method_name .
				?m tree:parameters ?param.
				}} GROUP BY ?m """
	ret = OwlList()
	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >= 5):
			ret.append(row)
	return ret

def long_parameter_constructor(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter)
				WHERE {{
				?c a tree:ClassDeclaration .
				?c tree:jname ?class_name .
				?c tree:body ?m .
				?m a tree:ConstructorDeclaration .
				?m tree:jname ?method_name .
				?m tree:parameters ?param.
				}} GROUP BY ?m """
	ret = OwlList()
	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >= 5):
			ret.append(row)
	return ret

# classes with only setters and getters
def data_class(graph):
	classes_query = f""" SELECT ?class_name (COUNT(*) AS ?counter) 
		WHERE {{
		?c a tree:ClassDeclaration .
		?c tree:jname ?class_name .
		?c tree:body ?m .
		?m a tree:MethodDeclaration .
		}} GROUP BY ?c"""

	get_set_query = f""" SELECT ?class_name ?method_name (COUNT(*) as ?counter) 
		WHERE {{ ?c a tree:ClassDeclaration .
		?c tree:jname ?class_name .
		?c tree:body ?m .
		?m a tree:MethodDeclaration .
		?m tree:jname ?method_name .
		FILTER regex(?method_name , "^(get|set)", "i") .
		}} GROUP BY ?c"""

	classes = []
	for row in graph.query(sq.prepareQuery(classes_query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) > 0):
			classes.append(row)

	getters_and_setters = []
	for row in graph.query(sq.prepareQuery(get_set_query, initNs={"tree":"http://example.org/tree.owl#"})):
		if(int(row.counter) >0):
			getters_and_setters.append(row)

	ret = OwlList()
	for method in getters_and_setters:
		for large in classes:
			if(large.class_name == method.class_name) and int(large.counter) == int(method.counter):
				ret.append(large, False)

	return ret
#methods with switch 
def methods_with_switch(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter) 
		WHERE {{
		?c a tree:ClassDeclaration . 
		?c tree:jname ?class_name . 
		?c tree:body ?m .
		?m a tree:MethodDeclaration .
		?m tree:jname ?method_name .
		?m tree:body ?s . 
		?s a tree:SwitchStatement
		}} GROUP BY ?m"""

	ret = OwlList()

	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if (int(row.counter) >= 1):
			ret.append(row)
	return ret

#Constructors with switch 
def constructors_with_switch(graph):
	query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter) 
		WHERE {{
		?c a tree:ClassDeclaration . 
		?c tree:jname ?class_name . 
		?c tree:body ?m .
		?m a tree:ConstructorDeclaration .
		?m tree:jname ?method_name .
		?m tree:body ?s . 
		?s a tree:SwitchStatement
		}} GROUP BY ?m"""

	ret = OwlList()

	for row in graph.query(sq.prepareQuery(query, initNs={"tree":"http://example.org/tree.owl#"})):
		if (int(row.counter) >= 1):
			ret.append(row)
	return ret



def main():
	print("long methods: ", long_methods(graph))
	print("long constructors: ", long_constructors(graph))
	print("long parameter lists in methods: ", long_parameter_method(graph))
	print("long parameter lists in constructors : ", long_parameter_constructor(graph))
	print("large class : ", large_class(graph))
	print("data  class : ", data_class(graph))
	print("Methods with switch : ", methods_with_switch(graph))
	print("Constructors with switch : ", constructors_with_switch(graph))

if __name__ == "__main__":
	main()



import pytest
from javalang import parse
from individ_creator import fill_ontology

class TestBadSmells:

	tree_owl = "./tree.owl"

	def get_onto(self, code):
		java_parsed = parse.parse(code)
		onto = get_ontology(self.tree_owl).load()
		fill_ontology(onto, java_parsed)
		return onto

	def create_graph(self, ontology):
		ontology.save(file="./test3.owl", format="rdfxml")
		world = World()
		world.get_ontology("./test3.owl").load()
		graph = world.as_rdflib_graph()
		return graph
	
	def delete_ontology(self, onto):
		for e in onto["ClassDeclaration"].instances():
			destroy_entity(e)


	def test_long_methods(self):
		code = "class A { int f(int x) {  x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;" \
			   "x++;x++;x++; return x; } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(long_methods(graph)) == 1
		self.delete_ontology(onto)


	def test_long_constructor(self):
		code = "class A { A() {  x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;" \
			   "x++;x++;x++; } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(long_constructors(graph)) == 1
		self.delete_ontology(onto)

	def test_long_parameter_method(self):
		code = "class A { void foo(int x, int y, int z, int a, int b, int c, int d) {  x++;x++;x++; } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(long_parameter_method(graph)) == 1
		self.delete_ontology(onto)

	def test_long_parameter_constructor(self):
		code = "class A { A(int x, int y, int z, int a, int b, int c, int d) {  x++;x++;x++; } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(long_parameter_constructor(graph)) == 1
		self.delete_ontology(onto)

	def test_data_class(self):
		code = "class A { void set_data(int a){} int get_data(){return 100;} }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len((data_class(graph))) == 1
		self.delete_ontology(onto)

	def test_data_class_invalid(self):
		code = "class A { void apple(){} void set_data(int a){} int get_data(){return 100;} }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len((data_class(graph))) == 0
		self.delete_ontology(onto)

	def test_method_with_switch(self):
		code = "class Test { int func(){ int a = 0; switch(a){ case 1: return 2 ; break; " \
			   "case 2: return 4; break; default: return 8; } } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(methods_with_switch(graph)) == 1
		self.delete_ontology(onto)

	def test_constructor_with_switch(self):
		code = "class Test {  A(){ int a = 0; switch(a){ case 1: return 2 ; break; " \
			   "case 2: return 4; break; default: return 8; } } }"
		onto = self.get_onto(code)
		graph = self.create_graph(onto)
		assert len(constructors_with_switch(graph)) == 1
		self.delete_ontology(onto)
