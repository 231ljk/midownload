#!/usr/bin/env python3
"""
Nx Programming Language - Interpreter
Version: 0.1.0 (Developer Preview)
A tree-walking interpreter for the Nx programming language.
"""
import sys
from dataclasses import dataclass
from typing import Any

class TT:
    NUMBER="NUMBER"; STRING="STRING"; IDENT="IDENT"
    FUNC="FUNC"; VAR="VAR"; IF="IF"; ELSE="ELSE"; FOR="FOR"; WHILE="WHILE"
    RETURN="RETURN"; CLASS="CLASS"; THIS="THIS"; NEW="NEW"; TRUE="TRUE"; FALSE="FALSE"
    NULL="NULL"; IN="IN"; IMPORT="IMPORT"; INTERFACE="INTERFACE"; MIXIN="MIXIN"
    TRY="TRY"; CATCH="CATCH"; FINALLY="FINALLY"; THROW="THROW"; WITH="WITH"
    PLUS="PLUS"; MINUS="MINUS"; STAR="STAR"; SLASH="SLASH"; PERCENT="PERCENT"
    ASSIGN="ASSIGN"; EQ="EQ"; NEQ="NEQ"; LT="LT"; GT="GT"; LTE="LTE"; GTE="GTE"
    AND="AND"; OR="OR"; NOT="NOT"
    LPAREN="LPAREN"; RPAREN="RPAREN"; LBRACE="LBRACE"; RBRACE="RBRACE"
    LBRACKET="LBRACKET"; RBRACKET="RBRACKET"; COMMA="COMMA"; DOT="DOT"
    COLON="COLON"; SEMICOLON="SEMICOLON"; ARROW="ARROW"; DDOT="DDOT"; EOF="EOF"

KEYWORDS = {
    "func":TT.FUNC,"var":TT.VAR,"if":TT.IF,"else":TT.ELSE,"for":TT.FOR,"while":TT.WHILE,
    "return":TT.RETURN,"class":TT.CLASS,"this":TT.THIS,"new":TT.NEW,"true":TT.TRUE,
    "false":TT.FALSE,"null":TT.NULL,"in":TT.IN,"import":TT.IMPORT,"interface":TT.INTERFACE,
    "mixin":TT.MIXIN,"try":TT.TRY,"catch":TT.CATCH,"finally":TT.FINALLY,"throw":TT.THROW,
    "with":TT.WITH,
}

@dataclass
class Token:
    type: str; value: Any; line: int; col: int

class Lexer:
    def __init__(self, src):
        self.src=src; self.pos=0; self.line=1; self.col=1; self.tokens=[]
    def peek(self): return self.src[self.pos] if self.pos < len(self.src) else '\0'
    def peek2(self): return self.src[self.pos+1] if self.pos+1 < len(self.src) else '\0'
    def advance(self):
        ch=self.src[self.pos]; self.pos+=1
        if ch=='\n': self.line+=1; self.col=1
        else: self.col+=1
        return ch
    def skip_ws_cmt(self):
        while self.pos < len(self.src):
            ch=self.peek()
            if ch in ' \t\r\n': self.advance()
            elif ch=='/' and self.peek2()=='/':
                while self.peek()!='\n' and self.pos<len(self.src): self.advance()
            elif ch=='/' and self.peek2()=='*':
                self.advance(); self.advance()
                while not(self.peek()=='*' and self.peek2()=='/') and self.pos<len(self.src): self.advance()
                if self.pos<len(self.src): self.advance(); self.advance()
            else: break
    def read_number(self):
        sc=self.col; s=''; f=False
        while self.peek().isdigit() or (self.peek()=='.' and not f and self.peek2()!='.'):
            if self.peek()=='.': f=True
            s+=self.advance()
        return Token(TT.NUMBER, float(s) if f else int(s), self.line, sc)
    def read_string(self):
        sc=self.col; q=self.advance(); v=''
        while self.peek()!=q and self.pos<len(self.src):
            if self.peek()=='\\':
                self.advance(); e=self.advance()
                v+={'n':'\n','t':'\t','r':'\r','\\':'\\','"':'"',"'":"'"}.get(e,e)
            else: v+=self.advance()
        if self.peek()==q: self.advance()
        return Token(TT.STRING, v, self.line, sc)
    def read_ident(self):
        sc=self.col; s=''
        while self.peek().isalnum() or self.peek()=='_': s+=self.advance()
        return Token(KEYWORDS.get(s, TT.IDENT), s, self.line, sc)
    def tokenize(self):
        while self.pos < len(self.src):
            self.skip_ws_cmt()
            if self.pos>=len(self.src): break
            ch=self.peek(); sc=self.col
            if ch.isdigit(): self.tokens.append(self.read_number())
            elif ch in '"\'': self.tokens.append(self.read_string())
            elif ch.isalpha() or ch=='_': self.tokens.append(self.read_ident())
            elif ch=='+': self.advance(); self.tokens.append(Token(TT.PLUS,'+',self.line,sc))
            elif ch=='-':
                self.advance()
                if self.peek()=='>': self.advance(); self.tokens.append(Token(TT.ARROW,'->',self.line,sc))
                else: self.tokens.append(Token(TT.MINUS,'-',self.line,sc))
            elif ch=='*': self.advance(); self.tokens.append(Token(TT.STAR,'*',self.line,sc))
            elif ch=='/': self.advance(); self.tokens.append(Token(TT.SLASH,'/',self.line,sc))
            elif ch=='%': self.advance(); self.tokens.append(Token(TT.PERCENT,'%',self.line,sc))
            elif ch=='=':
                self.advance()
                if self.peek()=='=': self.advance(); self.tokens.append(Token(TT.EQ,'==',self.line,sc))
                else: self.tokens.append(Token(TT.ASSIGN,'=',self.line,sc))
            elif ch=='!':
                self.advance()
                if self.peek()=='=': self.advance(); self.tokens.append(Token(TT.NEQ,'!=',self.line,sc))
                else: self.tokens.append(Token(TT.NOT,'!',self.line,sc))
            elif ch=='<':
                self.advance()
                if self.peek()=='=': self.advance(); self.tokens.append(Token(TT.LTE,'<=',self.line,sc))
                else: self.tokens.append(Token(TT.LT,'<',self.line,sc))
            elif ch=='>':
                self.advance()
                if self.peek()=='=': self.advance(); self.tokens.append(Token(TT.GTE,'>=',self.line,sc))
                else: self.tokens.append(Token(TT.GT,'>',self.line,sc))
            elif ch=='&':
                self.advance()
                if self.peek()=='&': self.advance()
                self.tokens.append(Token(TT.AND,'&&',self.line,sc))
            elif ch=='|':
                self.advance()
                if self.peek()=='|': self.advance()
                self.tokens.append(Token(TT.OR,'||',self.line,sc))
            elif ch=='(': self.advance(); self.tokens.append(Token(TT.LPAREN,'(',self.line,sc))
            elif ch==')': self.advance(); self.tokens.append(Token(TT.RPAREN,')',self.line,sc))
            elif ch=='{': self.advance(); self.tokens.append(Token(TT.LBRACE,'{',self.line,sc))
            elif ch=='}': self.advance(); self.tokens.append(Token(TT.RBRACE,'}',self.line,sc))
            elif ch=='[': self.advance(); self.tokens.append(Token(TT.LBRACKET,'[',self.line,sc))
            elif ch==']': self.advance(); self.tokens.append(Token(TT.RBRACKET,']',self.line,sc))
            elif ch==',': self.advance(); self.tokens.append(Token(TT.COMMA,',',self.line,sc))
            elif ch=='.':
                self.advance()
                if self.peek()=='.': self.advance(); self.tokens.append(Token(TT.DDOT,'..',self.line,sc))
                else: self.tokens.append(Token(TT.DOT,'.',self.line,sc))
            elif ch==':': self.advance(); self.tokens.append(Token(TT.COLON,':',self.line,sc))
            elif ch==';': self.advance(); self.tokens.append(Token(TT.SEMICOLON,';',self.line,sc))
            else: self.advance()
        self.tokens.append(Token(TT.EOF,None,self.line,self.col))
        return self.tokens

