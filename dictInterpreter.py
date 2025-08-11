BREAKCHARS = "]:,"
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

def eatLine(file) -> None:
    curr = file.readline()
    return

def determineType(s: str)->type:
    if(s.startswith('"')):
        return str
    elif(s=="true" or s=="false"):
        return bool
    elif(s.isnumeric()):
        return int
    elif(s.isalnum()):
        try:
            float(s)
            return float
        except ValueError:
            pass
    return str

"""
Needs to take in a file and a dict
Will interpret the dictionary as if it were a JSON
ignore comments
upon encountering another dictionary structue i.e. stats, learnsets, it will need to recursively call itself.
returns the input list

"""
def builddict(file, target: dict) -> dict:
    pass
    
#Handle lists as a special case for simplicity
def buildlist(file, target: list) -> list:
    token = " "
    while token[-1]!="]":
        token = getToken(file)
        if token[-1]=="/":
            # print(print("///"+token))
            while file.read(1)!='/':
                # print("skipped", f.tell())
                pass
            t = determineType(token[:-1])
            print("###"+token)
            # print("###"+str(type(t)))
            target.append(t(token[:-1].replace('"','').strip()))
        elif token == "]":
            break
        else:
            t = determineType(token[:-1])
            print("###"+token)
            # print("###"+str(type(t)))
            target.append(t(token[:-1].replace('"','').strip()))
    return target
        

if __name__ == "__main__":
    target = input()
    with open(target, "r+") as f:
        t = getToken(f).strip()
        if t.startswith("export"):
            eatLine(f)
            t = "{"
        while t!="":
            if t=="[":
                t = buildlist(f,[])
            print(t)
            t = getToken(f).strip()
    print("***************************DONE*****************************")