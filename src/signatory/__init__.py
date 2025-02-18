# Copyright 2019 Patrick Kidger. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================
"""Signatory: Differentiable computations of the signature and logsignature transforms, on both CPU and GPU.

Project homepage: https://github.com/patrick-kidger/signatory
Documentation: https://signatory.readthedocs.io
"""

import platform

if platform.system() == "Darwin":
    # On MacOS, libomp is tricky to find because the operating system doesn't
    # provide it. Torch packages libomp on MacOs, so we just need to make sure
    # the signatory library can find it.
    from ctypes import CDLL as _CDLL
    from importlib import metadata as _ilm

    dist = _ilm.distribution("torch")
    for so in (f for f in dist.files if f.match("libomp.*")):
        _CDLL(so.locate().resolve())


import torch  # must be imported before anything from signatory

try:
    from . import impl
except ImportError as e:
    if "specified procedure could not be found" in str(e):
        raise ImportError(
            "Caught ImportError:\n```\n{}\n```\nThis can probably be fixed by updating your version of "
            "Python, e.g. from 3.6.6 to 3.6.9. See the FAQ in the documentation.".format(
                str(e)
            )
        )
    elif "Symbol not found" in str(e):
        raise ImportError(
            "Caught Import Error:\n```\n{}\n```\nThis can probably be fixed by changing your version of "
            "PyTorch. See the FAQ in the documentation.".format(str(e))
        )
    else:
        raise


from . import \
    unstable  # make it available as an attribute here, but don't import any unstable objects themselves
from .augment import Augment
from .deprecated import max_parallelism
from .logsignature_module import Logsignature  # alias for LogSignature
from .logsignature_module import (LogSignature, SignatureToLogSignature,
                                  SignatureToLogsignature, logsignature,
                                  logsignature_channels,
                                  signature_to_logsignature)
from .path import Path
from .signature_inversion_module import invert_signature
from .signature_module import (Signature, extract_signature_term,
                               multi_signature_combine, signature,
                               signature_channels, signature_combine)
from .utility import all_words, lyndon_brackets, lyndon_words

__version__ = "1.2.7"

del torch
