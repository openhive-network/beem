# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from events import Events
from beemapi.websocket import HiveWebsocket
from beem.instance import shared_hive_instance
from beem.blockchain import Blockchain
from beem.price import Order, FilledOrder
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class Notify(Events):
    """ Notifications on Blockchain events.

        This modules allows yout to be notified of events taking place on the
        blockchain.

        :param fnt on_block: Callback that will be called for each block received
        :param Hive hive_instance: Hive instance

        **Example**

        .. code-block:: python

            from pprint import pprint
            from beem.notify import Notify

            notify = Notify(
                on_block=print,
            )
            notify.listen()

    """

    __events__ = [
        'on_block',
    ]

    def __init__(
        self,
        # accounts=[],
        on_block=None,
        only_block_id=False,
        hive_instance=None,
        keep_alive=25
    ):
        # Events
        Events.__init__(self)
        self.events = Events()

        # Hive instance
        self.hive = hive_instance or shared_hive_instance()

        # Callbacks
        if on_block:
            self.on_block += on_block

        # Open the websocket
        self.websocket = HiveWebsocket(
            urls=self.hive.rpc.nodes,
            user=self.hive.rpc.user,
            password=self.hive.rpc.password,
            only_block_id=only_block_id,
            on_block=self.process_block,
            keep_alive=keep_alive
        )

    def reset_subscriptions(self, accounts=[]):
        """Change the subscriptions of a running Notify instance
        """
        self.websocket.reset_subscriptions(accounts)

    def close(self):
        """Cleanly close the Notify instance
        """
        self.websocket.close()

    def process_block(self, message):
        self.on_block(message)

    def listen(self):
        """ This call initiates the listening/notification process. It
            behaves similar to ``run_forever()``.
        """
        self.websocket.run_forever()
