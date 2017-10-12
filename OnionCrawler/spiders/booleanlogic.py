import re

   
class Node(object):
    def __init__(self, text=''):
        self.text = text
        self.children = []

    def __repr__(self):
        if not self.children:
            return self.text
        else:
            return '%s(%s)' % (
                self.text,
                ' '.join(str(node) for node in self.children))

    def code(self):
        if self.text.startswith('-'):
            return lambda s: self.text[1:] not in s
        else:
            return lambda s: self.text in s

class AndNode(Node):
    def code(self):
        def fn(s):
            return all([
                child.code()(s)
                for child in self.children])
        return fn

class OrNode(Node):
    def code(self):
        def fn(s):
            return any([
                child.code()(s)
                for child in self.children])
        return fn
    
class SearchTerm:
    
    global phrase
      
    def __init__(self, phrase):
        self.phrase = phrase
    #phrase = CharField()
  

    def __unicode__(self):
        return self.phrase
    
    def parse(self):
        node_map = {'AND': AndNode, 'OR': OrNode}
    
        # The default conjunction is AND, so if the phrase simply consists of one or more words, "and"- them together.
        stack = [AndNode('AND')]
    
        for token in re.split('(\".+?\"|\(|\s+|\))', self.phrase):
            # Ignore any empty tokens.
            token = token.strip()
            if not token:
                continue
    
            if token == '(':
                stack.append(Node())
            elif token == ')':
                node = stack.pop()
                if len(stack) == 0:
                    raise ValueError('Error: unbalanced parentheses!')
                stack[-1].children.append(node)
            elif token in ('AND', 'OR'):
                # In the event the top node uses the same conjunction, just
                # continue on. Otherwise push a new node onto the stack.
                if stack[-1].text != token:
                    top = stack.pop()
                    node = node_map[token](token)
                    if top.text == '' and len(top.children) == 1:
                        node.children.extend(top.children)
                    else:
                        node.children.append(top)
                    stack.append(node)
            else:
                node = Node(token.strip('"'))
                stack[-1].children.append(node)
    
        if len(stack) != 1:
            raise ValueError('Error: unbalanced parentheses!')
    
        return stack[0]
    
    def test(self, s):
        # Parse the search phrase into a `Node` tree, then generate a function corresponding to the query conditions. 
        # Finally, apply that function to the incoming string, `s`.
        return self.parse().code()(s)
