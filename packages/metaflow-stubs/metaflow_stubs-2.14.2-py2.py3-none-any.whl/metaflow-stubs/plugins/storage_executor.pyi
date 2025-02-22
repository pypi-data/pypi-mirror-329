######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.2                                                                                 #
# Generated on 2025-02-21T20:07:34.999137                                                            #
######################################################################################################

from __future__ import annotations


from ..exception import MetaflowException as MetaflowException

class StorageExecutor(object, metaclass=type):
    """
    Thin wrapper around a ProcessPoolExecutor, or a ThreadPoolExecutor where
    the former may be unsafe.
    """
    def __init__(self, use_processes = False):
        ...
    def warm_up(self):
        ...
    def submit(self, *args, **kwargs):
        ...
    ...

def handle_executor_exceptions(func):
    """
    Decorator for handling errors that come from an Executor. This decorator should
    only be used on functions where executor errors are possible. I.e. the function
    uses StorageExecutor.
    """
    ...

