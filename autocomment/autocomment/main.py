#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Dieses Modul enthält das eigentliche Template für Qt Tools.

.. note::

       BLA BLA

"""

import argparse
import sys
import time

# print(sys.path)
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from autocomment.mainwindow import MainWindow
from pycpp.lexer import Lexer
from pycpp.blockfactory import BlockFactory
from pycpp.blockcombine import BlockCombine
from pycpp.code import TokenNewLine
from pycpp.serializer import Serializer
from pycpp.serializer import getTokenSummary
from pycpp.methodsearch import MethodSearch

import pprint

def main():
    """Die Main Funktion
    """

    parser = argparse.ArgumentParser(description='Qt Tool Template.')
    parser.add_argument(
        'filename', 
        type=str, 
        help='an integer for the accumulator'
    )
    # optional arguments:
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true"
    )

    args = parser.parse_args()
    print(args)
    app = QApplication(sys.argv)

    code = ""

    with open(args.filename, "r") as read_file:
        code = read_file.read()
    start = time.time()

    lexer = Lexer()
    lexer.input(code)
    output = list(lexer.tokens())

    cb_factory = BlockFactory()
    output2 = cb_factory.tree(output)

    doxy_factory = BlockFactory(
        begin_del_type='DOXYGENCOMMENT', 
        end_del_type='NL',
        trail_start="",
        trail_advance=""
    )
    output3 = doxy_factory.tree(output2)

    doxy_combine = BlockCombine(
        subs_type='doxygencomment',
        begin_token_type='DOXYGENCOMMENT', 
        end_token_type='NL'
    )
    output4 = doxy_combine.tree(output3)

    comment_factory = BlockFactory(
        begin_del_type='COMMENT',
        end_del_type='NL',
        trail_start="",
        trail_advance=""
    )
    output5 = comment_factory.tree(output4)

    comment_combine = BlockCombine(
        subs_type='comment',
        begin_token_type='COMMENT',
        end_token_type='NL'
    )
    output6 = comment_combine.tree(output5)

    patsearch =  MethodSearch()
    methods = list(patsearch.search(output6))

    end = time.time()

    print("Elapsed Time "+str(end - start)+" seconds")
    with open("output.txt", "w") as write_file:
        for t in output6:
            write_file.write(str(t))
            if isinstance(t, TokenNewLine):
                write_file.write('\n')

    serializer = Serializer()
    with open("output.cpp", "w") as write_file:
        write_file.write(serializer.toString(output6, getTokenSummary))


    pp = pprint.PrettyPrinter(indent=4)
    with open("methods.txt", "w") as write_file:
        write_file.write(pp.pformat(methods))

    w = MainWindow(methods)
    w.setWindowTitle('Simple')
    w.show()

    app.exec_()


if __name__ == "__main__":
    main()