class Node: pass
@dataclass
class Program(Node): stmts: list
@dataclass
class VarDecl(Node): name: str; value: object
@dataclass
class Assign(Node): target: object; value: object
@dataclass
class FuncDecl(Node): name: str; params: list; body: list
@dataclass
class ClassDecl(Node): name: str; base: object; body: list
@dataclass
class IfStmt(Node): cond: object; then: list; elifs: list; else_body: object
@dataclass
class ForStmt(Node): var: str; iterable: object; body: list
@dataclass
class WhileStmt(Node): cond: object; body: list
@dataclass
class ReturnStmt(Node): value: object
@dataclass
class ExprStmt(Node): expr: object
@dataclass
class BinaryOp(Node): op: str; left: object; right: object
@dataclass
class UnaryOp(Node): op: str; operand: object
@dataclass
class Number(Node): value: object
@dataclass
class String(Node): value: str
@dataclass
class Bool(Node): value: bool
@dataclass
class Null(Node): pass
@dataclass
class Ident(Node): name: str
@dataclass
class This(Node): pass
@dataclass
class FuncCall(Node): func: object; args: list
@dataclass
class MemberAccess(Node): obj: object; member: str
@dataclass
class IndexAccess(Node): obj: object; index: object
@dataclass
class ListLit(Node): elements: list
@dataclass
class DictLit(Node): pairs: list
@dataclass
class NewExpr(Node): class_name: str; args: list
@dataclass
class RangeExpr(Node): start: object; end: object

