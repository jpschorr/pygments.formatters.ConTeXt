# -*- coding: utf-8 -*-
"""
    pygments.formatters.context
    ~~~~~~~~~~~~~~~~~~~~~

    Formatter for ConTeXt verbatim output

    :copyright: Copyright 2013 by Josh Pschorr <josh@pschorr.org>
    :license: 2-clause BSD, see LICENSE for details.
"""

import re

from pygments.formatter import Formatter
from pygments.util import OptionError, get_choice_opt, b
from pygments.token import Token, STANDARD_TYPES
from pygments.console import colorize

__all__ = ['ContextFormatter']

def escape(text):
    return  text. \
        replace('\\\\', '\x00'). \
        replace('\\', '\x01'). \
        replace('\x01', '\letterbackslash{}'). \
        replace('\x00', '\\\\\\\\'). \
        replace(r'{', r'\{'). \
        replace(r'}', r'\}'). \
        replace(r'&', r'\&'). \
        replace(r'%', r'\%'). \
        replace(r'$', r'\$'). \
        replace(r'#', r'\#')

def _get_ttype_name(ttype):
    fname = STANDARD_TYPES.get(ttype)
    if fname:
        return fname
    aname = ''
    while fname is None:
        aname = ttype[-1] + aname
        ttype = ttype.parent
        fname = STANDARD_TYPES.get(ttype)
    return fname + aname

num_replacements = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
num_p = re.compile(r'([0-9])')
def _escape_macro_name(name):
    parts = num_p.split(name)
    for idx, part in enumerate(parts):
        if num_p.search(part):
            parts[idx] = num_replacements[int(part)]

    return ''.join(parts)

class ContextFormatter(Formatter):
    r"""
    Format tokens as ConTeXt verbatim code.
    """
    name = 'ConTeXt'
    aliases = ['context', 'tex']
    filenames = ['*.tex']

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        self.codename = options.get('codename', 'code')
        self.escapeopen = options.get('escapeopen', '/BTEX')
        self.escapeclose = options.get('escapeclose', '/ETEX')
        self.commandprefix = options.get('commandprefix', 'PYG')

        self.p = re.compile(r'(\s)')

        self._create_stylesheet()


    def _create_stylesheet(self):
        self.styles = {}
        self.colors = {}

        color_count = [0]
        def _get_color(color):
            color_name = self.commandprefix + '@Color@' + str(color_count[0])
            color_cmd = '\\' + color_name + '{}'
            color_count[0] += 1
            if color_name not in self.colors:
                self.colors[color_name] = color, color_name, color_cmd
            return color_name

        for ttype, style in self.style:
            name = _get_ttype_name(ttype)
            commanddef_pre = ''
            commanddef_post = ''

            if style['bold']:
                commanddef_pre += r'\bf{}'
            if style['italic']:
                commanddef_pre += r'\it{}'
            if style['underline']:
                commanddef_pre += r'\underbar{}'
            if style['roman']:
                commanddef_pre += r'\rm{}'
            if style['sans']:
                commanddef_pre += r'\ss{}'
            if style['mono']:
                commanddef_pre += r'\tt{}'
            if style['color']:
                commanddef_pre += r'\startcolor[' + _get_color(style['color']) + ']{}'
                commanddef_post += r'\stopcolor{}'

            self.styles[ttype] = (name, '\\'+self.commandprefix+_escape_macro_name(name), commanddef_pre, commanddef_post)

    def get_style_defs(self, arg=''):
        styles = [r'\setupcolor[hex]']

        for color, color_name, color_cmd in self.colors.values():
            styles.append(r'\definecolor[%s][h=%s]' % (color_name, color))

        for name, command, commanddef_pre, commanddef_post in self.styles.values():
            styles.append(r'\def%s#1{%s{#1}%s}' % (command, commanddef_pre, commanddef_post))

        return '\n'.join(styles)


    def write(self, value, ttype, outfile):
        lines = value.split('\n')
        first = True
        for line in lines:
            if not first:
                outfile.write('\n')
            first = False
            if line:
                self.write_line(line, ttype, outfile)

    def write_line(self, line, ttype, outfile):
        segments = self.p.split(line)
        for seg in segments:
            if seg:
                if self.p.search(seg):
                    outfile.write(escape(seg))
                else:
                    self.write_token(seg, ttype, outfile)

    def write_token(self, tok, ttype, outfile):
        outfile.write(self.escapeopen+'{')
        outfile.write(self.styles[ttype][1]+'{%s}' % (escape(tok)))
        outfile.write(' }'+self.escapeclose)

    def format_unencoded(self, tokensource, outfile):
        lastval = ''
        lasttype = None

        outfile.write('\start'+self.codename+'\n')

        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent

            if ttype == lasttype:
                lastval += value
            else:
                if lastval:
                    self.write(lastval, lasttype, outfile)
                lastval = value
                lasttype = ttype

        if lastval:
            self.write(lastval, lasttype, outfile)

        outfile.write('\stop'+self.codename+'\n')
