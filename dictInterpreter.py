BREAKCHARS = ":,"
SPECIALSTOP = "{[("

def getToken(file)->str:
    ret = ""
    curr = ''
    while True:
        curr = file.read(1)
        if(curr=='/'):
            curr = file.read(1)
            if curr == "/":
                while curr!='\n':
                    curr = file.read(1)
            if curr == "*":
                while curr!='/':
                    curr = file.read(1)
        elif(curr=='"'):
            #deal with string
            ret+=curr
            curr = file.read(1)
            while curr!='"':
                ret+=curr
                curr = file.read(1)
            ret+=curr
            curr = file.read(1) #Get breakcharacter (:,)
            ret+=curr
            break
        elif(curr in SPECIALSTOP):
            #end funct and signal to builder to build something different
            ret+=curr
            break
        elif(curr in BREAKCHARS):
            #end funct and signal to builder to handle token
            ret+=curr
            break
        else:
            ret+=curr
    return ret

def eatFunction(file)->None:
    curr = ''
    while curr!='}':
        curr = file.read(1)
    return

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

if __name__ == "__main__":
    target = input()
    with open(target, "r+") as f:
        t = getToken(f).strip()
        while t!="":
            print(t)
            t = getToken(f).strip()
    print("***************************DONE*****************************")