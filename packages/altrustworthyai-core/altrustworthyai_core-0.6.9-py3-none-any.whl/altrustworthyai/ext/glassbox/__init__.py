import sys

from altrustworthyai.ext.extension import GLASSBOX_EXTENSION_KEY, _is_valid_glassbox_explainer
from altrustworthyai.ext.extension_utils import load_class_extensions

load_class_extensions(
    sys.modules[__name__], GLASSBOX_EXTENSION_KEY, _is_valid_glassbox_explainer
)
