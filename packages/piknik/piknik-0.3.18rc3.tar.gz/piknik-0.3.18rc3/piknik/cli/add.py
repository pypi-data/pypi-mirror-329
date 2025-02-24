# standard imports
import sys

# local imports
from piknik import Issue

ctx = None


def subparser(argp):
    argp.add_argument('title', type=str, nargs='*', help='issue title')
    return argp


def assembler(o, arg):
    o.title = arg.title


def main():
    title = ''
    for s in ctx.title:
        if s == ' ':
            continue
        if title != '':
            title += ' '
        title += s
    if ctx.alias == None:
        issue_id = ctx.basket.id_generator()
        o = Issue(title, issue_id=issue_id, alias=issue_id[:5])
    else:
        o = Issue(title, alias=ctx.alias)
    v = ctx.basket.add(o)
    sys.stdout.write(v + '\n')
