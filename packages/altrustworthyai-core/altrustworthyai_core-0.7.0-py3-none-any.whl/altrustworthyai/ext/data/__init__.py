import sys

from altrustworthyai.ext.extension import DATA_EXTENSION_KEY, _is_valid_data_explainer
from altrustworthyai.ext.extension_utils import load_class_extensions

load_class_extensions(
    sys.modules[__name__], DATA_EXTENSION_KEY, _is_valid_data_explainer
)
