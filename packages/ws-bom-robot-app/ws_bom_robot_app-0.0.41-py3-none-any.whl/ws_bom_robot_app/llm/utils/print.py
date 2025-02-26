import os, sys, json

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

def printJson(data) -> str:
    return f"{json.dumps(data, indent=2, sort_keys=True)},"

def printSingleJson(data) -> str:
    return f"{json.dumps(data, indent=2, sort_keys=True)}"

def printString(data: str) -> str:
    if data != "":
        return printJson(data)

def printSingleString(data: str) -> str:
    if data != "":
        return printSingleJson(data)
