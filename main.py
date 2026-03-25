from sys import argv
from typing import TypeAlias, TypedDict
from sys import stderr, exit
from bisect import bisect_right
from re import findall as regex_findall
Line = TypedDict("Line", {"keyword": str, "args": list[str], "old_i": int, "new_i" : int })
File : TypeAlias = list[Line]

FILENAME = argv[1]   # gestions des erreurs arg dans le script bash associé
KEYWORDS = {
    "move"      :{"flags": ["movelike"]},
    "add"       :{"flags": ["operator"]},
    "sub"       :{"flags": ["operator"]},
    "mul"       :{"flags": ["operator"]},
    "div"       :{"flags": ["operator"]},
    "mod"       :{"flags": ["operator"]},
    "jump_eq"   :{"flags": ["jump"]},
    "jump_neq"  :{"flags": ["jump"]},
    "jump_g"    :{"flags": ["jump"]},
    "jump_ge"   :{"flags": ["jump"]},
    "jump_l"    :{"flags": ["jump"]},
    "jump_le"   :{"flags": ["jump"]},
    "jump"      :{"flags": ["jump"]},
    "malloc"    :{"flags": ["movelike"]},
    "ret"       :{"flags": ["no args"]},
    "call"      :{"flags": ["jump"]},
    "print"     :{"flags": ["print"]}, 
    "println"   :{"flags": ["print"]}, 
    "push"      :{"flags": ["push"]}, 
    "pop"       :{"flags": ["pop"]},        
    "label"     :{"flags": ["label"]},
    "halt"      :{"flags": ["no args"]},
    "end"       :{"flags": ["no args"]},
    "loop"      :{"flags": ["no args"]}
}
REGISTERS= {
    "R0",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7",
    "PC",
    "SP"
}
LABELS : dict[str,int] = {}
LOOP_STACK = []
END_LIST = []

def isPrintArg(string: str) -> bool:
    return isNumber(string) or (string.startswith("\"") and string.endswith("\"")) or ((string.startswith("(") and string.endswith(")")) and all([isPrintArg(a) for a in splitWithBlocks(string.strip("()")," +") ]))
def isNumber(string: str) -> bool:
    return isAddress(string) or string.isdecimal() or (string[0] == "-" and string[1:].isdecimal())
def isAddress(string: str) -> bool: 
    def isBracketAddress(string:str):
        if string.startswith("[") and string.endswith("]"):
            args = splitOnChars(string.strip("[]")," +-")
            for a in args:
                if not isNumber(a): return False
            return True
        return False
    return string in REGISTERS or isBracketAddress(string)
def isLineNumber(string: str) -> bool: 
    return isNumber(string) or isLabel(string) or string == "-break"
def isLabel(string:str) -> bool: 
    return string.startswith("$")

def newPrintArgs(args: list[str]) -> list[str]:
    return [f"({" + \" \" + ".join([arg.strip("()") for arg in args])})"]
def splitOnChars(string: str, chars: str) -> list[str]:
    lasti = 0
    res = []
    for i, c in enumerate(string):
        if c in chars:
            substr = string[lasti:i]
            if substr != '' : res.append(substr)
            lasti = i+1
    substr = string[lasti:len(string)]
    if substr != '' : res.append(substr)
    return res
def splitWithBlocks(string: str, chars: str) -> list[str]:
    pattern = fr'\[.*?\]|\(.*?\)|\".*?\"|[^{chars}\s]+'
    found = regex_findall(pattern, string)
    return [arg.strip() for arg in found]

def findNearestEnd(i : int):
    return END_LIST[bisect_right(END_LIST, i)]
def printerr(*args, **kwargs):
    print("Woops !\t",*args, file=stderr, **kwargs)
