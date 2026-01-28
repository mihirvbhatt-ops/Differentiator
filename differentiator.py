import rpn-to-tree as pft
def nodemaker(function):
    node = pft.treemaker(function)
    return node
def pwrrule(node):
    for i in node.values():
        if isinstance(i, list):
            items = i
        else:
            items = [i]
        for j in items:
            if isinstance(j,int):
                num = j
            else:
                var = j
    output = {"*": [num, {"^": [var, int(num) - 1]}]}
    return output

def prdctrule(node, du, dv, u, v):
    output = {"+": [{"*": [v, du]}, {"*": [dv, u]}]}
    return output

def sumrule(node, du, dv):
    output = {"+": [du, dv]}
    return output

def subrule(node, du):
    output= {"-": [du]}
    return output

def divrule(node, du, dv, u, v):
    output = {"/": [{"-": [{"*": [v, du]}, {"*": [dv, u]}]}, {"^": [v, 2]}]}
    return output

def cnstrule(u):
    output = 0
    return output
def varrule(u):
    output = 1
    return output

def trigrules(node, du):
    key = list(node.keys())[0]
    u = node[key]

    if key == "sin":
        return {"*": [{"cos": u}, du]}
    elif key == "cos":
        return {"*": [{"-": {"sin": u}}, du]}
    elif key == "tan":
        return {"*": [{"^": [ {"sec": u}, 2]}, du]}
    elif key == "sec":
        return {"*": [{"*": [{"tan": u}, {"sec": u}]}, du]}
    elif key == "csc":
        return {"*": [{"*": [{"-": {"csc": u}}, {"cot": u}]}, du]}
    elif key == "cot":
        return {"*": [{"*": [{"-": {"cot": u}}, {"csc": u}]}, du]}
    elif key == "ln":
        return {"/": [du, u]}
    elif key == "log":
        # assuming natural log base e
        return {"/": [du, u]}
    
def rule(node,u,du=None,v=None,dv=None):
    key=list(node.keys())[0]
    if key == "-":
        return subrule(node,du)     
    elif key=="/":
        return divrule(node, du, dv, u, v)
    elif key=="*":
        return prdctrule(node, du, dv, u, v)
    elif key=="^":
        return pwrrule(node)
    elif key=="+":
        return sumrule(node, du, dv)
    else:
        return trigrules(node,du)


def differentiate(node):
    #recursive function that takes nodes as inputs, processes them through the rules and outputs the derivative appropriately
    #param- ast containing the original function
    #output- tree containing the derivative of the function
        key = list(node.keys())[0]
        val = node[key]
        if isinstance(val,list):
            u=(val[0])
            v=(val[1])
            #print(val,u,v)
            if isinstance(u,dict):
                du=differentiate(u)
            elif isinstance(u,str):
                du=varrule(u)
            elif isinstance(u,int):
                du=cnstrule(u)
            if isinstance(v,dict):
                dv=differentiate(v)
            elif isinstance(v,str):
                dv=varrule(v)
            elif isinstance(v,int):
                dv=cnstrule(v)
            output=rule(node,u=u,du=du,v=v,dv=dv)
        else:
            u=val
            if isinstance(u,dict):
                du=differentiate(u)
            elif isinstance(u,str):
                du=varrule(u)
            elif isinstance(u,int):
                du=cnstrule(u)
            output=rule(node,u=u,du=du)
            
        return output
#function=input("enter")
#print(nodemaker(function))
#print(differentiate(nodemaker(function)))


