from converter import convert_num
from error import SYNTAXERROR


def exp(obj: str):
    return f"\"{obj}\" was expected."

def expect_not(obj: str, token: tuple):
    return obj != token[0]

def expect(obj: str, token: tuple):
    return obj == token[0]

def parser_engine(tokens: list, file_name):

    pos = 0

    def peek():
        return tokens[pos]

    def advance():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_atom():
        token = advance()
        if token[0] == "NUMBER":
            return ("num", convert_num(token[1]), token[2])
        elif token[0] == "IDENT":
            return ("ident", token[1], token[2])
        elif token[0] == "STRING":
            return ("str", token[1][1:-1], token[2])
        elif token[0] == "LPAREN":
            val = parse_expr()
            if expect_not("RPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(")"))
            advance()
            return val
        else:
            SYNTAXERROR.error(token[2], file_name, token)

    def parse_ident_list():
        names = []
        if peek()[0] == "IDENT":
            names.append(advance()[1])
            while peek()[0] == "COMMA":
                advance()
                if expect_not("IDENT", peek()):
                    SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
                names.append(advance()[1])
        return names
    
    def parse_value_list():
        values = []
        if peek()[0] in ("IDENT", "NUMBER", "STRING"):
            values.append(parse_atom())
            while peek()[0] == "COMMA":
                advance()
                if peek()[0] not in ("IDENT", "NUMBER", "STRING"):
                    SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Value"))
                values.append(parse_atom())
        return values

    def parse_term():
        left = parse_atom()
        while peek()[0] in ("STAR", "SLASH"):
            op = advance()
            right = parse_atom()
            left = ("binop", op[1], left, right, op[2])
        return left

    def parse_expr():
        left = parse_term()
        while peek()[0] in ("PLUS", "MINUS"):
            op = advance()
            right = parse_term()
            left = ("binop", op[1], left, right, op[2])
        return left

    def parse_comparison():
        left = parse_expr()
        if peek()[0] in ("EQEQ", "NEQ", "GT", "LT"):
            op = peek()
            advance()
            right = parse_expr()
            left = ("binop", op[1], left, right, op[2])
        return left

    def expect_semicolon():
        if expect_not("SEMICOLON", peek()):
            SYNTAXERROR.error(peek()[2], file_name, peek(), exp(";"))
        advance()

    def parse_statement():
        if expect("IF", peek()):
            line = peek()[2]
            advance()
            condition = parse_comparison()
            if expect_not("LBRACE", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("{"))
            advance()
            body = []
            while peek()[0] != "RBRACE":
                body.append(parse_statement())
            advance()
            return ("if", condition, body, line)

        elif expect("WHILE", peek()):
            line = peek()[2]
            advance()
            condition = parse_comparison()
            if expect_not("LBRACE", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("{"))
            advance()
            body = []
            while peek()[0] != "RBRACE":
                body.append(parse_statement())
            advance()
            return ("while", condition, body, line)

        elif expect("CALL", peek()):
            line = peek()[2]
            advance()
            if expect_not("IDENT", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
            name = peek()[1]
            advance()
            lib_name = None
            if peek()[0] == "DOT":
                advance()
                if expect_not("IDENT", peek()):
                    SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
                lib_name = name
                name = peek()[1]
                advance()
            if expect_not("LPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("("))
            advance()
            args = parse_value_list()
            if expect_not("RPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(")"))
            advance()
            if expect_not("COLON", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(":"))
            advance()
            if expect_not("LPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("("))
            advance()
            results = parse_ident_list()
            if expect_not("RPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(")"))
            advance()
            expect_semicolon()
            return ("call", name, lib_name, args, results, line)

        elif expect("FN", peek()):
            line = peek()[2]
            advance()
            if expect_not("IDENT", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
            name = peek()[1]
            advance()
            if expect_not("LPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("("))
            advance()
            params = parse_ident_list()
            if expect_not("RPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(")"))
            advance()
            if expect_not("COLON", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(":"))
            advance()
            if expect_not("LPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("("))
            advance()
            returns = parse_ident_list()
            if expect_not("RPAREN", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(")"))
            advance()
            if expect_not("LBRACE", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("{"))
            advance()
            body = []
            while peek()[0] != "RBRACE":
                body.append(parse_statement())
            advance()
            return ("fn", name, params, returns, body, line)

        elif expect("PRINT", peek()):
            line = peek()[2]
            advance()
            if expect_not("IDENT", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
            ident = peek()[1]
            advance()
            expect_semicolon()
            return ("print", ident, line)
        
        elif expect("REPEAT", peek()):
            advance()
            if expect_not("NUMBER", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("NUMBER"))
            num = peek()[1]
            advance()
            body = []
            if expect_not("LBRACE", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("{"))
            advance()  
            while peek()[0] != "RBRACE":
                body.append(parse_statement())
            advance()
            return ("repeat", int(num), body)
        
        elif expect("SLEEP", peek()):
            advance()
            if expect_not("NUMBER", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("NUMBER"))
            num = peek()[1]
            advance()
            expect_semicolon()
            return ("sleep", int(num))
        
        elif expect("USE", peek()):
            advance()
            if expect_not("IDENT", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
            name = peek()[1]
            advance()
            expect_semicolon()
            return ("use", name)
        
        elif expect("DEL", peek()):
            advance()
            if expect_not("IDENT", peek()):
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp("Ident"))
            value = peek()[1]
            advance()
            expect_semicolon()
            return ("del", value, peek()[2])
                
        elif expect("IDENT", peek()):
            ident = peek()
            name = advance()
            if peek()[0] == "EQ":
                advance()
                value = parse_comparison()
                if not expect_not("SEMICOLON", peek()):
                    advance()
                    return ("assign", name[1], value, name[2])
                SYNTAXERROR.error(peek()[2], file_name, peek(), exp(";"))
            else:
                SYNTAXERROR.error(ident[2], file_name, ident, exp("="))
        else:
            SYNTAXERROR.error(peek()[2], file_name, peek())

    def parse_program():
        statements = []
        while peek()[0] != "EOF":
            statements.append(parse_statement())

        return statements

    return parse_program()