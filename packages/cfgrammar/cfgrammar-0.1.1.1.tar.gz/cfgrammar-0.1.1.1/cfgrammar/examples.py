"""
    Context-free grammars.
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
gds_def = '''
E -> i = E | E + E | ( E ) | i
'''

g1_def = '''
        S -> A B | D a
        A -> a A b|
        B -> b B |
        D-> d D|e
    '''

g9_def = '''
S-> A a | b A c | d c | b d a
A -> d
'''
g91_def = '''
S-> E + E | E * E | a
'''
g92_def = '''
S-> L | E
L -> id : S | case C : S
E -> C ;
C -> id
'''

g21_def = '''
        E -> E + T | T
        T -> T * F | F
        F -> * F  | ( E ) | i
    '''

g22_def = '''
        E -> E + T | T
        T -> T * F | F
        F -> F *  | ( E ) | i
    '''

g3_def = '''
        E -> T G
        G -> + T G |
        T -> F H
        H -> * F H |
        F -> ( E ) | x | W
        W -> a X Z
        X -> a W
        Z -> a
    '''

g3b_def = '''
        E -> T E'
        E' -> + T E' |
        T -> F T'
        T' -> * F T' |
        F -> ( E ) | x | W
        W -> a X Z
        X -> a W
        Z -> a
    '''

g4_def = '''
        X -> Y a
        Y -> b Y
    '''

g5_def = '''
        REL -> PRIM S
        S -> ⋈ REL | 
        PRIM -> id | σ COND ( REL )
        COND -> ( id = id L )
        L -> id = id L |
    '''

g6_def = '''
        S-> A c
        A-> A a A b | d
    '''

g7_def = '''
        S -> G = D | D
        G -> * D | i
        D -> G
    '''

g8_def = '''
        S-> A d
        A-> A a A b | d
    '''

g11_def = '''
        A-> a A b | c
    '''
g12_def = '''
        A-> a A b | 
    '''
g13_def = '''
        A-> a A b | a b
    '''

gdsbis_def = '''
        X -> a Y b | i X e X | s
        Y -> Y b X | X
    '''

geq0_def = '''
        S -> a S b S | b S a S |
'''

geq_def = '''
        S -> a T b S | b U a S |
        T -> a T b T |
        U -> b U a U |
'''

gcours_def = '''
X → a Y U | c Z
Y → T a | Z e | b 
Z → Z d | c
T → X e 
U → Y b
'''
