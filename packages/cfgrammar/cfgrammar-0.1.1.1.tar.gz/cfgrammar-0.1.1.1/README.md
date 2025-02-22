# cfgrammar : Context-free grammars, parsing and semantic #

## Table of Contents

- [Main Features](#main-features)
- [Example](#example)
- [API overall graph](#API-overall-graph)

## Main features

* Grammar properties
  * accessible and productive rules / variables
  * ε-productive rules / variables
  * reduced grammar
  * "First" and "Follow" sets
* LL1 parsing
  * computes and displays LL(1) table
  * constructs parser
* LR parsing
  * computes and displays LR(0) automaton
  * constructs LR(0), SLR(1), LALR(1) tables and parsers
* Semantic
  * parsing with semantic actions
* Abstract Syntax Tree
  * predefined semantic classes to produce AST
    * Graphviz / dot output 
    * Latex + Tikz output
  
## Example
Code :
```python
from cfgrammar import Grammar

g = Grammar.from_string('S -> ( S ) S | a')

print(g)
print('productives variables : ', g.productive.vars)
print('Follow sets : ', g.follow)
print(g.tableLL1().to_markdown())
```
Output:
```
Grammar(
     terminals : ( ) a
     variables : S
     axiom : S
     rules : ['S → ( S ) S', 'S → a']
    )
productives variables :  {'S'}
Follow sets :  {'S': {')', '#'}}
|    | S           |
|:---|:------------|
| (  | S → ( S ) S |
| )  |             |
| a  | S → a       |
| #  |             |
```
## API overall graph

![schema](https://gitlab.univ-lille.fr/bruno.bogaert/cfgrammar/-/blob/e7ce707148b95087c8ab35ed446bbd13cbe6d8de/images/doc.svg)





