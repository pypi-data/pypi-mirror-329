#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import os
import platform

from .build_vai_custom_op import compile_custom_op, get_library_path

_DEVICE_SUFFIX = 'DEVICE_SED_MASK'

# Synchronized from custom_op_library.cc
_COP_DOMAIN = "com.vai.quantize"
_COP_VERSION = 1

__all__ = ["get_library_path", "_COP_DOMAIN", "_COP_VERSION", "_DEVICE_SUFFIX"]
