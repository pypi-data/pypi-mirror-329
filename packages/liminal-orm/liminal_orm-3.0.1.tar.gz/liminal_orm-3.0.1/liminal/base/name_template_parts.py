import warnings

from liminal.orm.name_template_parts import *  # noqa: F403

warnings.warn(
    "Importing from 'liminal.base.name_template_parts' is deprecated. Please import from 'liminal.orm.name_template_parts' instead.",
    DeprecationWarning,
    stacklevel=2,
)
