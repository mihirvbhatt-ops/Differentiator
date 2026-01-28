Takes a mathematical function as a string input 
lexer+shuntingyard:
      uses a lexer,tokenizer and the shuntingyard algorithm to convert the function into its reverse postfix notation
rpn-to-tree:
      checks the function/operator to decide how many child nodes it needs 
      stores those into an AST
differentiator:
      recursively traverses the tree and differentiates each child node and then checks the parent node to decide what differentiation rule to use (product rule, quotient rule, trig rules etc)
      stores the result of these trees into a new result tree
simplification:
      traverses the tree and prunes useless nodes (something^1, something*1, something+0,etc)
      calculates commutative functions (+,*) and adds the final result into the tree
result:
      converts the final tree into a string 
      runs one final parse to simpify math (cases where the simplification process doesn't work due to nesting etc) and combines like terms (x+x=2x etc)