class Parser:
    def __init__(self, tokens): self.tokens=tokens; self.pos=0
    def cur(self): return self.tokens[self.pos]
    def advance(self):
        t=self.tokens[self.pos]
        if t.type!=TT.EOF: self.pos+=1
        return t
    def expect(self, tt):
        if self.cur().type==tt: return self.advance()
        raise SyntaxError(f"Expected {tt}, got '{self.cur().value}' at line {self.cur().line}")
    def match(self, *tts):
        if self.cur().type in tts: self.advance(); return True
        return False
    def parse(self):
        stmts=[]
        while self.cur().type!=TT.EOF:
            s=self.parse_stmt()
            if s: stmts.append(s)
        return Program(stmts)
    def parse_stmt(self):
        t=self.cur().type
        if t==TT.FUNC: return self.parse_func()
        if t==TT.CLASS: return self.parse_class()
        if t==TT.INTERFACE: return self.skip_interface()
        if t==TT.MIXIN: return self.skip_mixin()
        if t==TT.VAR: return self.parse_var()
        if t==TT.IF: return self.parse_if()
        if t==TT.FOR: return self.parse_for()
        if t==TT.WHILE: return self.parse_while()
        if t==TT.RETURN: return self.parse_return()
        if t==TT.TRY: return self.skip_try()
        if t==TT.SEMICOLON: self.advance(); return None
        return self.parse_expr_stmt()
    def skip_interface(self):
        self.advance()
        if self.cur().type==TT.IDENT: self.advance()
        if self.match(TT.LBRACE):
            d=1
            while d>0 and self.cur().type!=TT.EOF:
                if self.cur().type==TT.LBRACE: d+=1
                elif self.cur().type==TT.RBRACE: d-=1
                self.advance()
        return None
    def skip_mixin(self):
        self.advance()
        if self.cur().type==TT.IDENT: self.advance()
        if self.match(TT.LBRACE):
            d=1
            while d>0 and self.cur().type!=TT.EOF:
                if self.cur().type==TT.LBRACE: d+=1
                elif self.cur().type==TT.RBRACE: d-=1
                self.advance()
        return None
    def skip_try(self):
        self.advance()
        if self.match(TT.LBRACE):
            d=1
            while d>0 and self.cur().type!=TT.EOF:
                if self.cur().type==TT.LBRACE: d+=1
                elif self.cur().type==TT.RBRACE: d-=1
                self.advance()
        while self.cur().type in (TT.CATCH, TT.FINALLY):
            self.advance()
            if self.cur().type==TT.LPAREN:
                d=1; self.advance()
                while d>0 and self.cur().type!=TT.EOF:
                    if self.cur().type==TT.LPAREN: d+=1
                    elif self.cur().type==TT.RPAREN: d-=1
                    self.advance()
            if self.match(TT.LBRACE):
                d=1
                while d>0 and self.cur().type!=TT.EOF:
                    if self.cur().type==TT.LBRACE: d+=1
                    elif self.cur().type==TT.RBRACE: d-=1
                    self.advance()
        return None
    def parse_var(self):
        self.expect(TT.VAR); name=self.expect(TT.IDENT).value; val=None
        if self.match(TT.ASSIGN): val=self.parse_expr()
        self.match(TT.SEMICOLON); return VarDecl(name, val)
    def parse_func(self):
        self.expect(TT.FUNC); name=self.expect(TT.IDENT).value; self.expect(TT.LPAREN)
        params=[]
        if self.cur().type!=TT.RPAREN:
            params.append(self.expect(TT.IDENT).value)
            while self.match(TT.COMMA):
                if self.cur().type==TT.RPAREN: break
                params.append(self.expect(TT.IDENT).value)
        self.expect(TT.RPAREN)
        if self.match(TT.ARROW): self.skip_type()
        body=self.parse_block(); return FuncDecl(name, params, body)
    def skip_type(self):
        if self.cur().type==TT.IDENT:
            self.advance()
            if self.match(TT.LBRACKET):
                d=1
                while d>0 and self.cur().type!=TT.EOF:
                    if self.cur().type==TT.LBRACKET: d+=1
                    elif self.cur().type==TT.RBRACKET: d-=1
                    self.advance()
    def parse_class(self):
        self.expect(TT.CLASS); name=self.expect(TT.IDENT).value
        if self.match(TT.LBRACKET):
            d=1
            while d>0 and self.cur().type!=TT.EOF:
                if self.cur().type==TT.LBRACKET: d+=1
                elif self.cur().type==TT.RBRACKET: d-=1
                self.advance()
        base=None
        if self.match(TT.COLON):
            base=self.expect(TT.IDENT).value
            while self.match(TT.COMMA):
                if self.cur().type==TT.IDENT: self.advance()
        if self.match(TT.WITH):
            if self.cur().type==TT.IDENT: self.advance()
        body=self.parse_class_body(); return ClassDecl(name, base, body)
    def parse_class_body(self):
        self.expect(TT.LBRACE); members=[]
        while self.cur().type!=TT.RBRACE and self.cur().type!=TT.EOF:
            if self.cur().type==TT.VAR:
                self.advance(); name=self.expect(TT.IDENT).value; val=None
                if self.match(TT.ASSIGN): val=self.parse_expr()
                self.match(TT.SEMICOLON); members.append(VarDecl(name, val))
            elif self.cur().type==TT.FUNC: members.append(self.parse_func())
            else: self.advance()
        self.expect(TT.RBRACE); return members
    def parse_if(self):
        self.expect(TT.IF); cond=self.parse_expr(); then=self.parse_block(); elifs=[]
        while self.cur().type==TT.ELSE and self.tokens[self.pos+1].type==TT.IF:
            self.advance(); self.advance(); c=self.parse_expr(); b=self.parse_block(); elifs.append((c,b))
        else_b=None
        if self.match(TT.ELSE): else_b=self.parse_block()
        return IfStmt(cond, then, elifs, else_b)
    def parse_for(self):
        self.expect(TT.FOR); var=self.expect(TT.IDENT).value; self.expect(TT.IN)
        it=self.parse_expr(); body=self.parse_block(); return ForStmt(var, it, body)
    def parse_while(self):
        self.expect(TT.WHILE); cond=self.parse_expr(); body=self.parse_block(); return WhileStmt(cond, body)
    def parse_return(self):
        self.expect(TT.RETURN); val=None
        if self.cur().type not in (TT.SEMICOLON, TT.RBRACE, TT.EOF): val=self.parse_expr()
        self.match(TT.SEMICOLON); return ReturnStmt(val)
    def parse_block(self):
        self.expect(TT.LBRACE); stmts=[]
        while self.cur().type!=TT.RBRACE and self.cur().type!=TT.EOF:
            s=self.parse_stmt()
            if s: stmts.append(s)
        self.expect(TT.RBRACE); return stmts
    def parse_expr_stmt(self):
        if self.cur().type==TT.IDENT and self.tokens[self.pos+1].type==TT.COMMA:
            names=[self.advance().value]
            while self.match(TT.COMMA):
                if self.cur().type==TT.IDENT: names.append(self.advance().value)
                else: break
            if self.match(TT.ASSIGN):
                val=self.parse_expr(); self.match(TT.SEMICOLON)
                return ExprStmt(FuncCall(Ident("__tuple_unpack__"), [ListLit([Ident(n) for n in names]), val]))
        expr=self.parse_expr(); self.match(TT.SEMICOLON); return ExprStmt(expr)
    def parse_expr(self): return self.parse_assign()
    def parse_assign(self):
        left=self.parse_or()
        if self.cur().type==TT.ASSIGN: self.advance(); val=self.parse_assign(); return Assign(left, val)
        return left
    def parse_or(self):
        l=self.parse_and()
        while self.cur().type==TT.OR: self.advance(); r=self.parse_and(); l=BinaryOp("||",l,r)
        return l
    def parse_and(self):
        l=self.parse_eq()
        while self.cur().type==TT.AND: self.advance(); r=self.parse_eq(); l=BinaryOp("&&",l,r)
        return l
    def parse_eq(self):
        l=self.parse_cmp()
        while self.cur().type in (TT.EQ,TT.NEQ): op=self.advance().value; r=self.parse_cmp(); l=BinaryOp(op,l,r)
        return l
    def parse_cmp(self):
        l=self.parse_range()
        while self.cur().type in (TT.LT,TT.GT,TT.LTE,TT.GTE): op=self.advance().value; r=self.parse_range(); l=BinaryOp(op,l,r)
        return l
    def parse_range(self):
        l=self.parse_add()
        if self.cur().type==TT.DDOT: self.advance(); r=self.parse_add(); return RangeExpr(l,r)
        return l
    def parse_add(self):
        l=self.parse_mul()
        while self.cur().type in (TT.PLUS,TT.MINUS): op=self.advance().value; r=self.parse_mul(); l=BinaryOp(op,l,r)
        return l
    def parse_mul(self):
        l=self.parse_unary()
        while self.cur().type in (TT.STAR,TT.SLASH,TT.PERCENT): op=self.advance().value; r=self.parse_unary(); l=BinaryOp(op,l,r)
        return l
    def parse_unary(self):
        if self.cur().type in (TT.MINUS,TT.NOT): op=self.advance().value; o=self.parse_unary(); return UnaryOp(op,o)
        return self.parse_postfix()
    def parse_postfix(self):
        e=self.parse_primary()
        while True:
            if self.cur().type==TT.DOT: self.advance(); m=self.expect(TT.IDENT).value; e=MemberAccess(e,m)
            elif self.cur().type==TT.LPAREN: args=self.parse_args(); e=FuncCall(e,args)
            elif self.cur().type==TT.LBRACKET: self.advance(); idx=self.parse_expr(); self.expect(TT.RBRACKET); e=IndexAccess(e,idx)
            else: break
        return e
    def parse_args(self):
        self.expect(TT.LPAREN); args=[]
        if self.cur().type!=TT.RPAREN:
            args.append(self.parse_expr())
            while self.match(TT.COMMA):
                if self.cur().type==TT.RPAREN: break
                args.append(self.parse_expr())
        self.expect(TT.RPAREN); return args
    def parse_primary(self):
        t=self.cur()
        if t.type==TT.NUMBER: self.advance(); return Number(t.value)
        if t.type==TT.STRING: self.advance(); return String(t.value)
        if t.type==TT.TRUE: self.advance(); return Bool(True)
        if t.type==TT.FALSE: self.advance(); return Bool(False)
        if t.type==TT.NULL: self.advance(); return Null()
        if t.type==TT.THIS: self.advance(); return This()
        if t.type==TT.NEW: self.advance(); cn=self.expect(TT.IDENT).value; args=self.parse_args(); return NewExpr(cn,args)
        if t.type==TT.IDENT: self.advance(); return Ident(t.value)
        if t.type==TT.LPAREN: self.advance(); e=self.parse_expr(); self.expect(TT.RPAREN); return e
        if t.type==TT.LBRACKET: return self.parse_list()
        if t.type==TT.LBRACE: return self.parse_dict()
        raise SyntaxError(f"Unexpected '{t.value}' at line {t.line}")
    def parse_list(self):
        self.expect(TT.LBRACKET); elems=[]
        if self.cur().type!=TT.RBRACKET:
            first=self.parse_expr()
            if self.cur().type==TT.FOR:
                self.advance()
                if self.cur().type==TT.IDENT: self.advance()
                self.expect(TT.IN); self.parse_expr()
                if self.match(TT.IF): self.parse_expr()
                self.expect(TT.RBRACKET); return ListLit([])
            elems.append(first)
            while self.match(TT.COMMA):
                if self.cur().type==TT.RBRACKET: break
                elems.append(self.parse_expr())
        self.expect(TT.RBRACKET); return ListLit(elems)
    def parse_dict(self):
        self.expect(TT.LBRACE); pairs=[]
        if self.cur().type!=TT.RBRACE:
            k=self.parse_expr(); self.expect(TT.COLON); v=self.parse_expr(); pairs.append((k,v))
            while self.match(TT.COMMA):
                if self.cur().type==TT.RBRACE: break
                k=self.parse_expr(); self.expect(TT.COLON); v=self.parse_expr(); pairs.append((k,v))
        self.expect(TT.RBRACE); return DictLit(pairs)

