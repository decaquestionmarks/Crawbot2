BREAKCHARS = "]}:,"
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
    bracecount = 1
    while bracecount>0:
        curr = file.read(1)
        if(curr=="}"):
            bracecount-=1
        if(curr=="{"):
            bracecount+=1
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
    token = " "
    while len(token)>0 and not "}" in token:
        #Key
        token = getToken(file).strip()
        print(token)
        if token.startswith("export"):
            eatLine(file)
            continue
        if token[-1]=="(":
            eatLine(file)
            eatFunction(file)
            continue
        if "}" in token:
            print("Breaking Out")
            break
        key = token[:-1]
        #Value
        token = getToken(file).strip()
        # print(token)
        if token=="[":
            l = buildlist(file,[])
            token = file.read(1)
            target[key] = l
            # print(target)
            # print(key,token)
            # print(key,l)
            continue
        if token=="{":
            print(f"Entering dictionary for {key}")
            d = builddict(file,{})
            token = file.read(1)
            target[key] = d
            # print(target)
            # print(key,token)
            # print(key,d)
            continue
        if token[-1]=="/":
            # print(print("///"+token))
            while file.read(1)!='/':
                # print("skipped", f.tell())
                pass
        t = determineType(token[:-1])
        # print(token)
        # print("###"+str(type(t)))
        target[key] = (t(token[:-1].replace('"','').replace('}','').strip()))
        print(target)
        print(key,token)
        # input()
    if token.count("}")>1:
        print(token)
        print(file.tell(), token.count("}")-1)
        file.seek(-1*(token.count("}")-1),1)
    return target
    
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
        
def get(target: dict, keys: list[str]): ##can return any type
    if len(keys)==1:
        return target[keys[0]]
    else:
        return get(target[keys[0]],keys[1:])

if __name__ == "__main__":
    target = input()
    result = {}
    with open(target, "r+") as f:
        builddict(f,result)
    print("***************************DONE*****************************")
    print(result)
    while True:
        args = input().split(" ")
        print(args)
        print(get(result,args))