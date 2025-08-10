BREAKCHARS = ":,"
SPECIALSTOP = "{[("

def getToken(file)->str:
    ret = ""
    curr = ''
    while True:
        curr = file.read(1)
        if(curr=='\\'):
            #deal with comment
            pass
        if(curr=='"'):
            #deal with string
            pass
        if(curr in SPECIALSTOP):
            #end funct and signal to builder to build something different
            pass
        if(curr in BREAKCHARS):
            #end funct and signal to builder to handle token
            pass

    return ret

"""
Needs to take in a file and a dict
Will interpret the dictionary as if it were a JSON
ignore comments
upon encountering another dictionary structue i.e. stats, learnsets, it will need to recursively call itself.
return a copy?

"""
def builddict(file: '_io.TextIOWrapper', target: dict) -> dict:
    pass
    
#Handle lists as a special case for simplicity
def buildlist(file: "_io.TextIOWrapper", target: list) -> list:
    pass