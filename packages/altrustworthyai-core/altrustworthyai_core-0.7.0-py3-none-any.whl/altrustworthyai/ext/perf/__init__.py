import sys

from altrustworthyai.ext.extension import PERF_EXTENSION_KEY, _is_valid_perf_explainer
from altrustworthyai.ext.extension_utils import load_class_extensions

load_class_extensions(
    sys.modules[__name__], PERF_EXTENSION_KEY, _is_valid_perf_explainer
)
