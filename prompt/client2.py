#from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
#
#html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
#text = prompt('Enter HTML: ', completer=html_completer)
#print('You said: %s' % text)


from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        print(document)
        print(complete_event)
        yield Completion('completion', start_position=0)

class MyCompleter(WordCompleter):

    def get_completions(self, document, complete_event):
        print(document)
        print(complete_event)
        res = WordCompleter.get_completions(self, document, complete_event)
        print(res)
        return res

#text = prompt('> ', completer=MyCustomCompleter())
PROMPT = '\\u@\\h:\\d> '

html_completer = MyCompleter(['<html>', '<body>', '<head>', '<title>'])
text = prompt(PROMPT, completer=html_completer)
print('You said: %s' % text)