class V: pass
class VNum(V):
    def __init__(s,v): s.v=v
    def __repr__(s): return str(s.v)
class VStr(V):
    def __init__(s,v): s.v=v
    def __repr__(s): return s.v
class VBool(V):
    def __init__(s,v): s.v=v
    def __repr__(s): return "true" if s.v else "false"
class VNull(V):
    def __repr__(s): return "null"
class VList(V):
    def __init__(s,e=None): s.e=e or []
    def __repr__(s): return "["+", ".join(repr(x) for x in s.e)+"]"
class VDict(V):
    def __init__(s,p=None): s.p=p or {}
    def __repr__(s): return "{"+", ".join(f"{repr(k)}:{repr(v)}" for k,v in s.p.items())+"}"
class VFunc(V):
    def __init__(s,name,params,body,closure,native=None):
        s.name=name; s.params=params; s.body=body; s.closure=closure; s.native=native
    def __repr__(s): return f"<func {s.name}>"
class VClass(V):
    def __init__(s,name,base,methods,fields):
        s.name=name; s.base=base; s.methods=methods; s.fields=fields
    def __repr__(s): return f"<class {s.name}>"
class VInst(V):
    def __init__(s,klass):
        s.klass=klass; s.fields={}
        for n,v in klass.fields.items(): s.fields[n]=v
    def __repr__(s): return f"<{s.klass.name}>"
