# Bad Smell Detection: Using Ontologies to Find Bad Smells in Code

## Overview

This project focuses on utilizing ontologies to identify and detect various types of bad smells in code. Bad smells are indicators of potential issues in software code, and this project aims to automate their detection using semantic web technologies and Sparql queries.

## Bad Smell Types

The project addresses the following types of bad smells:

- **Bloaters**
- **Object-Orientation Abusers**
- **Change Preventers**
- **Dispensables**
- **Couplers**

## Project Components

1. **Create Ontology**: 
   - Create an ontology for Java entities that serves as the foundation for detecting bad smells.

2. **Populate Ontology**:
   - Populate the ontology with instances, including classes and class members.

3. **Populate Ontology (Statements and Method Parameters)**:
   - Further populate the ontology with instances related to statements and method parameters.

4. **Find Bad Smells**:
   - Encode bad smells as Sparql queries to automatically detect them within the code.

## How to Run

## Ontology Creator
`python3 onto-creator.py tree.py`

## Run ontology test
`python3 -m pytest -s onto-creator.py`

## Invid Creator
`python3 individ_creator.py`

## Run individ test
`python3 -m pytest -s individ_creator.py`

## Bad smells 
`python3 bad_smells.py`

## Run bad smells test
`python3 -m pytest -s bad_smells.py`

## Save the result in .txt file
`python3 bad_smells.py > result.txt`