# -*- coding: utf-8 -*-
import blurtpy


class SharedInstance(object):
    """Singelton for the Blurt Instance"""
    instance = None
    config = {}


def shared_blockchain_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        blurt instance that can be reused by multiple classes.

        .. code-block:: python

            from blurtpy.account import Account
            from blurtpy.instance import shared_blurt_instance

            account = Account("test")
            # is equivalent with
            account = Account("test", blockchain_instance=shared_blurt_instance())

    """
    if not SharedInstance.instance:
        clear_cache()
        from blurtpy.storage import get_default_config_store
        default_chain = get_default_config_store()["default_chain"]
        if default_chain == "blurt":
            SharedInstance.instance = blurtpy.Blurt(**SharedInstance.config)
        else:
            SharedInstance.instance = blurtpy.Blurt(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_blockchain_instance(blockchain_instance):
    """ This method allows us to override default blurt instance for all users of
        ``SharedInstance.instance``.

        :param Blurt blockchain_instance: Blurt instance
    """
    clear_cache()
    SharedInstance.instance = blockchain_instance


def shared_blurt_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        blurt instance that can be reused by multiple classes.

        .. code-block:: python

            from blurtpy.account import Account
            from blurtpy.instance import shared_blurt_instance

            account = Account("test")
            # is equivalent with
            account = Account("test", blockchain_instance=shared_blurt_instance())

    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = blurtpy.Blurt(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_blurt_instance(blurt_instance):
    """ This method allows us to override default blurt instance for all users of
        ``SharedInstance.instance``.

        :param Blurt blurt_instance: Blurt instance
    """
    clear_cache()
    SharedInstance.instance = blurt_instance


def shared_blurt_instance():
    """ This method will initialize ``SharedInstance.instance`` and return it.
        The purpose of this method is to have offer single default
        blurt instance that can be reused by multiple classes.

        .. code-block:: python

            from blurtpy.account import Account
            from blurtpy.instance import shared_blurt_instance

            account = Account("test")
            # is equivalent with
            account = Account("test", blockchain_instance=shared_blurt_instance())

    """
    if not SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = blurtpy.Blurt(**SharedInstance.config)
    return SharedInstance.instance


def set_shared_blurt_instance(blurt_instance):
    """ This method allows us to override default blurt instance for all users of
        ``SharedInstance.instance``.

        :param Blurt blurt_instance: Blurt instance
    """
    clear_cache()
    SharedInstance.instance = blurt_instance


def clear_cache():
    """ Clear Caches
    """
    from .blockchainobject import BlockchainObject
    BlockchainObject.clear_cache()


def set_shared_config(config):
    """ This allows to set a config that will be used when calling
        ``shared_blurt_instance`` and allows to define the configuration
        without requiring to actually create an instance
    """
    if not isinstance(config, dict):
        raise AssertionError()
    SharedInstance.config.update(config)
    # if one is already set, delete
    if SharedInstance.instance:
        clear_cache()
        SharedInstance.instance = None
