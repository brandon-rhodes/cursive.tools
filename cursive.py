"""The `cursive` command-line program itself."""

from docutils.nodes import GenericNodeVisitor
from docutils import core
from docutils.writers import Writer

textual_nodes = set([ 'block_quote', 'paragraph',
                      'list_item', 'term', 'definition_list_item', ])

class Section(object):
    """Maintains a counter of how many words are in a section."""

    def __init__(self):
        self.title = ''
        self.words = 0
        self.subsections = []

    def create_subsection(self):
        ss = Section()
        self.subsections.append(ss)
        return ss

    def add_text(self, text):
        self.words += len(text.split())

    def total(self):
        return sum([ self.words ] + [ ss.words for ss in self.subsections ])

    def report(self):
        title = self.title
        if len(title) > 58:
            title = title[:57] + '\\'
        wordstr = str(self.total())
        dots = '.' * (68 - len(title) - len(wordstr) - 7)
        return ('%s %s %s words\n' % (title, dots, wordstr) +
                ''.join( '    ' + ss.report() for ss in self.subsections ))

class MyVisitor(GenericNodeVisitor):
    def __init__(self, *args, **kw):
        self.sections = [ Section() ]
        GenericNodeVisitor.__init__(self, *args, **kw)

    def visit_title(self, node):
        self.sections[-1].title = node.astext()

    def visit_section(self, node):
        sections = self.sections
        ss = sections[0].create_subsection()
        sections.append(ss)

    def depart_section(self, node):
        self.sections.pop()

    def visit_Text(self, node):
        if node.parent.tagname in textual_nodes:
            self.sections[-1].add_text(node.astext())

    def default_visit(self, node): pass
    def default_departure(self, node): pass

    def astext(self):
        return self.sections[0].report()

class MyWriter(Writer):
    def translate(self):
        visitor = MyVisitor(self.document)
        self.document.walkabout(visitor)
        self.output = '\n' + visitor.astext() + '\n'

def console_script_cursive():
    core.publish_cmdline(writer=MyWriter())
