import ast
import owlready2 as owl
import types
import os


#for parsing java
from javalang import tree, parse

#java source code path
java_src = "data/android-chess/app/src/main/java/jwtc/chess/"

#new owl filename
new_owl_file = "./tree2.owl"

#load the ontology 


#takes in a parsed java object
#goes thru all the class, field, method and constructor declarations, 
#adds it to the ontology

def fill_ontology(onto, parsed):
	for i, node in parsed:
		#first we need to see if the node is a class declaration
		if type(node) is tree.ClassDeclaration:
			cd = onto["ClassDeclaration"]() #create a class declaration instance
			cd.jname = [node.name]

			#check for methods 
			for member in node.body:

				#field declarations
				if type(member) is tree.FieldDeclaration:
					#add all the field names on the class decl ontology
					for field in member.declarators:
						fd = onto["FieldDeclaration"]()
						fd.jname = [field.name]
						cd.body.append(fd)

				#method declarations
				if type(member) is tree.MethodDeclaration:
					#append the methodname in ontology
					md = onto["MethodDeclaration"]()
					md.jname = [member.name]

					#add parameters
					for _, param in member.parameters:
						parameter = onto[param[0][0].__class__.__name__]()
						md.parameters.append(parameter)

					#add statements
					for _, stm in member.filter(tree.Statement):
						statement = onto[stm.__class__.__name__]()
						md.body.append(statement)
					cd.body.append(md)

				#Constructor declarations	
				elif type(member) is tree.ConstructorDeclaration:
					#append the Constructor name in ontology
					const_d = onto["ConstructorDeclaration"]()
					const_d.jname = [member.name]

					#add parameters
					for _, param in member.parameters:
						parameter = onto[param[0][0].__class__.__name__]()
						const_d.parameters.append(parameter)

					#add statements
					for _, stm in member.filter(tree.Statement):
						statement = onto[stm.__class__.__name__]()
						const_d.body.append(statement)
					cd.body.append(const_d)


def main():
	#go thru all the directory in the directory
	onto = owl.get_ontology("./tree.owl").load()
	for dirpath, dirname, filenames, in os.walk(java_src):
		for file in filenames:

			#if it's a java file parse it and call fill_ontology
			if(file.split('.')[-1] == "java"):
				file_src = open(os.path.join(dirpath, file), 'r').read()
				parsed   = parse.parse(file_src)
				fill_ontology(onto, parsed)
	onto.save(new_owl_file, format='rdfxml')




if __name__ == '__main__':
	main()







import pytest
class TestIndvid:
	onto = owl.get_ontology("./tree.owl").load()

	#parse a java code to fill the ontology
	src  = parse.parse("class A{int x,y; A(){x = 1; y = 2;} int hello(int a, int b){while(a <10){a++;} return a + b;}}")

	fill_ontology(onto, src)

	#We will test the first class
	A = onto['ClassDeclaration'].instances()[0]

	def test_field_decl(self):
		assert self.A.body[0].is_a[0].name == "FieldDeclaration"
		assert self.A.body[1].is_a[0].name == "FieldDeclaration"

	def test_field_decl_name(self):
		assert self.A.body[0].jname[0] == "x"
		assert self.A.body[1].jname[0] == "y"

	def test_method_decl(self):
		assert self.A.body[3].is_a[0].name == "MethodDeclaration"
		assert self.A.body[3].jname[0] == "hello"

	def test_constructor_decl(self):
		assert self.A.body[2].is_a[0].name == "ConstructorDeclaration"
		assert self.A.body[2].jname[0] == "A"

	def test_parameters(self):
		assert self.A.body[3].parameters[0].name == "formalparameter1"

		assert self.A.body[3].parameters[1].name == "formalparameter2"

	def test_statements(self):
		assert self.A.body[3].is_a[0].name == "MethodDeclaration"

		assert self.A.body[3].body[0].is_a[0].name == "WhileStatement"

		assert self.A.body[3].body[1].is_a[0].name == "BlockStatement"
