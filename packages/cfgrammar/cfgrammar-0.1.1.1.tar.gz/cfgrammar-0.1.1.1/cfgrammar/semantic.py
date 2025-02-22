"""
    Context-free grammars.

    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
from collections.abc import Callable, Mapping, Iterable, Set
from types import SimpleNamespace
from typing import Any

from .common import Word, BasicSemantic, Rule, Semantic, EPSILON, GRAMMAR_START, SynthesisFunction, TokenValueFunction
from itertools import chain


class ParmsList (list) :
    def __init__(self, w : Word):
        super().__init__()
        positions = dict()
        count = dict()
        for index,symbol in enumerate(w) :
            k = f'{symbol}{count.get(symbol,0)}'
            if symbol in positions or k in count :
                raise Exception(f'incompatible variable name {symbol}')
            positions[k] = index
            count[symbol] = 1 + count.get(symbol,0)
        for symbol in count :
            if count[symbol]==1 :
                positions[symbol] = positions[f'{symbol}0']
        self._word_length = len(w)
        self._positions = positions

    def __getattr__(self, attr):
        return self[self._positions[attr]]

    def __setattr__(self, attr, value):
        if attr in ('_positions','_word_length') :
            super().__setattr__(attr, value)
        else :
            self[self._positions[attr]] = value

    def append(self, __object) -> None:
        if len(self) == self._word_length :
            raise Exception('list is full')
        super().append( __object)

    def extend(self, __iterable) -> None:
        _=(* map(self.append,__iterable),)


class ParmsValues (ParmsList) :

    def __setitem__(self, key, value):
        """
            Forbidden.
            NB : to add new values, use append or extend
        """
        raise Exception('values are read-only')



class SimpleSemantic(BasicSemantic):
    """
        same semantic for any Rule
    """
    def __init__(self,
                 rule_function:SynthesisFunction,
                 start_function:SynthesisFunction = None,
                 token_function:TokenValueFunction = None):
        self._rule_f = rule_function
        self._start_f = start_function
        self._token_f = token_function


class DictSemantic(BasicSemantic):
    """
        based on dict of functions indexed by rule
    """
    @staticmethod
    def dico_split_rules(dico: Mapping[str, Any]) -> Mapping[Rule, Any]:
        from cfgrammar import GrammarBuilder
        return { rule:f
                    for line,f in dico.items()
                        for rule  in GrammarBuilder.parse_line(line)
                }

    def __init__(self,
            sem_dict: Mapping[str, Callable],
            start_function : SynthesisFunction | None = None,
            token_function  : TokenValueFunction| None = None
        ):
        sem_dict = dict(sem_dict)  # local copy
        self._start_f = start_function or sem_dict.pop('_start',None) or self._start_f
        self._token_f = token_function or sem_dict.pop('_token',None) or self._token_f
        self._sem_dict = DictSemantic.dico_split_rules(sem_dict)

    def rules(self) -> Set[Rule]:
        return self._sem_dict.keys()

    def rule_synth(self, rule : Rule) -> SynthesisFunction:
        return self._sem_dict[rule]


tex_conv = {c:rf'\{c}{{}}' for c in r'&%#$_{}^'}| {
    '~': r'\textasciitilde{}',
    '\\': r'\textbackslash{}',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
}
forest_conv = tex_conv | { c:'{'+c+'}' for c in '[],=' }
# def tex_escape(s) :
#     return ''.join(tex_conv.get(c,c) for c in s)
def forest_escape(s) :
    return ''.join(forest_conv.get(c,c) for c in s)


class LatexForestAST(Semantic) :
    """
    """
    set_style = r'''
        \forestset{
            token/.style={draw={black,dashed,thick, fill=black!10}},
            eps/.style={draw={none}},
            default preamble={for tree={font=\scriptsize,draw, thin}}
        }
    '''
    def __init__(self, preamble='', token_marker = 'token', show_epsilon = True, variable_marker ='', with_style=False, pretty_print=True ):
        self.preamble = preamble
        self.token_marker = token_marker
        self.show_epsilon = show_epsilon
        self.variable_marker = variable_marker
        self.with_style = with_style
        self.pretty_print = pretty_print
        self.epsilon_node = r'[$\varepsilon$, eps]'
        self.indent = ' '*2
        # self.nl ='\n'

    def __forest_node(self,p,run,_) -> str:
        if not p and self.show_epsilon:
            p = [self.epsilon_node]
        if p and self.pretty_print :
            children = '\n'+'\n'.join([self.indent+line for child in p for line in child.split('\n')]) + '\n'
        else :
            children = ''.join(p)
        label = forest_escape(run.var)
        return f"[{label}{children}]"
    def __forest_init(self,p,run,_) -> str:
        style = LatexForestAST.set_style if self.set_style else ''
        return rf'''
            {style}
            \begin{{forest}}
                {self.preamble}
                {p[0]}\
            \end{{forest}}
        '''
    def __forest_token(self,token : Any) -> str:
        label = forest_escape(token.type)
        return f'[{label}, {self.token_marker}]'

    def start_synth(self) -> Callable [[list[Any],SimpleNamespace,SimpleNamespace], Any]:
        return self.__forest_init
    def rule_synth(self, rule : Rule) -> Callable [[list[Any],SimpleNamespace, SimpleNamespace], Any]:
        return self.__forest_node
    def token_semantic(self) -> Callable [[Any],Any]:
        return self.__forest_token


class GraphvizAST(Semantic) :
    escape_dict = {ord(x): '\\' + x for x in r'"\{}|'}

    def __init__(self, token_display= type, with_word : bool = False, show_epsilon = True, graph_attributes=None):
        # def __init__(self, token_display: str | callable = 'type'):
        graph_attributes = graph_attributes or dict()
        self.node_count = 0
        self.show_epsilon = show_epsilon
        if token_display == 'type' :
            self._token_display = lambda tok : tok.type
        elif token_display == 'value' :
            self._token_display = lambda tok : str(tok.value)
        elif token_display == 'both' :
            self._token_display = lambda tok : f'{tok.value} {tok.type}'
        else :
            self._token_display = token_display

        self._graph_attributes = {'margin':0, 'bgcolor':'transparent'}| graph_attributes
        self._leaf_list =[]
        self._token_list =[]
        self._with_word = with_word

    def _create_id(self):
        node_id = f'node{self.node_count}'
        self.node_count += 1
        return node_id

    def _create_node(self, label, node_id=None, raw_html=False, **attributes):
        if node_id is None:
            node_id = self._create_id()
        label = f'<{label}>' if raw_html else label.translate(GraphvizAST.escape_dict)
        attr_str = ' '.join((f'{key}="{value}"' for key, value in attributes.items()))
        node_def = f'{node_id}[label="{label}",{attr_str}]'
        return (node_id, node_def)
    def _create_word_node(self, content, node_id = None, **attributes):
        if node_id is None :
            node_id = self._create_id()
        label = '|'.join(f'<{i}>{s.translate(GraphvizAST.escape_dict)}' for i, s in enumerate(content))
        attr_str = ' '.join((f'{key}="{value}"' for key,value in attributes.items()))
        node_def = f'{node_id}[label="{label}" shape="record" {attr_str}]'
        return (node_id, node_def)

    def gv_rule(self,p,run,_) :
        if not p and self.show_epsilon :
            eps_id, eps_def = self._create_node(label=EPSILON,shape='none')
            p = [(eps_id,(eps_def,),(),())]
        shape = 'box'
        node_id, node_def = self._create_node(label=run.var,shape=shape)
        edges = (f'{node_id}->{res[0]}' for res in p)
        all_nodes = chain((node_def,), chain.from_iterable(res[1] for res in p))
        all_edges = chain(edges, chain.from_iterable(res[2] for res in p))
        if len(p)>1 :
            chilren_list = ','.join(res[0] for res in p)
            constraint = (f'{{rank=same;{chilren_list}}}',)
        else :
            constraint = ()
        all_constraints = chain( constraint ,chain.from_iterable(res[3] for res in p))

        return (node_id, all_nodes, all_edges, all_constraints)

    def gv_init(self,p,run,_):
        attr_str = ';'.join((f'{key}="{value}"' for key, value in self._graph_attributes.items()))
        res = ['digraph arbre {',' node [width=0.1,height=0.05]',' edge [arrowhead="none"]', attr_str]
        res.extend(chain(p[0][1],p[0][2],p[0][3]))
        if self._with_word :
            word_id, word_def = self._create_word_node(content = (str(t.value) for t in self._token_list))
            res += [word_def,'edge [minlen=3,style=dashed,arrowhead=onormal,arrowsize=0.7]']
            res.extend(f'{leaf_id}->{word_id}:{index}:n  ' for index,leaf_id in enumerate(self._leaf_list) )
        res += ['}']
        return '\n'.join(res)

    def gv_token(self, token : Any) :
        label = self._token_display(token)
        node_id, node_def = self._create_node(label=label,shape='box',style='dashed,rounded,filled')
        self._leaf_list.append(node_id)
        self._token_list.append(token)
        return (node_id, (node_def,), (),())

    def start_synth(self) -> Callable [[list[Any],SimpleNamespace,SimpleNamespace], Any]:
        return self.gv_init

    def rule_synth(self, rule : Rule) -> Callable [[list[Any],SimpleNamespace, SimpleNamespace], Any]:
        return self.gv_rule

    def token_semantic(self) -> Callable [[Any],Any]:
        return self.gv_token




# class TikzSemanticN(Semantic) :
#     components = {
#         'forest' : {
#             'empty_node' : r'[$\varepsilon$]',
#             'root_func' : str,
#             'init_func' : lambda content : rf'\begin{{forest}} {content} \end{{forest}}'
#         },
#         'tikz-qtree': {
#             'empty_node' : (r'\node[eps]{$\varepsilon$};',) ,
#             'root_func' :  lambda v : rf'.\node[var]{{{v}}}',
#             'init_func': lambda content: rf'\Tree {content}'
#         }
#     }
#     def tikz_node(self,run,_) :
#         compo = self.__class__.components[self._mode]
#         children_trad = ' '.join(run.res) if run.res else compo['empty_node']
#         root_trad = compo['root_func'](run.var)
#         return  rf"[{root_trad} {children_trad}]"
#
#     def tikz_init(self,run,_):
#         compo = self.__class__.components[self._mode]
#         return compo['init_func'](run.res[0])
#
#     def rule_synth(self, rule=None):
#         if rule is None :
#             return SimpleNamespace(synth=self.tikz_init)
#         else :
#             return SimpleNamespace(synth=self.tikz_node)
#
#     def token_semantic(self):
#         return lambda v : f'[{v}]'
#
#     def __init__(self, mode):
#         assert mode in ['tikz-qtree','forest']
#         self._mode = mode
#

#
class RuleRun():
    def __init__(self, semantic : Semantic, rule : Rule ):
        self.namespace = SimpleNamespace()
        self._p = ParmsValues(rule.right)
        self.run = SimpleNamespace(len=len(rule.right), var=rule.left, rule = rule )
        if rule.left == GRAMMAR_START :          # start context
            self.synth_func = semantic.start_synth()
        else :
            self.synth_func = semantic.rule_synth(rule)
        if self.run.len == 0 : # epsilon rule
            self._resolve()

    def __str__(self):
        return f'RuleRun : {self.run} {self.synth_func} {self._p}'

    def _resolve(self):
        if not self.is_complete() :
            raise Exception('Run is not complete')
        self.synthetised = self.synth_func(self._p,self.run,self.namespace)

    def is_closed(self):
        return getattr(self,'synthetised') is  not None

    def is_complete(self):
        return self.run.len == len(self._p)

    def add_result(self,value):
        assert not self.is_complete()
        self._p.append(value)
        if self.is_complete() :
            self._resolve()

    def add_results(self, * values):
        for v in values :
            self.add_result(v)

