"""
A Kivy front end component for the WAMP Votes demo application.

The Votes application collects votes for our favourite flavours of ice cream.
It is powered by a back end WAMP component that runs on the address as
defined in the start_wamp_component() function.
See
https://github.com/crossbario/crossbarexamples/tree/master/votes
on how to start up your own back end component and Crossbar router.

In this front end component, click a button with an image background to vote
for the flavour it denotes.
Reset votes to zero by clicking the bottom button.

Open up a browser window with another front end component to see the numbers
change.
"""

# copyright Roger Erens, the Apache 2.0 license applies

# Kivy's install_twisted_reactor MUST be called early on!
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from twisted.internet.defer import inlineCallbacks


class VotesWampComponent(ApplicationSession):
    """
    A WAMP application component which is run from the Kivy UI.
    """

    def onJoin(self, details):
        # print("session ready", self.config.extra)

        # get the Kivy UI component this session was started from
        ui = self.config.extra['ui']
        ui.on_session(self)

        # subscribe to WAMP PubSub events and call the Kivy UI component's
        # function when such an event is received
        self.subscribe(ui.on_vote_message, u'io.crossbar.demo.vote.onvote')
        self.subscribe(ui.on_reset_message, u'io.crossbar.demo.vote.onreset')


class VotesRoot(BoxLayout):
    """
    The Root widget, defined in conjunction with the rule in votes.kv.
    """

    votes_container = ObjectProperty(None)  # Used to refer to the widget that
                                            # holds the VotesWidgets
    votes = {}  # Since votes_container is a list, we need a dictionary for
                # bookkeeping, connecting each flavour to its VotesWidget

    def add_vote_widget(self, name):
        """
        Dynamically create and add a VoteWidget to the container in Root widget.

        Updates the list self.votes_container and the dictionary self.votes.
        """
        vote_widget = Factory.VoteWidget()
        vote_widget.name = name

        self.votes_container.add_widget(vote_widget)

        self.votes[name] = self.votes_container.children[0]

    @inlineCallbacks
    def on_session(self, session):
        """
        Called from WAMP session when attached to Crossbar router.
        """
        self.session = session

        # obtain a list of dictionaries with number of votes for each
        # subject (i.e. flavour)
        votes_results = yield self.session.call(u'io.crossbar.demo.vote.get')
        for vote in votes_results:
            self.votes[vote[u'subject']].amount = vote[u'votes']

    def send_vote(self, name):
        """
        Called from VoteWidget's top button.

        Only send the name of the flavour that gets an extra vote: the back end
        will update its number of votes and publish the updated number.
        """
        if self.session:
            self.session.call(u'io.crossbar.demo.vote.vote', name)

    def send_reset(self):
        """
        Called from VotesRoot bottom button.
        """
        if self.session:
            self.session.call(u'io.crossbar.demo.vote.reset')

    def on_vote_message(self, vote_result):
        """
        Called from VotesWampComponent when Crossbar router published vote event.
        """
        self.votes[vote_result[u'subject']].amount = vote_result[u'votes']

    def on_reset_message(self):
        """
        Called from VotesWampComponent when Crossbar router published reset event.
        """
        for vote_widget in self.votes_container.children:
            vote_widget.amount = 0


class VotesApp(App):

    def build(self):

        self.root = VotesRoot()

        flavours = [u'Banana', u'Chocolate', u'Lemon']  # If you adapt this
                                                        # list, also adapt it
                                                        # in the back end
        for flavour in flavours:
            self.root.add_vote_widget(name=flavour)

        self.start_wamp_component()

        return self.root

    def start_wamp_component(self):
        """
        Create a WAMP session and start the WAMP component
        """
        self.session = None
        
        # adapt to fit the Crossbar.io instance you're using
        url, realm = u"ws://localhost:8080/ws", u"crossbardemo"

        # Create our WAMP application component
        runner = ApplicationRunner(url=url,
                                   realm=realm,
                                   extra=dict(ui=self.root))

        # Start our WAMP application component without starting the reactor because
        # that was already started by kivy
        runner.run(VotesWampComponent, start_reactor=False)


if __name__ == '__main__':
    VotesApp().run()
