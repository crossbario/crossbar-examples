from prompt_toolkit import prompt_async
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt

import asyncio
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

# http://python-prompt-toolkit.readthedocs.io/en/stable/pages/building_prompts.html#input-validation
class NumberValidator(Validator):

    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input contains non-numeric characters',
                                  cursor_position=i)


class MyComponent(ApplicationSession):

    async def onJoin(self, details):
        print('Connected!')
        x = await prompt_async('x: ', validator=NumberValidator(), patch_stdout=True)
        x = int(x)
        y = 23
        res = await self.call(u'com.example.add2', x, y)
        print("RPC succeded: {} + {} = {}".format(x, y, res))
        self.leave()

    def onDisconnect(self):
        loop = asyncio.get_event_loop()
        loop.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(u"ws://localhost:8080/ws", u"realm1")
    runner.run(MyComponent)
