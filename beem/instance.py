# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
import beem as hv


class SharedInstance(object):
    """Singelton for the Hive Instance"""
    instance = None
    config = {}


def shared_hive_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        hive instance that can be reused by multiple classes.

        .. code-block:: python

            from beem.account import Account
            from beem.instance import shared_hive_instance

            account = Account("test")
            # is equivalent with
            account = Account("test", hive_instance=shared_hive_instance())

    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = hv.Hive(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_hive_instance(hive_instance):
    """ This method allows us to override default hive instance for all users of
        ``SharedInstance.instance``.

        :param Hive hive_instance: Hive instance
    """
    clear_cache()
    SharedInstance.instance = hive_instance


def clear_cache():
    """ Clear Caches
    """
    from .blockchainobject import BlockchainObject
    BlockchainObject.clear_cache()


def set_shared_config(config):
    """ This allows to set a config that will be used when calling
        ``shared_hive_instance`` and allows to define the configuration
        without requiring to actually create an instance
    """
    if not isinstance(config, dict):
        raise AssertionError()
    SharedInstance.config.update(config)
    # if one is already set, delete
    if SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = None
