import cog

class StateClass:
    def __init__(self, name, transitions=None):
        self.__name = name
        self.__indent = ""
        self.__indentSpaceCount = 0
        self.__transitions=transitions       

    def get_id(self, from_=None):
        if from_:
            return "ID_"+from_.upper()
        else:
            return "ID_"+self.__name.upper()

    def out_indent(self, str):
        cog.outl("{}{}".format(self.__indent, str))
   
    def out_nl(self):
        self.out_indent("")

    def out_begin(self):
        self.out_indent("{")

    def out_end(self):
        self.out_indent("}")

    def out_code(self, code):
        self.out_indent("{};".format(code))

    def out_comment(self, comment):
        self.out_indent("// {}".format(comment))

    def raise_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount+4
        self.__indent=" "*self.__indentSpaceCount

    def lower_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount-4
        self.__indent=" "*self.__indentSpaceCount   


    def out_transition_check(self, name, to_state):
        self.out_indent("if (check{}())".format(name))
        self.out_begin()
        self.raise_indent()
        self.out_code("setNextState({})".format(self.get_id(to_state)))
        self.out_code("return")
        self.lower_indent()
        self.out_end()

    def generate_processTransitions(self):
        self.out_indent("void {}::processTransitions()".format(
            self.__name
        ))
        self.out_begin()
        self.raise_indent()

        if self.__transitions:
            last = self.__transitions[-1]
            for transition in self.__transitions:
                self.out_transition_check(transition['name'], transition['to'])

                if transition!=last:
                    self.out_nl()
        else:
            self.out_comment("Check for transitions here ...")
        self.lower_indent()
        self.out_end()

    def out_state_check(self, name):
        self.out_indent("bool {}::{}()".format(
            self.__name, 
            "check{}".format(name)
        ))
        self.out_begin()
        self.raise_indent()
        self.out_comment("If transition must be executed return true.")
        self.out_code("return false")
        self.lower_indent()
        self.out_end()

    def out_state_check_prototype(self, name):
        self.out_indent("///")
        self.out_indent("bool {}();".format(
            "check{}".format(name)
        ))
        
    def generate_state_checks(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.out_state_check(transition['name'])
            self.out_nl()
    
    def generate_state_check_prototypes(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.out_state_check_prototype(transition['name'])
            self.out_nl()