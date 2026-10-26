from datetime import UTC

class Error:
    def __init__(self, ErrorName:str, ErrorText:str, ):
        self.ErrorName = ErrorName
        self.ErrorText = ErrorText
    
    def error(self, ErrorLine:int, ErrorFile:str, ErrorElement:str | None = None, OptionalErrorText:str | None = None):
        
        # Hata oluşmayacak scriptlerde modüllerin yüklenip overhead vermemesi için içe aktarmalar .error() metoduna eklendi.
        
        from datetime import datetime
        from sys import exit as sysexit

        from colorama import Fore


        reset = Fore.RESET
        red = Fore.RED
        green = Fore.GREEN
        blue = Fore.BLUE
        magenta = Fore.MAGENTA
        space = " " * 5
        
        date = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        print(f"\n [⦁] {magenta}Error{reset} at file: {magenta}{ErrorFile}{reset}:{magenta}{ErrorLine}{reset}")
        print(f"{space}|> Error Time: {date}")
        print(f"{space}|> {red}{self.ErrorName}{reset}: {self.ErrorText}")
        if OptionalErrorText:
            print(f"{space}|> Error Msg: {red}{OptionalErrorText}{reset}")
        if ErrorElement:
            print(f"{space}|> Element: {ErrorElement}")

        sysexit(1)

SYNTAXERROR             = Error(ErrorName="SyntaxError", ErrorText="Unknown syntax.")
MEMORYERROR             = Error(ErrorName="MemoryError", ErrorText="Insufficient memory.")
UNDEFINEDVALUEERROR     = Error("UndefinedValueError", "Variable not defined.")
UNDEFINEDFUNCTIONERROR  = Error("UndefinedFunctionError", "Function not defined.")
ZERODIVISIONERROR       = Error("ZeroDivisionError", "Division by zero.")
RECURSIONERROR          = Error("RecursionError", "The recursive function call limit has been reached.")