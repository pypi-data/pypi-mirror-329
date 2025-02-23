"""
    Context-free grammars. UI tools
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
import types
import pandas
pandas.set_option('display.max_colwidth', 0)

def myapply(obj, name):
    for p in name.split('.'):
        obj = getattr(obj, p)
        if type(obj) is types.MethodType:
            obj = obj()
    return obj


def maketest(g, name):
    res = myapply(g, name)
    format = lambda l : '{ '+', '.join(str(x) for x in l) + ' }'
    if type(res) in (set, list, types.GeneratorType):
        res = format(res)
    elif type(res) is dict:
        res = '\n'.join([f'{str(k)} : {format(v)}' for k, v in res.items()])
    return {'prop': name, 'valeur': res}


def results(g):
    return [maketest(g, name) for name in
            ('terminals', 'variables', 'axiom', 'rules',
             'eps_prod.vars', 'eps_prod.rules',
             'productive.vars', 'productive.rules',
             'accessible',
             'is_reduced',
             'prem', 'suiv'
             )]


def results_frame(g):
    styler = pandas.DataFrame(results(g)).style
    styler.set_properties(
        **{
            'text-align': 'left',
            'white-space': 'pre-wrap',
            'border' : '1pt solid grey',
        }
    )
    if list(map(int,pandas.__version__.split('.'))) >= [1,4] :
        styler.hide(axis='index')
    else:
        styler.hide_index()
    return styler

