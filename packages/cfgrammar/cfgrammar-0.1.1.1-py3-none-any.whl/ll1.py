"""
    Context-free grammars. LL(1) parsing tools
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
import itertools

from types import MappingProxyType
from collections import defaultdict
from collections.abc import Iterable, Iterator, Mapping

from .semantic import RuleRun
from .common import EOD, GRAMMAR_START, Symbol, Word, ConflictError, ParseError, Parser, Rule, Semantic, LLMethod, Token
from .grammar import GrammarBase

class LL1Table:
    """
        Table LL(1) : Variable, Terminal -> Rule

        private property :
         __table :  dictionary :
                key : pair (variable, terminal)
                value : word (right part of a rule)

            No default value : raise exception if (variable, terminal) cell is empty
            Use for instance table.get( key, None ) to get None default value
    """
    Key = tuple[Symbol, Symbol]
    Conflict = tuple[Word,str]
    @property
    def table(self) -> Mapping[Key, Word]:
        """
            dictionary :
                key : pair (variable, terminal)
                value : word (right part of a rule)
            read-only proxy of self.__table
        """
        return MappingProxyType(self.__table)

    @property
    def grammar(self) -> GrammarBase:
        """
            target grammar
        """
        return self.__grammar

    @property
    def conflicts(self) -> Mapping[Key, Iterable[Conflict]]:
        return MappingProxyType(self.__conflicts)

    def conflicts_str(self) -> str:
        return '\n'.join(
            f'{k} : {",".join(f"{w} {t}" for w,t in l)}'
            for k,l in self.conflicts.items()
        )

    def __init__(self, g: GrammarBase, raise_exception: bool = True):
        """
            g: Grammar
        """
        self.__grammar: GrammarBase = g
        self.__conflicts = defaultdict[LL1Table.Key,set[LL1Table.Conflict]](set)
        table = dict[LL1Table.Key,Word]()  # table LL(1). clé : (variable, lettre terminale)
        for r in g.rules:
            for x in g.prem[r]:
                if (r.left, x) not in table:
                    table[(r.left, x)] = r.right
                elif raise_exception:
                    raise ConflictError(f'conflit phase Premiers, case [{r.left}, {x}] : {r.right} vs {table[(r.left, x)]}')
                else:
                    self.__conflicts[(r.left, x)].add((r.right, 'first'))
        for r in g.eps_prod.rules:
            for x in g.suiv[r.left]:
                if (r.left, x) not in table:
                    table[(r.left, x)] = r.right
                elif raise_exception:
                    raise ConflictError(f'conflit phase Suivants, case [{r.left}, {x}] : {r.right} vs {table[(r.left, x)]}')
                else:
                    self.__conflicts[(r.left, x)].add((r.right, 'follow'))

        self.__table = table

    def get(self, var:Symbol, term:Symbol) -> Word | None:
        """
            get cell content for key (var,term)
            var : variable symbol
            term : terminal symbol

            Returns Word or None
        """
        return self.__table.get((var,term),None)

    def get_as_rule(self, var:Symbol, term:Symbol) -> Rule | None:
        """
            get cell content for key (var,term)
            var : variable symbol
            term : terminal symbol

            Returns Rule or None
        """
        word = self.get(var,term)
        return Rule(Symbol(var), word) if word is not None else None

    def parser(self, default_semantic = None) -> Parser:
        return LL1Parser(self, default_semantic)

    def to_pandas(self, latex: bool = False) -> "pandas.DataFrame":
        """
            Returns table as pandas.DataFrame
        """
        import pandas
        lines = list(self.__grammar.terminals) + [EOD]
        f = pandas.DataFrame(dict.fromkeys(self.__grammar.get_vars(), [""] * len(lines)), index=lines)
        for (v, x), w in self.table.items():
            if latex :
                f.loc[x,v] = Rule(v, w).to_latex()
            else :
                f.loc[x,v] = str(Rule(v, w))
        if latex :
            f.index = f.index.map(Symbol.to_latex)
            f.columns = f.columns.map(Symbol.to_latex)
        return f

    def to_latex(self) -> str:
        """
            Returns table as latex table
            (use pandas DataFrame)
        """
        f = self.to_pandas(latex=True)
        styler = f.style
        styler.set_table_styles([
            {'selector': 'midrule,toprule,bottomrule', 'props': ':hline; :hline;'},
        ], overwrite=False)
        # styler.set_table_styles({
        #     'A': [{'selector': '',
        #
        #            'props': [('color', 'red')]}],
        #
        #     'B': [{'selector': 'td',
        #
        #            'props': 'color: blue;'}]
        # }, axis=1,overwrite=False)
        styler.set_table_styles(
            {
            # '\#':[{'selector':'td', 'props':'cellcolor:[HTML]{FFFF00}; color:{red}; itshape:; bfseries:;'}]
            'a':[{'selector':'', 'props':'color: #f0e;'}]
            },
            axis=1
        )
        return styler.to_latex(column_format='|l|' + 'c|' * len(f.columns), convert_css=True)

    def to_html(self) -> str:
        """
            Returns table as HTML table
            (use pandas DataFrame)
        """
        styler = self.to_pandas().style
        td = {'selector':'td','props': 'border : solid 0.8pt; text-align:left'}
        th = {'selector':'th','props': 'text-align:center'}
        return styler.set_table_styles([td,th]).to_html()

    def _repr_html_(self) -> str:
        return self.to_html()

    def to_markdown(self) -> str:
        """
            Returns table as markdown table
            (use pandas DataFrame)
        """
        return self.to_pandas().to_markdown()


class LL1Parser(Parser):
    def __init__(self, table: LL1Table , default_semantic=None):
        super().__init__(default_semantic)
        self.__table = table

    @property
    def method(self):
        return LLMethod.LL1

    @property
    def table(self) -> LL1Table:
        return self.__table

    @property
    def grammar(self) -> GrammarBase:
        return self.table.grammar

    def parse_tokens_impl(self, tokens:Iterable[Token], semantic : Semantic, verbose=False):
        """
            tokens : Iterable[Token] (without End Of Data token)
            Token :  any class with 'type' and 'value' attributes
        """
        table = self.__table
        grammar = table.grammar
        runs = RunManager(semantic)
        token_input:Iterator[Token] = itertools.chain(tokens, [Parser.BasicToken(type=EOD,value=None)])
        current = next(token_input)
        stack:[Symbol,...] = [grammar.axiom]
        verbose and print(f'stack:{stack}, current: {current.type}')
        while stack :
            symbol = stack.pop()
            verbose and print(f'stack:{stack}, symbol:{symbol}, current: {current.type}')
            if grammar.is_var(symbol) :
                rule = table.get_as_rule(symbol,Symbol(current.type))
                if rule is not None :
                    verbose and print(f"apply {rule}")
                    stack.extend( reversed (rule.right) )
                    semantic and runs.create_run(rule)    # ==> semantic
                    verbose and print(f'stack:{stack}, current: {current.type}')
                else :
                    raise ParseError('mot incorrect')
            elif symbol == current.type:
                verbose and print("shift")
                semantic and runs.add_token_result(current) # ==> semantic
                current = next(token_input)
            else:
                raise ParseError(f'mot incorrect, waiting {symbol}')
        if current.type != EOD:
            raise ParseError('mot incorrect waiting EOD')
        if semantic :
            return runs.synthetised  # ==> semantic
        else :
            return True


class RunManager:
    def __init__(self, semantic : Semantic):
        self._stack = [RuleRun(semantic = semantic, rule = Rule(GRAMMAR_START,Word(Symbol('_'))))]
        self._token_semantic = semantic.token_semantic()
        self._semantic = semantic

    def create_run(self, rule:Rule):
        created = RuleRun(rule=rule, semantic=self._semantic)
        if created.is_complete() :
            self.add_result(created.synthetised)
        else :
            # current = self._stack[-1]
            # index = len(current._p)
            # if getattr(current,'down',False) and index in current.down :
            #      created.run.inherited = current.down[index](current.run,current.namespace)
            self._stack.append(created)

    def add_token_result(self,token:Token):
        self.add_result(self._token_semantic(token))

    def add_result(self, value):
        self._stack[-1].add_result(value)
        while len(self._stack)>=2 and self._stack[-1].is_complete() :
            run = self._stack.pop()
            self._stack[-1].add_result(run.synthetised)

    @property
    def synthetised(self):
        if len(self._stack) != 1 :
            raise Exception(f'erreur {len(self._stack)} runs')
        return self._stack[0].synthetised




