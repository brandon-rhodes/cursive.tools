"""The `cursive` command-line program itself."""

from docutils.nodes import Text, GenericNodeVisitor
from docutils import core
from docutils.writers import Writer

textual_nodes = set([ 'block_quote', 'paragraph',
                      'list_item', 'term', 'definition_list_item', ])

class MyVisitor(GenericNodeVisitor):
    def __init__(self, *args, **kw):
        self.words = 0
        GenericNodeVisitor.__init__(self, *args, **kw)

    def default_visit(self, node):
        if (isinstance(node, Text)
            and (node.parent.tagname in textual_nodes)):
            self.words += len(node.astext().split())

    def default_departure(self, node):
        pass

    def astext(self):
        return '%d words\n' % self.words

class MyWriter(Writer):
    def translate(self):
        visitor = MyVisitor(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

def console_script_cursive():
    core.publish_cmdline(writer=MyWriter())
