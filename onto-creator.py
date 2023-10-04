import ast
import owlready2 as owl
import types

#creating ontology to store the java ontology
onto  = owl.get_ontology("http://example.org/tree.owl")

#ontology file 
onto_file = "./tree.owl"

#python file containing all the information about the java syntax
tree_file = "./tree.py"


"""
Steps
create a new class OntoVisitor derived from ast.NodeVisitor 
override the generic_visitor method that takes in node

if node is a Class defination
	if the class is derived from "Node"
		create new_class derived from  "Thing" on ontology
	else 
		create new_class derived from all bases

	for everything in the class:
		if it's body or parameter create ObjectProperty else create DataProperty
"""

class OntoVisitor(ast.NodeVisitor):
	def generic_visit(self, node):
		#put the ontology in the namespace
		super().generic_visit(node)
		with onto:

			if type(node) == ast.ClassDef:
				if(node.bases[0].id) == "Node":
					types.new_class(node.name, (owl.Thing,))
				else:
					#all the bases the class is derived from
					bases = [onto[base.id] for base in node.bases]
					types.new_class(node.name, tuple(bases))


				#go over all the properties in the class
				for property in node.body[0].value.elts:
					if property.s not in ["body", "parameters"]:
						if property.s == "name":
							types.new_class("jname", (owl.DataProperty,))
						else:
							types.new_class(property.s, (owl.DataProperty,))

				types.new_class("body", (owl.ObjectProperty,))
				types.new_class("parameters", (owl.ObjectProperty,))


def main():
	tree        = open(tree_file, "r").read()
	parsed_tree = ast.parse(tree)

	#visit all the node to fill the ontology
	OntoVisitor().generic_visit(parsed_tree)
	onto.save(onto_file, format='rdfxml')
if __name__ == '__main__':
	main()

import pytest
class TestClass:
	onto = owl.get_ontology("./tree.owl").load()

	def test_one(self):
		decl = self.onto["ClassDeclaration"]
		assert decl.name == "ClassDeclaration"

	def test_interface_decl(self):
		decl = self.onto["InterfaceDeclaration"]
		assert decl.name ==  "InterfaceDeclaration"
		assert decl.is_a[0].name ==  "TypeDeclaration"

	def test_annotation_decl(self):
		decl = self.onto["AnnotationDeclaration"]
		assert decl.name ==  "AnnotationDeclaration"
		assert decl.is_a[0].name == "TypeDeclaration"

	def test_constructor_decl(self):
		decl = self.onto["ConstructorDeclaration"]
		assert decl.name == "ConstructorDeclaration"
		assert decl.is_a[0].name == "Declaration"
		assert decl.is_a[1].name == "Documented"




