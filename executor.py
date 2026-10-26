import operator
import sys

from error import (
    RECURSIONERROR,
    SYNTAXERROR,
    UNDEFINEDFUNCTIONERROR,
    UNDEFINEDVALUEERROR,
    ZERODIVISIONERROR,
)
from export_lib import library_functions, load
from keyword_functions import *

variables = {}
functions = {}
scopes    = {}

OperatorChars = {
    "!=": operator.ne,
    "==": operator.eq,
    ">":  operator.gt,
    "<":  operator.lt,
    "-":  operator.sub,
    "+":  operator.add,
    "*":  operator.mul
}

def evaluate(node, file_name):
    kind = node[0]
    if kind == "num":
        return node[1]
    elif kind == "ident":
        name = node[1]
        line = node[2]
        if name not in variables:
            UNDEFINEDVALUEERROR.error(line, file_name, name)
        return variables[name]
    elif kind == 'binop':
        op = node[1]
        left = evaluate(node[2], file_name)
        right = evaluate(node[3], file_name)
        line = node[4]
        if op == '/':
            if right == 0:
                ZERODIVISIONERROR.error(line, file_name)
            return left / right
        
        return OperatorChars[op](left, right)
        
        
    elif kind == "str":
        return node[1]


def execute(node, file_name, debug):
    
    kind = node[0]
    
    if debug:
        print(f"\nExecuting {kind}")
    
    if kind == 'assign':
        name = node[1]
        value = evaluate(node[2], file_name)
        variables[name] = value

    elif kind == "fn":
        functions[node[1]] = (node[2], node[3], node[4])

    elif kind == "call":
        try:
            name = node[1]
            lib_name = node[2]
            args = node[3]
            results = node[4]
            line = node[5]

            if lib_name is not None:
                if lib_name not in library_functions:
                    UNDEFINEDFUNCTIONERROR.error(line, file_name, lib_name, "Library not loaded.")
                if name not in library_functions[lib_name]:
                    UNDEFINEDFUNCTIONERROR.error(line, file_name, name)
                func = library_functions[lib_name][name]
                evaluated_args = [evaluate(a, file_name) for a in args]
                result = func(*evaluated_args)
                if results:
                    variables[results[0]] = result

            else:
                if name not in functions:
                    UNDEFINEDFUNCTIONERROR.error(line, file_name, name)
                params, returns, body = functions[name]
                if len(args) != len(params):
                    SYNTAXERROR.error(line, file_name, name, "Argument count mismatch.")
                if len(results) != len(returns):
                    SYNTAXERROR.error(line, file_name, name, "Return count mismatch.")
                for pname, arg_node in zip(params, args):
                    variables[pname] = evaluate(arg_node, file_name)
                for stmt in body:
                    execute(stmt, file_name, debug)
                return_values = {}
                for rname in returns:
                    return_values[rname] = variables.get(rname, "")
                for pname in params:
                    variables.pop(pname, None)
                for rname, value in zip(results, return_values.values()):
                    variables[rname] = value

        except RecursionError:
            RECURSIONERROR.error(line, file_name, node, f"Recursion limit: {sys.getrecursionlimit()}")
            

    elif kind == 'if':
        condition = evaluate(node[1], file_name)
        if condition:
            for stmt in node[2]:
                execute(stmt, file_name, debug)

    elif kind == 'while':
        while evaluate(node[1], file_name):
            for stmt in node[2]:
                execute(stmt, file_name, debug)

    elif kind == "print":
        name = node[1]
        line = node[2]
        if name not in variables:
            UNDEFINEDVALUEERROR.error(line, file_name, name)
        keyword_print(variables[name])
    
    elif kind == "repeat":
        for _ in range(node[1]):
            for stmt in node[2]:
                execute(stmt, file_name, debug)
                
    elif kind == "sleep":
        keyword_sleep(node[1])
        
    elif kind == "use":
        load(node[1])
        
    elif kind == "del":
        if node[1] not in variables and node[1] not in functions:
            UNDEFINEDVALUEERROR.error(node[2], file_name, node, "Variable or Function not founded.")
        if node[1] in variables:
            variables.pop(node[1])
        else:
            functions.pop(node[1])
