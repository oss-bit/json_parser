RIGHT_BRACE = '}'
LEFT_BRACE = '{'
COLON = ':'
COMMA = ','
LEFT_BRACKET ='['
RIGHT_BRACKET = ']'


class JsonLexer:
    WHITE_SPACE = [' ', '\t', '\n','\b','\r']
    JSON_SYNTAX = [RIGHT_BRACE, LEFT_BRACE, COLON, COMMA, LEFT_BRACKET, RIGHT_BRACKET]
    QUOTE = '"'
    TRUE_LEN,NULL_LEN = 4,4
    FALSE_LEN = 5

    def __init__(self):
        self.tokens = []
    
    def lex_string(self, string):
        json_string = ''
        if string[0] != self.QUOTE:
            return None, string
        string = string[1:]
        for c in string:
            if c != self.QUOTE:
                json_string += c
                continue
            return json_string, string[len(json_string) + 1:]
        raise Exception("Expected End-of-String quote")
    
    def lex_nums(self, string):
        json_string = ''
        nums = [str(i) for i in range(10)] + ['-', 'e', '.']
        for c in string:
            if c in nums:
                json_string += c
                continue
            break
        if not len(json_string):
            return None, string
        ln = len(json_string)
        json_string = float(json_string) if '.' in json_string else int(json_string)
        return json_string, string[ln:]
    
    def lex_boolean(self, string):
        if len(string) >= self.TRUE_LEN and string[:self.TRUE_LEN] == 'true':
            return True, string[self.TRUE_LEN:]
        if len(string) >= self.FALSE_LEN and string[:self.FALSE_LEN:] == 'false':
            return False, string[self.FALSE_LEN:]
        return None, string
    
    def lex_null(self, string):
        if len(string) >= self.NULL_LEN and string[:self.NULL_LEN] == 'null':
            return None, string[self.NULL_LEN:]
        return None, string

    def lex(self, string):
        while len(string):
            json_ext, string = self.lex_string(string)
            if json_ext is not None:
                self.tokens.append(json_ext)
                continue

            json_ext, string = self.lex_nums(string)
            if json_ext is not None:
                self.tokens.append(json_ext)
                continue
            json_ext, string = self.lex_boolean(string)
            if json_ext is not None:
                self.tokens.append(json_ext)
                continue
            json_ext, string = self.lex_null(string)
            if json_ext is not None:
                self.tokens.append(json_ext)
                continue
            if string[0] in self.WHITE_SPACE:
                string = string[1:]
            if string[0] in self.JSON_SYNTAX:
                self.tokens.append(string[0])
                string = string[1:]
        
            

    def __call__(self, string):
        self.lex(string)
        return self.tokens
    
    def __str__(self):
        return self.tokens
    

class JsonParser:
    def __call__(self, tokens):
        self.json,_ = self.parse(tokens)
        return self.json
    def parse(self, tokens,root=False):
        t = tokens[0]
        if root and t != LEFT_BRACE:
            raise Exception("root must be a object")
        if t == LEFT_BRACKET:
            return self.parse_array(tokens[1:])
        elif t == LEFT_BRACE:
            return self.parse_objects(tokens[1:])
        else:
            return t, tokens[1:]
    
    def parse_array(self, tokens):
        json_array = []
        if tokens[0] == RIGHT_BRACKET:
            return json_array, tokens[1:]
        while True:
            json , tokens = self.parse(tokens)
            json_array.append(json)
            t = tokens[0]
            if t == RIGHT_BRACKET:
                return json_array, tokens
            if t != COMMA:
                raise Exception("Expected comman after array item instead got %s".format(t))
            else:
                tokens = tokens[1:] 
    
    def parse_objects(self, tokens):
        json_obj = {}
        if tokens[0] == RIGHT_BRACE:

            return json_obj, tokens[1:]
        while True:
            json_key, tokens = self.parse(tokens)
            if not isinstance(json_key, str):
                raise Exception(f"Json key must be a string instead got {type(json_key)}")
            if tokens[0] != COLON:
                raise Exception(f"Expected a colon after object key but got {tokens[[0]]} ")
            json_value, tokens = self.parse(tokens[1:])
            json_obj[json_key] = json_value
            if tokens[0] == RIGHT_BRACE:
                return json_obj, tokens[1:]
            if tokens[0] != COMMA:
                raise Exception(f"Expected a comma after key-value pair but got {tokens[0]}")
            tokens = tokens[1:]

def parse_to_dict(string):
    tokens = JsonLexer()(string)
    return JsonParser()(tokens)

if __name__ == '__main__':
    print(type(parse_to_dict('{"foo":123}')))

