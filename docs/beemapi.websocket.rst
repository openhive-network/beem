beemapi\.websocket
==================

This class allows subscribe to push notifications from the Hive
node.

.. code-block:: python

    from pprint import pprint
    from beemapi.websocket import HiveWebsocket

    ws = HiveWebsocket(
        "wss://gtg.hive.house:8090",
        accounts=["test"],
        on_block=print,
    )

    ws.run_forever()


.. autoclass:: beemapi.websocket.HiveWebsocket
    :members:
    :undoc-members:
    :private-members:
    :special-members:


