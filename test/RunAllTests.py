import os
from pathlib import Path

TestFiles = []

for file in Path(__file__).parent.glob('*.spl-test'):
    TestFiles.append(file)
    print(file)
    
Interpreter = (Path(__file__).parent.parent / "spl.py").resolve()

n = 1

for file in TestFiles:
    print("[+] Test:", n, "\n")    
    os.system(f"python {Interpreter} --file {file}")
    print("\n[+] Test", n, "Finished.")
    n = n+1