class VSuper(V):
    def __init__(s,instance): s.instance=instance
    def __repr__(s): return "<super>"
class ReturnExc(Exception):
    def __init__(s,v): s.v=v

class Env:
    def __init__(s,parent=None): s.vars={}; s.parent=parent
    def get(s,name):
        if name in s.vars: return s.vars[name]
        if s.parent: return s.parent.get(name)
        raise NameError(f"Undefined: {name}")
    def set(s,name,val):
        if name in s.vars: s.vars[name]=val; return
        if s.parent:
            try: s.parent.set(name,val); return
            except NameError: pass
        s.vars[name]=val
    def define(s,name,val): s.vars[name]=val

class Interpreter:
    def __init__(s): s.glob=Env(); s._builtins()
    def _builtins(s):
        def nx_print(*args): print(" ".join(s._tostr(a) for a in args)); return VNull()
        def nx_len(*args):
            if len(args)!=1: raise TypeError("len() takes 1 arg")
            v=args[0]
            if isinstance(v,VStr): return VNum(len(v.v))
            if isinstance(v,VList): return VNum(len(v.e))
            if isinstance(v,VDict): return VNum(len(v.p))
            raise TypeError(f"len() not supported")
        def nx_type(*args):
            if len(args)!=1: raise TypeError("type() takes 1 arg")
            v=args[0]
            for t,n in [(VNum,"number"),(VStr,"string"),(VBool,"bool"),(VNull,"null"),
                         (VList,"list"),(VDict,"dict"),(VFunc,"function"),(VClass,"class"),(VInst,"object")]:
                if isinstance(v,t): return VStr(n)
            return VStr("unknown")
        def nx_int(*args):
            if len(args)!=1: raise TypeError("int() takes 1 arg")
            v=args[0]
            if isinstance(v,VNum): return VNum(int(v.v))
            if isinstance(v,VStr): return VNum(int(v.v))
            raise TypeError("Cannot convert to int")
        def nx_str(*args):
            if len(args)!=1: raise TypeError("str() takes 1 arg")
            return VStr(s._tostr(args[0]))
        def nx_range(*args):
            if len(args)==1: st,en=0,int(args[0].v)
            elif len(args)==2: st,en=int(args[0].v),int(args[1].v)
            else: raise TypeError("range() takes 1 or 2 args")
            return VList([VNum(i) for i in range(st,en)])
        def nx_abs(*args):
            if len(args)!=1: raise TypeError("abs() takes 1 arg")
            v=args[0]
            if isinstance(v,VNum): return VNum(abs(v.v))
            raise TypeError("abs() not supported")
        def nx_max(*args):
            if not args: raise TypeError("max() takes at least 1 arg")
            items=args[0].e if len(args)==1 and isinstance(args[0],VList) else args
            if not items: return VNull()
            return max(items, key=lambda x: x.v if isinstance(x,VNum) else 0)
        def nx_min(*args):
            if not args: raise TypeError("min() takes at least 1 arg")
            items=args[0].e if len(args)==1 and isinstance(args[0],VList) else args
            if not items: return VNull()
            return min(items, key=lambda x: x.v if isinstance(x,VNum) else 0)
        def nx_sum(*args):
            if len(args)!=1 or not isinstance(args[0],VList): raise TypeError("sum() takes a list")
            total=0
            for x in args[0].e:
                if isinstance(x,VNum): total+=x.v
            return VNum(total)
        def tuple_unpack(names_val, value):
            if not isinstance(names_val,VList): return VNull()
            names=[n.name for n in names_val.e if isinstance(n,Ident)]
            vals=value.e if isinstance(value,VList) else [value]
            for i,name in enumerate(names):
                s.glob.set(name, vals[i] if i<len(vals) else VNull())
            return VNull()
        s._def_native("print", nx_print)
        s._def_native("len", nx_len)
        s._def_native("type", nx_type)
        s._def_native("int", nx_int)
        s._def_native("str", nx_str)
        s._def_native("range", nx_range)
        s._def_native("abs", nx_abs)
        s._def_native("max", nx_max)
        s._def_native("min", nx_min)
        s._def_native("sum", nx_sum)
        s._def_native("__tuple_unpack__", tuple_unpack)
        s.glob.define("pi", VNum(3.141592653589793))
        s.glob.define("true", VBool(True))
        s.glob.define("false", VBool(False))
        s.glob.define("null", VNull())
    def _def_native(s, name, fn): s.glob.define(name, VFunc(name, ["*args"], None, None, native=fn))
    def _tostr(s, v):
        if isinstance(v,VStr): return v.v
        if isinstance(v,VNull): return "null"
        if isinstance(v,VBool): return "true" if v.v else "false"
        return repr(v)
    def run(s, program):
        for stmt in program.stmts: s.exec(stmt, s.glob)
    def exec(s, stmt, env):
        if isinstance(stmt, VarDecl):
            v=s.eval(stmt.value,env) if stmt.value else VNull(); env.define(stmt.name, v)
        elif isinstance(stmt, Assign):
            v=s.eval(stmt.value,env); s._assign(stmt.target,v,env)
        elif isinstance(stmt, FuncDecl):
            env.define(stmt.name, VFunc(stmt.name,stmt.params,stmt.body,env))
        elif isinstance(stmt, ClassDecl):
            methods={}; fields={}
            for m in stmt.body:
                if isinstance(m,FuncDecl): methods[m.name]=VFunc(m.name,m.params,m.body,None)
                elif isinstance(m,VarDecl): fields[m.name]=s.eval(m.value,env) if m.value else VNull()
            base=None
            if stmt.base:
                try:
                    bv=env.get(stmt.base)
                    if isinstance(bv,VClass): base=bv
                except NameError: pass
            env.define(stmt.name, VClass(stmt.name,base,methods,fields))
        elif isinstance(stmt, IfStmt):
            if s._truthy(s.eval(stmt.cond,env)): s._exec_block(stmt.then, Env(env))
            else:
                done=False
                for c,b in stmt.elifs:
                    if s._truthy(s.eval(c,env)): s._exec_block(b,Env(env)); done=True; break
                if not done and stmt.else_body: s._exec_block(stmt.else_body,Env(env))
        elif isinstance(stmt, ForStmt):
            it=s.eval(stmt.iterable,env); items=s._iter_items(it)
            for item in items:
                le=Env(env); le.define(stmt.var,item)
                try: s._exec_block(stmt.body,le)
                except ReturnExc: raise
        elif isinstance(stmt, WhileStmt):
            while s._truthy(s.eval(stmt.cond,env)):
                try: s._exec_block(stmt.body,Env(env))
                except ReturnExc: raise
        elif isinstance(stmt, ReturnStmt):
            v=s.eval(stmt.value,env) if stmt.value else VNull(); raise ReturnExc(v)
        elif isinstance(stmt, ExprStmt): s.eval(stmt.expr,env)
    def _exec_block(s, stmts, env):
        for st in stmts: s.exec(st,env)
    def _assign(s, target, val, env):
        if isinstance(target,Ident): env.set(target.name,val)
        elif isinstance(target,MemberAccess):
            obj=s.eval(target.obj,env)
            if isinstance(obj,VInst): obj.fields[target.member]=val
            else: raise TypeError(f"Cannot assign to member of {type(obj).__name__}")
        elif isinstance(target,IndexAccess):
            obj=s.eval(target.obj,env); idx=s.eval(target.index,env)
            if isinstance(obj,VList): obj.e[int(idx.v)]=val
            elif isinstance(obj,VDict): obj.p[s._hkey(idx)]=val
            else: raise TypeError(f"Cannot index assign to {type(obj).__name__}")
        else: raise TypeError("Invalid assignment target")
    def _truthy(s, v):
        if isinstance(v,VBool): return v.v
        if isinstance(v,VNull): return False
        if isinstance(v,VNum): return v.v!=0
        if isinstance(v,VStr): return len(v.v)>0
        if isinstance(v,VList): return len(v.e)>0
        if isinstance(v,VDict): return len(v.p)>0
        return True
    def _iter_items(s, v):
        if isinstance(v,VList): return v.e
        if isinstance(v,VStr): return [VStr(c) for c in v.v]
        if isinstance(v,VDict): return [VStr(k) if isinstance(k,str) else VNum(k) for k in v.p.keys()]
        raise TypeError(f"Cannot iterate over {type(v).__name__}")
    def _hkey(s, k):
        if isinstance(k,VStr): return k.v
        if isinstance(k,VNum): return k.v
        if isinstance(k,VBool): return k.v
        return repr(k)
    def eval(s, expr, env):
        if isinstance(expr,Assign): v=s.eval(expr.value,env); s._assign(expr.target,v,env); return v
        if isinstance(expr,Number): return VNum(expr.value)
        if isinstance(expr,String): return VStr(expr.value)
        if isinstance(expr,Bool): return VBool(expr.value)
        if isinstance(expr,Null): return VNull()
        if isinstance(expr,Ident): return env.get(expr.name)
        if isinstance(expr,This): return env.get("this")
        if isinstance(expr,BinaryOp): return s._bin(expr,env)
        if isinstance(expr,UnaryOp): return s._un(expr,env)
        if isinstance(expr,FuncCall): return s._call(expr,env)
        if isinstance(expr,MemberAccess): obj=s.eval(expr.obj,env); return s._member(obj,expr.member,env)
        if isinstance(expr,IndexAccess):
            obj=s.eval(expr.obj,env); idx=s.eval(expr.index,env)
            if isinstance(obj,VList): return obj.e[int(idx.v)]
            if isinstance(obj,VDict): return obj.p.get(s._hkey(idx),VNull())
            if isinstance(obj,VStr): return VStr(obj.v[int(idx.v)])
            raise TypeError(f"Cannot index {type(obj).__name__}")
        if isinstance(expr,ListLit): return VList([s.eval(e,env) for e in expr.elements])
        if isinstance(expr,DictLit):
            p={}
            for k_ast,v_ast in expr.pairs: k=s.eval(k_ast,env); v=s.eval(v_ast,env); p[s._hkey(k)]=v
            return VDict(p)
        if isinstance(expr,NewExpr): return s._new(expr,env)
        if isinstance(expr,RangeExpr):
            st=int(s.eval(expr.start,env).v); en=int(s.eval(expr.end,env).v)
            return VList([VNum(i) for i in range(st,en)])
        raise TypeError(f"Unknown expr: {type(expr).__name__}")
    def _bin(s, e, env):
        if e.op=="&&":
            l=s.eval(e.left,env)
            if not s._truthy(l): return l
            return s.eval(e.right,env)
        if e.op=="||":
            l=s.eval(e.left,env)
            if s._truthy(l): return l
            return s.eval(e.right,env)
        l=s.eval(e.left,env); r=s.eval(e.right,env); op=e.op
        if op=="+" and (isinstance(l,VStr) or isinstance(r,VStr)): return VStr(s._tostr(l)+s._tostr(r))
        if isinstance(l,VNum) and isinstance(r,VNum):
            a,b=l.v,r.v
            if op=="+": return VNum(a+b)
            if op=="-": return VNum(a-b)
            if op=="*": return VNum(a*b)
            if op=="/": return VNum(a/b)
            if op=="%": return VNum(a%b)
            if op=="==": return VBool(a==b)
            if op=="!=": return VBool(a!=b)
            if op=="<": return VBool(a<b)
            if op==">": return VBool(a>b)
            if op=="<=": return VBool(a<=b)
            if op==">=": return VBool(a>=b)
        if op=="==": return VBool(s._equal(l,r))
        if op=="!=": return VBool(not s._equal(l,r))
        if op=="+" and isinstance(l,VList) and isinstance(r,VList): return VList(l.e+r.e)
        raise TypeError(f"Unsupported: {type(l).__name__} {op} {type(r).__name__}")
    def _equal(s, a, b):
        if type(a)!=type(b): return False
        if isinstance(a,VNum): return a.v==b.v
        if isinstance(a,VStr): return a.v==b.v
        if isinstance(a,VBool): return a.v==b.v
        if isinstance(a,VNull): return True
        if isinstance(a,VList):
            if len(a.e)!=len(b.e): return False
            return all(s._equal(x,y) for x,y in zip(a.e,b.e))
        if isinstance(a,VDict):
            if len(a.p)!=len(b.p): return False
            for k in a.p:
                if k not in b.p: return False
                if not s._equal(a.p[k],b.p[k]): return False
            return True
        return a is b
    def _un(s, e, env):
        o=s.eval(e.operand,env)
        if e.op=="-":
            if isinstance(o,VNum): return VNum(-o.v)
            raise TypeError(f"Cannot negate {type(o).__name__}")
        if e.op=="!": return VBool(not s._truthy(o))
        raise TypeError(f"Unknown unary: {e.op}")
    def _call(s, e, env):
        fv=s.eval(e.func,env); args=[s.eval(a,env) for a in e.args]
        if isinstance(fv,VFunc):
            if fv.native: return fv.native(*args)
            return s._call_func(fv,args,env)
        if isinstance(fv,VClass): return s._instantiate(fv,args,env)
        raise TypeError(f"{type(fv).__name__} is not callable")
    def _call_func(s, func, args, call_env):
        fe=Env(func.closure if func.closure else call_env)
        try:
            this_val=fe.get("this")
            if isinstance(this_val,VInst): fe.define("super", VSuper(this_val))
        except NameError: pass
        if func.params and func.params[0]=="*args": fe.define("args", VList(args))
        else:
            for i,p in enumerate(func.params): fe.define(p, args[i] if i<len(args) else VNull())
        try: s._exec_block(func.body,fe)
        except ReturnExc as ex: return ex.v
        return VNull()
    def _instantiate(s, klass, args, env):
        inst=VInst(klass)
        init=s._find_method(klass,"init")
        if init:
            me=Env(env); me.define("this",inst); me.define("super",VSuper(inst))
            for i,p in enumerate(init.params): me.define(p, args[i] if i<len(args) else VNull())
            try: s._exec_block(init.body,me)
            except ReturnExc: pass
        return inst
    def _find_method(s, klass, name):
        if name in klass.methods: return klass.methods[name]
        if klass.base: return s._find_method(klass.base,name)
        return None
    def _member(s, obj, name, env):
        if isinstance(obj,VSuper):
            klass=obj.instance.klass
            if klass.base and name in klass.base.methods:
                m=klass.base.methods[name]
                be=Env(env); be.define("this",obj.instance)
                return VFunc(m.name,m.params,m.body,be)
            raise AttributeError(f"super has no attribute '{name}'")
        if isinstance(obj,VInst):
            if name in obj.fields: return obj.fields[name]
            m=s._find_method(obj.klass,name)
            if m:
                be=Env(env); be.define("this",obj)
                return VFunc(m.name,m.params,m.body,be)
            raise AttributeError(f"'{obj.klass.name}' has no attribute '{name}'")
        if isinstance(obj,VClass):
            if name in obj.methods: return obj.methods[name]
            raise AttributeError(f"Class '{obj.name}' has no attribute '{name}'")
        if isinstance(obj,VStr):
            if name=="length": return VNum(len(obj.v))
            if name=="upper": return VFunc("upper",[],None,None,native=lambda: VStr(obj.v.upper()))
            if name=="lower": return VFunc("lower",[],None,None,native=lambda: VStr(obj.v.lower()))
            if name=="strip": return VFunc("strip",[],None,None,native=lambda: VStr(obj.v.strip()))
            if name=="split":
                def split_fn(*args):
                    sep=args[0].v if args else None
                    return VList([VStr(p) for p in obj.v.split(sep)])
                return VFunc("split",["sep"],None,None,native=split_fn)
            if name=="contains":
                def contains_fn(*args):
                    if not args: return VBool(False)
                    return VBool(args[0].v in obj.v)
                return VFunc("contains",["sub"],None,None,native=contains_fn)
            if name=="startsWith":
                def sw_fn(*args):
                    if not args: return VBool(False)
                    return VBool(obj.v.startswith(args[0].v))
                return VFunc("startsWith",["prefix"],None,None,native=sw_fn)
            if name=="endsWith":
                def ew_fn(*args):
                    if not args: return VBool(False)
                    return VBool(obj.v.endswith(args[0].v))
                return VFunc("endsWith",["suffix"],None,None,native=ew_fn)
            raise AttributeError(f"String has no attribute '{name}'")
        if isinstance(obj,VList):
            if name=="length": return VNum(len(obj.e))
            if name=="append":
                def ap(*args):
                    if len(args)!=1: raise TypeError("append() takes 1 arg")
                    obj.e.append(args[0]); return VNull()
                return VFunc("append",["item"],None,None,native=ap)
            if name=="pop":
                def pp(*args):
                    if obj.e: return obj.e.pop()
                    return VNull()
                return VFunc("pop",[],None,None,native=pp)
            if name=="contains":
                def ct(*args):
                    if not args: return VBool(False)
                    return VBool(any(s._equal(x,args[0]) for x in obj.e))
                return VFunc("contains",["item"],None,None,native=ct)
            if name=="indexOf":
                def io(*args):
                    if not args: return VNum(-1)
                    for i,x in enumerate(obj.e):
                        if s._equal(x,args[0]): return VNum(i)
                    return VNum(-1)
                return VFunc("indexOf",["item"],None,None,native=io)
            if name=="join":
                def jn(*args):
                    sep=args[0].v if args else ","
                    return VStr(sep.join(s._tostr(x) for x in obj.e))
                return VFunc("join",["sep"],None,None,native=jn)
            if name=="reverse":
                def rv(*args): obj.e.reverse(); return VNull()
                return VFunc("reverse",[],None,None,native=rv)
            if name=="sort":
                def st(*args):
                    obj.e.sort(key=lambda x: x.v if isinstance(x,VNum) else s._tostr(x))
                    return VNull()
                return VFunc("sort",[],None,None,native=st)
            if name=="first": return obj.e[0] if obj.e else VNull()
            if name=="last": return obj.e[-1] if obj.e else VNull()
            raise AttributeError(f"List has no attribute '{name}'")
        if isinstance(obj,VDict):
            if name=="length": return VNum(len(obj.p))
            if name=="keys":
                def ks(*args):
                    return VList([VStr(k) if isinstance(k,str) else VNum(k) for k in obj.p.keys()])
                return VFunc("keys",[],None,None,native=ks)
            if name=="values":
                def vs(*args): return VList(list(obj.p.values()))
                return VFunc("values",[],None,None,native=vs)
            if name=="contains":
                def ct(*args):
                    if not args: return VBool(False)
                    return VBool(s._hkey(args[0]) in obj.p)
                return VFunc("contains",["key"],None,None,native=ct)
            raise AttributeError(f"Dict has no attribute '{name}'")
        raise AttributeError(f"{type(obj).__name__} has no attribute '{name}'")

