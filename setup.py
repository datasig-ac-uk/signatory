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
"""setup.py - hopefully you know what this does without me telling you..."""

import setuptools
import sys
import platform
import ctypes


from importlib import metadata as ilm
from pathlib import Path



# The RPATH entries on Linux are set wrong in Torch, so we do some hacks
# using the metadata to find and load all the shared libraries, priming
# the ld cache with all the libraries that might be needed.
if platform.system() == "Linux" and platform.machine() == "x86_64":

    torch_dist = ilm.distribution("torch")

    requires = [
        line.split(';')[0].split()[0].strip()
        for line in torch_dist.requires
        if line.endswith("platform_system == \"Linux\" and platform_machine == \"x86_64\"")
    ]

    for req in requires:
        dist = ilm.distribution(req)
        for so in (f for f in dist.files if f.match("*.so*")):
            ctypes.CDLL(so.locate().resolve())


try:
    import torch.utils.cpp_extension as cpp
except ImportError as e:
    raise ImportError("PyTorch is not installed, and must be installed prior to installing Signatory.") from e


extra_compile_args = []

# fvisibility flag because of https://pybind11.readthedocs.io/en/stable/faq.html#someclass-declared-with-greater-visibility-than-the-type-of-its-field-someclass-member-wattributes
if not sys.platform.startswith('win'):  # linux or mac
    extra_compile_args.append('-fvisibility=hidden')

if sys.platform.startswith('win'):  # windows
    extra_compile_args.append('/openmp')
else:  # linux or mac
    extra_compile_args.append('-fopenmp')
    extra_compile_args.append('-D_GLIBCXX_USE_CXX11_ABI=0')
    extra_compile_args.extend(["-fvisibility-inlines-hidden", "-fvisibility=hidden"])

ext_modules = [cpp.CppExtension(name='signatory._impl',
                                sources=['src/logsignature.cpp',
                                         'src/lyndon.cpp',
                                         'src/misc.cpp',
                                         'src/pytorchbind.cpp',
                                         'src/signature.cpp',
                                         'src/tensor_algebra_ops.cpp'],
                                depends=['src/logsignature.hpp',
                                         'src/lyndon.hpp',
                                         'src/misc.hpp',
                                         'src/signature.hpp',
                                         'src/tensor_algebra_ops.hpp'],
                                extra_compile_args=extra_compile_args)]

setuptools.setup(package_dir={'': 'src'},
                 ext_modules=ext_modules)