def checkSyntaxByFlags(line: Line): # return whether a line should be skipped or not
    def checkOperatorArgs() -> None:
        if not len(args) == 3: raise SyntaxError(f"line {i} in '{FILENAME}', '{line["keyword"]}' expects 3 arguments but {len(args)} were given")
        if not isAddress(args[0]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects an Adress Identifier for first parameter but {args[0]} was found instead")
        if not isNumber(args[1]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for second parameter but {args[1]} was found instead")
        if not isNumber(args[2]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for third parameter but {args[2]} was found instead")
    def checkPushArgs() -> None:
        if len(args) < 1: raise SyntaxError(f"line {i} in \"{FILENAME}\", '{line["keyword"]}' expects at least 1 arguments but None were given")
        if not isNumber(args[0]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for first parameter but {args[0]} was found instead")
        if not isNumber(args[1]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for second parameter but {args[1]} was found instead")
        if not isNumber(args[2]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for third parameter but {args[2]} was found instead")
    def checkJumpArgs() -> None:
        match keyword:
            case "call"|"jump":
                if not len(args) == 1: raise SyntaxError(f"line {i} in '{FILENAME}', '{line["keyword"]}' expects 1 arguments but {len(args)} were given")
                if not isLineNumber(args[0]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects an Label or Line Number for first parameter but {args[0]} was found instead")
            case _ :
                if not len(args) == 3: raise SyntaxError(f"line {i} in '{FILENAME}', '{line["keyword"]}' expects 3 arguments but {len(args)} were given")
                if not isNumber(args[0]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for first parameter but {args[0]} was found instead")   
                if not isNumber(args[1]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for second parameter but {args[1]} was found instead")
                if not isLineNumber(args[2]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects an Label or Line Number for third parameter but {args[2]} was found instead")
    def checkPrintArgs() -> None:
        for arg in args:
            if not isPrintArg(arg): raise SyntaxError(f"line {i} in '{FILENAME}', '{arg}' is not a valid print argument")
    def checkNoArgs() -> None:
        if len(line["args"]) != 0: raise SyntaxError(f"line {i} in '{FILENAME}', '{line['keyword']} expects no argument but {len(line['args'])} were given'")
    def checkMoveLikeArgs() -> None:
        if not len(args) == 2: raise SyntaxError(f"line {i} in '{FILENAME}', '{line["keyword"]}' expects 2 arguments but {len(args)} were given")
        if not isAddress(args[0]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects an Adress Identifier for first parameter but {args[0]} was found instead")
        if not isNumber(args[1]) : raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for second parameter but {args[1]} was found instead")
    def checkPopArgs() -> None:
        if len(args) == 1: 
            if not isNumber(args[0]): raise SyntaxError (f"line {i} in '{FILENAME}', '{line["keyword"]}' expects a Number Value for first parameter but {args[0]} was found instead")   
        if len(args) < 1: raise SyntaxError(f"line {i} in '{FILENAME}', '{line["keyword"]}' expects up to 1 argument but {len(args)} were given")
    def checkLabelArgs() -> None :
        if len(line["args"]) != 1 : raise SyntaxError(f"line {i} in '{FILENAME}', {line["keyword"]} expects 1 argument but {len(line['args'])} were given" )
        arg = args[0]
        if not isLabel(arg): raise SyntaxError(f"line {i} in '{FILENAME}', Invalid label name '{arg}'. Did you mean ${arg}?")

    keyword = line["keyword"]
    i = line["old_i"] + 1
    args = line['args']
    for flag in KEYWORDS[keyword]["flags"]:
        match flag:
            case "no args":     checkNoArgs()
            case "operator":    checkOperatorArgs()
            case "jump":        checkJumpArgs()
            case "movelike":    checkMoveLikeArgs()
            case "print":       checkPrintArgs()
            case "push":        checkPushArgs()
            case "pop" :        checkPopArgs()
            case "label":       checkLabelArgs()

def treatment():
    
    FILE : File = []
    # Syntax Verification, Label registering and structure building
    with open(FILENAME) as file:
        old_i = 0 # original file line numbers, used for error detection on written script
        new_i = 0 # result file line numbers (after adding lines), used to order compiled script
        for strline in file:
            counted = True
            ### basic line contruction
            strline = strline.strip()

            if (i := strline.find("//")) >= 0: strline = strline[:i] # strip commentaries

            line_block = splitWithBlocks(strline," ,") # split expression

            if len(line_block) == 0: # skip newlines
                old_i += 1
                continue
            
            ###  syntax detection

            keyword = line_block[0] 
            if keyword not in KEYWORDS : raise SyntaxError(f"line {old_i+1} in '{FILENAME}', Unknown token {keyword} : delete this token")
            
            # line construction
            
            line : Line = {"keyword": keyword, "args": line_block[1:], "old_i" : old_i, "new_i": new_i}
            checkSyntaxByFlags(line) # syntax checking of args

            ### special keyword management: loop/end/label (they are removed) and push (adds lines)

            match keyword:
                case "loop": 
                    LOOP_STACK.append(new_i)
                    counted = False
                case "end" : 
                    if len(LOOP_STACK) <= 0: 
                        raise SyntaxError(f"line {old_i + 1} in '{FILENAME}', Unexpected 'end' token, delete this token ")
                    line : Line = {"keyword": "jump", "args" : [str(LOOP_STACK.pop())], "old_i": old_i, "new_i": new_i}
                    counted = False
                    END_LIST.append(new_i)
                case "label": 
                    LABELS[line["args"][0]] = new_i
                    counted = False
                case "push" : 
                    for arg in line["args"]: # adding lines
                        FILE.append({"keyword": "push", "args": [arg], "old_i": old_i, "new_i": new_i})
                        new_i += 1
                        
            # adding line to total
            
            if counted:
                FILE.append(line)
                new_i += 1
            old_i += 1
        FILE.append({"keyword": "halt", "args": [], "new_i": new_i, "old_i": -1})

    ### replacing -break and labels and formatting prints
    if len(LOOP_STACK) != 0:
        raise SyntaxError(f"file {FILENAME}, Unmatched loop statement")
    for line in FILE:
        for pos,arg in enumerate(line["args"]):
            if isLabel(arg):
                if arg in LABELS:
                    line["args"][pos] = str(LABELS[arg])
                else : raise SyntaxError(f"line {line['old_i']+1} in '{FILENAME}', Undefined label name '{arg}'")
            elif arg == "-break":
                if line["new_i"] > END_LIST[-1]: raise SyntaxError(f"line {line['old_i']+1} in '{FILENAME}', cannot break: reached end of file")
                #print("line : ", line["new_i"], " | ENDS : ", END_LIST)
                line["args"][pos] = str(findNearestEnd(line["new_i"]))
        if line["keyword"] == "print" or line["keyword"] == "println":
            line["args"] = newPrintArgs(line["args"])


    # printing / writing
    stringified = "\n".join([f"{line["new_i"]} : {line['keyword']} {", ".join(line['args'])}" for line in FILE])
    print(stringified)
    #print(LABELS)

if __name__ == "__main__":
    try:
        treatment()
        exit(0)
    except SyntaxError as err:
        printerr("<SyntaxError>\t", err)
        exit(1)


