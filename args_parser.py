__author__ = "Shlomy Balulu"

from argparse import ArgumentParser
import sys

class ArgsParser():

    def __init__(self):
        self.__args = self.parse()

    def parse(self):
        """
        extracting user input using python argparse lib
        :return: args object (ArgumentParser instance)
        """
        try:
            parser = ArgumentParser()
            parser.add_argument('--collect', dest='collect', action='store_true')
            parser.add_argument('--search', nargs=1)
            args = parser.parse_args()
        except Exception as err:
            print err
            return None

        return args


    def get_args(self):
        return self.__args.__dict__
