import re
from pycpp.code import Block
from pycpp.serializer import Serializer
from pycpp.serializer import getTokenSummary

LNPAT = r'(\(\d+\))'


class MethodSearch:
    def __init__(self):
        self.buf = ''
        self.tokens = None

        pat = ''
        pat += '(?P<returns>%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)' % (LNPAT)
        pat += '(?P<name>%sSTRING_)' % (LNPAT)
        pat += '(%sLP_)' % (LNPAT)
        pat += '(?P<arguments>'
        pat += '('
        pat += '(%sSTRING_%s2COLONS_){0,1}' % (LNPAT, LNPAT)
        pat += '(%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)*' % (LNPAT)
        pat += '(%sMULTIPLY_|%sAND_)*' % (LNPAT, LNPAT)
        pat += '(%sWS_)*' % (LNPAT)
        pat += '(%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)*' % (LNPAT)
        pat += '(%sCOMMA_){0,1}' % (LNPAT)
        pat += '(%sWS_)*' % (LNPAT)
        pat += ')*'
        pat += ')'
        pat += '(%sRP_)' % (LNPAT)
        pat += '(%sEOC_)' % (LNPAT)
        self.meth_regex = re.compile(pat)

        argpat = ''
        argpat += '(%sSTRING_%s2COLONS_){0,1}' % (LNPAT, LNPAT)
        argpat += '(?P<argtype>%sSTRING_)' % (LNPAT)
        argpat += '(%sWS_)*' % (LNPAT)
        argpat += '(?P<ptr_ref>%sMULTIPLY_|%sAND_)*' % (LNPAT, LNPAT)
        argpat += '(%sWS_)*' % (LNPAT)
        argpat += '(?P<argname>%sSTRING_)' % (LNPAT)
        argpat += '(%sWS_)*' % (LNPAT)
        argpat += '(%sCOMMA_){0,1}' % (LNPAT)
        argpat += '(%sWS_)*' % (LNPAT)
        self.arg_regex = re.compile(argpat)

    def __isolate_pos_from_string(self, str_):
        elements = str_.split('(')
        elements = elements[1].split(')')
        return int(elements[0])

    def __search_for_token_at_pos(self, pos, tokens):
        for tok in tokens:
            if isinstance(tok, Block):
                found_token = self.__search_for_token_at_pos(pos, tok.content)
                if found_token:
                    return found_token
            else:
                if tok.pos == pos:
                    return tok

    def __getToken(self, match, groupname):
        token_pos = self.__isolate_pos_from_string(match.group(groupname))
        token = self.__search_for_token_at_pos(token_pos, self.tokens)
        return token

    def __isolate_arguments(self, argstr):
        pos = 0
        while 1:
            argmatch = self.arg_regex.search(argstr, pos)
            if argmatch:
                pos = argmatch.end()
                
                ptr_ref = ''
                if argmatch.group('ptr_ref'):
                    ptr_ref = self.__getToken(argmatch, 'ptr_ref')

                    if ptr_ref.val == '*':
                        ptr_ref = 'pointer'
                    elif ptr_ref.val == '&':
                        ptr_ref = 'reference'
                else: 
                    ptr_ref = 'value'
                
                arg_parsed = {
                    'name': self.__getToken(argmatch, 'argname'),
                    'type': self.__getToken(argmatch, 'argtype'),
                    'ptr_ref' : ptr_ref,
                }
                yield arg_parsed
            else:
                break

    def search(self, tokens):
        serializer = Serializer()

        self.tokens = tokens
        self.buf = serializer.toString(tokens, getTokenSummary)

        pos = 0

        while 1:
            match = self.meth_regex.search(self.buf, pos)
            if match:
                pos = match.end()
                match_parsed = {
                    'returns': self.__getToken(match, 'returns'),
                    'name': self.__getToken(match, 'name'),
                    'args': list(self.__isolate_arguments(match.group('arguments')))
                }

                yield match_parsed
            else:
                return