def run_file(filename):
    with open(filename,'r',encoding='utf-8') as f: src=f.read()
    lex=Lexer(src); tokens=lex.tokenize()
    parser=Parser(tokens); program=parser.parse()
    interp=Interpreter(); interp.run(program)

def run_repl():
    print("Nx Programming Language v0.1.0 REPL")
    print("Type 'exit' or Ctrl+C to quit\n")
    interp=Interpreter()
    while True:
        try:
            line=input("nx> ")
            if line.strip() in ("exit","quit",".exit"): break
            if not line.strip(): continue
            lex=Lexer(line); tokens=lex.tokenize()
            parser=Parser(tokens); program=parser.parse()
            for stmt in program.stmts:
                if isinstance(stmt,ExprStmt):
                    r=interp.eval(stmt.expr,interp.glob)
                    if not isinstance(r,VNull): print(repr(r))
                else: interp.exec(stmt,interp.glob)
        except KeyboardInterrupt: print("\nGoodbye!"); break
        except Exception as ex: print(f"Error: {ex}")

def main():
    if len(sys.argv)<2: run_repl(); return
    cmd=sys.argv[1]
    if cmd=="run":
        if len(sys.argv)<3: print("Usage: nx run <file.nx>"); sys.exit(1)
        run_file(sys.argv[2])
    elif cmd=="repl": run_repl()
    elif cmd=="version":
        print("Nx Programming Language v0.1.0")
        print("Developer Preview")
        print(f"Python: {sys.version.split()[0]}")
    elif cmd=="help":
        print("Nx Programming Language v0.1.0\n")
        print("Usage: nx <command> [options]\n")
        print("Commands:")
        print("  run <file.nx>  Run an Nx script")
        print("  repl            Start interactive REPL")
        print("  version         Show version")
        print("  help            Show this help")
    else: run_file(cmd)

if __name__=="__main__": main()
