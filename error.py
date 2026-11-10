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
        
        print(f"\n [⦁] {magenta}Hata{reset} dosyasında: {magenta}{ErrorFile}{reset}:{magenta}{ErrorLine}{reset}")
        print(f"{space}|> Hata anı: {date}")
        print(f"{space}|> {red}{self.ErrorName}{reset}: {self.ErrorText}")
        if OptionalErrorText:
            print(f"{space}|> Hata Mesajı: {red}{OptionalErrorText}{reset}")
        if ErrorElement:
            print(f"{space}|> Element: {ErrorElement}")

        sysexit(1)

SYNTAXERROR             = Error(ErrorName="SözdizimiHatası", ErrorText="Bilinmeyen sözdizimi.")
MEMORYERROR             = Error(ErrorName="BellekHatası", ErrorText="Yetersiz bellek.")
UNDEFINEDVALUEERROR     = Error("TanımsızDeğişkenHatası", "Değişken tanımsız.")
UNDEFINEDFUNCTIONERROR  = Error("TanımsızFonksiyonHatası", "Fonksiyon tanımsız.")
ZERODIVISIONERROR       = Error("SıfıraBölünmeHatası", "Sıfır ile bölünemez.")
RECURSIONERROR          = Error("İçFonksiyonHatası", "İç fonksiyon çağırma sınırına ulaşıldı.")
TYPEERROR               = Error("TipHatası", "Tanımlanmamış işlemler farklı tip işlemlerle kullanılamaz.")