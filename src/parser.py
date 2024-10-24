class JsonLexer:
    WHITE_SPACE = [' ', '\t', '\n','\b','\r']
    JSON_SYNTAX = ['{', '}',':',',','[',']']
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
    
if __name__ == '__main__':
    x = JsonLexer()
    print(x('{"foo": null}'))
    assert x('{"foo": null}')== ['{', 'foo', ':', None, '}']