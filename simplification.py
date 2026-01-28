import differentiation as diff
#node=diff.nodemaker(function)
#ans=(diff.differentiate(node))
def prune(ans):
    #removes irrelevant nodes and operators such as *0,+0,*1,^1; adds and multiplies constants
    #param- tree with the derivative of the function
    #output- simplified tree
    def is_zero(x):
        return x == 0

    def is_one(x):
        return x == 1

    def flatten_sum(lst):
        res = []
        add=0
        for item in lst:
            if isinstance(item, dict) and list(item.keys())[0] == "+":
                res.extend(flatten_sum(item["+"]))
            else:
                res.append(item)
            for i in res:
                if isinstance(i,int):
                    add+=i
                    res.remove(i)
        res.insert(0,add)   
        return res

    def flatten_prod(lst):
        res = []
        pro=1
        for item in lst:
            if isinstance(item, dict) and list(item.keys())[0] == "*":
                res.extend(flatten_prod(item["*"]))
            else:
                res.append(item)
            for i in res:
                if isinstance(i,int):
                    pro*=i
                    res.remove(i)
        res.insert(0,pro)   
        return res

    if not isinstance(ans, dict):
        return ans  # leaf node

    op = list(ans.keys())[0]
    val = ans[op]

    # unary operators
    if not isinstance(val, list):
        val = [val]

    # recursively prune children
    children = [prune(c) if isinstance(c, dict) else c for c in val]

    # simplify by operator type
    if op == "+":
        items = flatten_sum(children)
        # remove zeros
        items = [i for i in items if not is_zero(i)]
        if not items:
            return 0
        if len(items) == 1:
            return items[0]
        return {"+": items}

    if op == "*":
        items = flatten_prod(children)
        # if any is zero
        if any(is_zero(i) for i in items):
            return 0
        # remove ones
        items = [i for i in items if not is_one(i)]
        if not items:
            return 1
        if len(items) == 1:
            return items[0]
        return {"*": items}

    if op == "-":
        # unary minus
        if len(children) == 1:
            child = children[0]
            if isinstance(child, int):
                return -child
            if isinstance(child, dict) and list(child.keys())[0] == "-":
                # double negative
                return child["-"][0]
            return {"-": [child]}
        # binary minus
        a, b = children
        if is_zero(b):
            return a
        if is_zero(a):
            return {"-": [b]}
        return {"-": [a, b]}

    if op == "/":
        a, b = children
        if is_zero(a):
            return 0
        if is_one(b):
            return a
        return {"/": [a, b]}

    if op == "^":
        a, b = children
        if is_zero(b):
            return 1
        if is_one(b):
            return a
        if is_zero(a):
            return 0
        if is_one(a):
            return 1
        return {"^": [a, b]}

    # for unary trig/log functions etc.
    if len(children) == 1:
        return {op: [children[0]]}

    # fallback for unexpected
    return {op: children}


