import sys

from altrustworthyai.ext.extension import PROVIDER_EXTENSION_KEY, _is_valid_provider
from altrustworthyai.ext.extension_utils import load_class_extensions

load_class_extensions(sys.modules[__name__], PROVIDER_EXTENSION_KEY, _is_valid_provider)
