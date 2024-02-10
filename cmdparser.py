#!/bin/env python3
import os, sys, readline, platform
import re

termio_handler_support = False

if platform.system() == 'Linux':
    import termios
    termio_handler_support = True

def term_handler(key=None):
    if termio_handler_support is True:
        terminfo = save_term = termios.tcgetattr(sys.stdin)
        print(terminfo)


class CmdParser:
    def __init__(self):
        self._line_args = []
        self.null_line = []
        self.default_sep = ' \n\t\r'
        self.set_commands = []
        self.ignore = []

    def __doc__(self):
        pass
    def __getattr__(self, cls, attr):
        return getattr(cls, attr)

    def getcmd(self):
        return sys.argv

    def empty_line(self):
        pass

    def prog(self):
        return os.path.relpath(self.getcmd()[0])

    def local(self):
        return dir(self)

    def split(self, sep, string, maxsplit=0):
        regex_pattern = '|'.join(map(re.escape, sep))
        reg_extract = re.split(regex_pattern, string, maxsplit)
        return [extract for extract in reg_extract if extract != '']

    def parse_line(self, line):
        assert type(line) is str
        line = self.split(self.default_sep, line)
        line = self.ignore_args(line)

        if line == self.null_line:
            self.empty_line()
        else:
            self.run(line)

    def ignore_args(self, args):
        return [arg for arg in args if not arg in self.ignore]

    def run(self, line):
        if line == self.null_line:
            return None
        method_list = self.local()
        parse_cmd = line.pop(0)
        if parse_cmd not in self.set_commands:
            parse_cmd = 'run_' + parse_cmd
            if parse_cmd not in method_list:
                return False
        __attrcmd = self.__getattr__(self, parse_cmd)

        if not hasattr(__attrcmd, '__call__'):
            return False
        __attrcmd(line)
        return True

class inParser(CmdParser):
    def __init__(self):
        self.prompt = '(cmd) '
        self.key_value = None
        self.filter_arg = []
        self.repeat_flag = False
        self.set_loop = None
        self.set_keywords = ['ignore', 'prompt', 'key_store']
        super().__init__()

    def set_loop(self, **kwargs):
        pass

    def update_keys(self, **kwargs):
        keywords = dict(**kwargs)
        if ('ignore' in keywords.keys()):
           self.ignore.extend(keywords.get('ignore'))

    def break_loop(self):
        if self.repeat_flag is True:
            self.repeat_flag = False

    def init_loop(self):
        self.repeat_flag = True
        readFrmStdin = sys.stdin.readline
        if not sys.stdin.isatty():
            line = readFrmStdin()
            self.parse_line(line)
        else:
            while (self.repeat_flag):
                print(self.prompt, file=sys.stdout, end="", flush=True)
                try:
                    line = readFrmStdin()
                except KeyboardInterrupt:
                    print('interrupted - closed')
                    exit()
                else:
                    self.parse_line(line)
        self.repeat_flag = False

    def run_create(self, *arg):
        print('running')

if __name__ == "__main__":
    parser = inParser()
    parser.prompt = '(airbnb) '
    term_handler()
 #   parser.update_keys(ignore=[';', '&'], s=['create', '1'], p='hi')
  #  parser.init_loop()
