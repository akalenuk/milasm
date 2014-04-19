import sys

def dig( line, level = 0, ls = []):
        opening = line.find('((')
        closing = line.find('))')
        if opening == -1 and closing == -1:
                return ls + [(level, line)]
        elif opening == -1:
                return dig(line[closing+2:], level-1, ls + [(level, line[:closing])])
        elif closing == -1:
                raise Exception("Unmatched closing )) in " + line)
        elif opening < closing:
                return dig(line[opening+2:], level+1, ls + [(level, line[:opening])])
        elif closing < opening:
                return dig(line[closing+2:], level-1, ls + [(level, line[:closing])])
                
def datum_to_list2( text ):
        return text.split(' ')
                
def datum_to_list( text ):
        nq = text.split('\"')
        ret = []
        for i, el in enumerate(nq):
                if i % 2 == 0:
                        ret += el.split(' ')
                else:
                        ret += ['\"' + el + '\"']
        return ret
        

def entree( ls, cur_level = 0 ):
        tree = []
        temp_ls = []
        for (level, datum) in ls:
                if level == cur_level:
                        tree = (tree + [entree(temp_ls, level+1)]) if temp_ls != [] else tree
                        tree += datum_to_list( datum )
                        temp_ls = []
                else:
                        for datum_element in datum_to_list( datum ):
                                temp_ls += [(level, datum_element)]
        return tree

        
def read_macroses( text ):
        macroses = []
        imports = [macros.split('<<')[1] for macros in  text.split('>>')[:-1]]
        for imp in imports:
                f = open(imp)
                macroses += read_macroses( ''.join( f.readlines() ) )
                f.close()
        
        macroses_raw = [macros.split('[[')[1] for macros in  text.split(']]')[:-1]]
        defn_meanings = [tuple(macros.split('->')) for macros in macroses_raw]
        macroses += [(defn.strip().split(' '), meaning.strip()) for (defn, meaning) in defn_meanings]
        return macroses


def macroid():
        mid = 0
        while True:
                mid += 1
                yield str(mid)
                
MID = macroid()
        
def sanitize_tree( tree ):
        if tree == []:
                return []
        if tree[0] == '' or tree[0] == '\n':
                return sanitize_tree( tree[1:] )
        if tree[0] == '.line':
                return sanitize_tree( tree[2:] )
        return [tree[0]] + sanitize_tree( tree[1:] )

def eval_macros( tree_or_leaf, macroses ):
        global MID
        mid = MID.next()

        if not isinstance(tree_or_leaf, list):
                leaf = tree_or_leaf
                return leaf
        tree = sanitize_tree( tree_or_leaf )
        for macros in macroses:
                (macro_def, macro_meaning) = macros
                if len(macro_def) != len(tree):
                        continue
                symbols = []
                right_macros = True
                for (m, t) in zip(macro_def, tree):                     
                        if m[0] == '$':
                                symbols += [(m, t)]
                        elif m != t:
                                right_macros = False
                                break
                if right_macros:
                        ret = macro_meaning.replace( '$#', mid )
                        for (m, t) in symbols:
                                ret = ret.replace(m, eval_macros(t, macroses))
                        return ret
        return ' '.join([eval_macros( subtree, macroses ) for subtree in tree_or_leaf])
                        
                
def eval_macroses( tree, macroses ):
        evaled = []
        for elem in tree:
                if isinstance(elem, list):
                        evaled += [eval_macros( elem, macroses )]
                else:
                        evaled += [ elem ]
        return evaled

        
def prepare_input( text ):
        text = text.replace('\t', ' ')
        while text.find('  ') != -1:
                text = text.replace('  ', ' ')

        lines = text.split('\n')
        numbered_lines = []
        for (i, line) in enumerate(lines, 1):
                line = line.split('//')[0].strip()
                if line == '' or line[0] == '{' or line[0] == '}' or line[0] == '.' or line[0] == '['  or line[0] == '<':
                        numbered_lines += [line]
                else:
                        numbered_lines += ['.line ' + str(i) + ' ' + line ]
        
        return ' \n '.join( numbered_lines )


def sanitize_definitions( text ):
        pairs = text.split('[[')
        return pairs[0] + ''.join([pair.split(']]')[1] for pair in pairs[1:]])
        
def sanitize_imports( text ):
        pairs = text.split('<<')
        return pairs[0] + ''.join([pair.split('>>')[1] for pair in pairs[1:]])

def sanitize( text ):
        return sanitize_definitions( sanitize_imports( text ) )
        
if len(sys.argv) == 1:
        print "File name, please."
        exit(1)

        
f = open(sys.argv[1])   
text = ''.join(f.readlines())
text = prepare_input( text )
f.close()

the_macroses = read_macroses( text )

while text.find('((') != -1:
        the_tree = entree(dig( text ))
        text = sanitize(' '.join( eval_macroses( the_tree, the_macroses ) ) )

print text
