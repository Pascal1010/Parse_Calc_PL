from tree_visual import VisualTool


class TokenType:
    IDENT = 'IDENT'
    NUM = "NUM"
    LPAR = 'LPAR'
    RPAR = 'RPAR'
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'
    EXP = 'EXP'
    EOF = 'EOF'


class Token:
    def __init__(self, value, category):
        self.value = value
        self.type = category

    def __repr__(self):
        return f'Token({repr(self.value)}, {self.type})'


class TreeNode:
    def __init__(self, token, left=None, right=None):
        self.root = token
        self.right = right
        self.left = left

    def __repr__(self):
        if self.left is None and self.right is None:
            return f'{self.root}'
        else:
            return f'({self.left} {self.root} {self.right})'


class Lexer:
    def __init__(self, text_str):
        self.user_in = text_str
        self.tokens = []

    def lexer(self):
        src_list = []
        N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for token in self.user_in:
            if token == "(":
                src_list.append(Token(token, TokenType.LPAR))
            elif token == ")":
                src_list.append(Token(token, TokenType.RPAR))
            elif token == "+":
                src_list.append(Token(token, TokenType.ADD))
            elif token == "-":
                src_list.append(Token(token, TokenType.SUB))
            elif token == "*":
                src_list.append(Token(token, TokenType.MUL))
            elif token == "/":
                src_list.append(Token(token, TokenType.DIV))
            elif token == "^":
                src_list.append(Token(token, TokenType.EXP))
            elif token == " ":
                continue
            elif token == N[int(token)]:
                src_list.append(Token(token, TokenType.NUM))
        self.tokens.append(src_list[0])
        for index in range(1, len(src_list)):
            if self.tokens[-1].type == "NUM" and src_list[index].type == "NUM":
                self.tokens[-1].value = self.tokens[-1].value + src_list[index].value
            else:
                self.tokens.append(src_list[index])
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def __advance(self):
        self.position += 1

    def __current(self):
        return self.tokens[self.position]

    def __nud(self, tok: Token):
        if tok.type == TokenType.NUM:
            return TreeNode(tok.value)
        elif tok.type == TokenType.IDENT:
            return TreeNode(tok.value)
        elif tok.type == TokenType.SUB:
            return TreeNode(tok.value, TreeNode(0), self.expr(5))
        elif tok.type == TokenType.EXP:
            return TreeNode(1)
        elif tok.type == TokenType.LPAR:
            e = self.expr(0)
            if self.__current().type == TokenType.RPAR:
                self.__advance()
                return e
            else:
                raise SyntaxError("Expecting )")
        else:
            raise SyntaxError(f'No null denotation for {tok}')

    def __lbp(self, left):
        token_precedence = {'LPAR': 0, 'RPAR': 0, 'NUM': 0, 'IDEN': 0, 'ADD': 2, 'SUB': 2, 'MUL': 3, 'DIV': 3,
                            'EXP': 4, 'EOF': -1}
        try:
            return token_precedence[left.type]
        except KeyError:
            print(f'ERROR: Token Precedence value not found in dictionary:{left.type}')

    def bop(self, left, operator, right):
        return TreeNode(operator, left, right)

    def __led(self, left, token):
        if token.type == TokenType.NUM:
            return self.bop(left, token.value, self.expr(0))
        elif token.type == TokenType.IDENT:
            return self.bop(left, token.value, self.expr(0))
        elif token.type == TokenType.ADD:
            return self.bop(left, token.value, self.expr(2))
        elif token.type == TokenType.SUB:
            return self.bop(left, token.value, self.expr(2))
        elif token.type == TokenType.MUL:
            return self.bop(left, token.value, self.expr(3))
        elif token.type == TokenType.DIV:
            return self.bop(left, token.value, self.expr(3))
        elif token.type == TokenType.EXP:
            #return self.bop(left, token.value, self.expr(4))
            raised_val = None
            for i in range(0, int(self.__current().value) - 1, 1):
                if i < 1:
                    raised_val = self.bop(left, '*', left)
                else:
                    raised_val = self.bop(raised_val, '*', left)
            self.__advance()
            return raised_val

    def expr(self, limit):
        first = self.__current()
        self.__advance()
        left = self.__nud(first)
        while self.__lbp(self.__current()) > limit:
            next_elem = self.__current()
            self.__advance()
            left = self.__led(left, next_elem)
        return left


def evaluate(node):
    if node.left is None and node.right is None:
        return node.root
    left_value = evaluate(node.left)
    right_value = evaluate(node.right)
    if node.root == '+':
        return float(left_value) + float(right_value)
    elif node.root == '-':
        return float(left_value) - float(right_value)
    elif node.root == '*':
        return float(left_value) * float(right_value)
    elif node.root == '^':
        return float(left_value) ** float(right_value)
    elif node.root == '/':
        return float(left_value) / float(right_value)
    else:
        raise ValueError(f"Unknown operator: {node.root}")

def inorder_traversal(node):
    if node:
        inorder_traversal(node.left)
        print(node.root)
        inorder_traversal(node.right)


def main():
    while True:
        user_in = input('>>> ')
        if user_in.lower() == 'q':
            break
        lxr_obj = Lexer(user_in)
        tokens = lxr_obj.lexer()
        tokens.append(Token('$$', TokenType.EOF))
        print(tokens)
        parse_obj = Parser(tokens)
        tree = parse_obj.expr(0)
        print(tree)
        print(evaluate(tree))
        tool = VisualTool(tree)
        tool.run()


if __name__ == '__main__':
    main()
