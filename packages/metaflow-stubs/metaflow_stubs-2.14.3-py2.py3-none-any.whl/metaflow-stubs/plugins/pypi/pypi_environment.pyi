######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.3                                                                                 #
# Generated on 2025-02-22T04:36:00.863291                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

