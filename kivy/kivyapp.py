import os
from pprint import pprint

pprint(dict(os.environ))


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

# Kivy's install_twisted_rector MUST be called early on!
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class MyComponent(ApplicationSession):

    """
    A simple WAMP app component run from the Kivy UI.
    """

    def onJoin(self, details):
        print("session ready", self.config.extra)

        # get the Kivy UI component this session was started from
        ui = self.config.extra['ui']
        ui.on_session(self)

        # subscribe to WAMP PubSub event and call the Kivy UI component when events are received
        self.subscribe(ui.print_message, u"com.example.topic1")


class CrossbarKivyApp(App):

    """
    A simple kivy App, with a textbox to enter messages, and
    a large label to display all the messages received from Crossbar.io.
    """

    def build(self):
        """
        Entry point of Kivy UI component.
        """
        # WAMP session
        self.session = None

        # run our WAMP application component
        runner = ApplicationRunner(url = u"ws://localhost:8080/ws", realm = u"realm1", extra = dict(ui=self))
        runner.run(MyComponent, start_reactor=False)

        # setup the Kivy UI
        root = self.setup_gui()
        return root

    def setup_gui(self):
        """
        Setup Kivy UI.
        """
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def on_session(self, session):
        """
        Called from WAMP session when attached to router.
        """
        self.print_message("WAMP session connected!")
        self.session = session

    def send_message(self, *args):
        """
        Called from UI when user has entered text and pressed RETURN.
        """
        msg = self.textbox.text
        if msg and self.session:
            self.session.publish(u"com.example.kivy", str(self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        """
        Called from WAMP app component when message was received in a PubSub event.
        """
        self.label.text += msg + "\n"


if __name__ == '__main__':
    CrossbarKivyApp().run()
