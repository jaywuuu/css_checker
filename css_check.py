import tinycss

class CSSBlock:
    def __init__(self, selectors, declarations):
        self.selectors = selectors
        self.declarations = declarations
        self.selector_str = selector_to_str(selectors)
        self.declarations_str = declarations_to_str(declarations)

    def compare_to(self, that):
        if len(self.declarations) != len(that.declarations):
            return False

        if len(self.selectors) != len(that.selectors):
            return False

        if self.selector_str != that.selector_str:
            return False

        return True


def selector_to_str(selectors):
    str_list = []
    string = ''
    for t in selectors:
        if t.type == 'S':
            continue

        if t.as_css() == ',':
            string = string.rstrip(' ')
            str_list.append(string)
            string = ''
        else:
            if t.as_css() == '.':
                string = string + t.as_css()
            else:
                string = string + t.as_css() + ' '

    if len(string) > 0:
        string = string.rstrip(' ')
        str_list.append(string)

    str_list.sort()
    retval = ''
    for s in str_list:
        retval = retval + s + ', '

    retval = retval.rstrip(', ')

    return retval


def declarations_to_str(declarations):
    return ''

# return a list of css block objects
def process_css_file(file_path):
    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file(file_path)
    css_blocks = []
    for rule in stylesheet.rules:
        css_block = CSSBlock(rule.selector, rule.declarations)
        css_blocks.append(css_block)

    return css_blocks


# Returns a dictionary of sets of the same css blocks and their line numbers.
def css_dup_check(filepath):
    blocks = process_css_file(filepath)
    dups = {}
    for b in blocks:
        print("==================================================")
        print('Checking:', b.selector_str)
        if b.selector_str in dups.keys():
            print('Duplicate found on line:', b.selectors.line, 'with line:', dups[b.selector_str][0].selectors.line)
            dups[b.selector_str].append(b)
        else:
            dups[b.selector_str] = [b]

    return dups

