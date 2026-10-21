import argparse
import time
from sys import exit as sysexit

from executor import execute, functions, variables
from export_lib import library_functions
from lexer import lexer_engine
from parser import parser_engine

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, default=None, )
parser.add_argument("-d", "--debug",action="store_true", help="Enable debug mode.")
parser.add_argument("-t", "--timer", action="store_true", help="The program outputs the duration for which it ran.")

args = parser.parse_args()

if args.file is None:
    raise FileNotFoundError("You must use the --file argument.")

with open(args.file, "r") as f:
    code = f.read()

FILE_NAME = args.file

if args.timer:
    start = time.perf_counter_ns()

tokens = lexer_engine(code, FILE_NAME)

if args.debug:
    print(f"Tokens: {tokens}\n")

ast = parser_engine(tokens, FILE_NAME)

if args.debug:
        print(f"AST: {ast}\n")

for line in ast:
    execute(line, FILE_NAME, debug=args.debug)

if args.timer:
    end = time.perf_counter_ns()

if args.debug:
    print(f"Variables: {variables}")
    print(f"Functions: {functions}\n")
    print(f"Library Functions: {library_functions}")


if args.timer:
    print(f"Time: {(end-start)/1_000_000} ms.")

sysexit(0)