import sys

from altrustworthyai.ext.extension import GREYBOX_EXTENSION_KEY, _is_valid_greybox_explainer
from altrustworthyai.ext.extension_utils import load_class_extensions

load_class_extensions(
    sys.modules[__name__], GREYBOX_EXTENSION_KEY, _is_valid_greybox_explainer
)
