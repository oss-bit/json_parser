from .parser import JsonLexer,JsonParser
def mk_lexObj():
    return JsonLexer()

def mk_prsrObj():
    return JsonParser()

def parse_to_dict(string):
    tokens = JsonLexer()(string)
    return JsonParser()(tokens)