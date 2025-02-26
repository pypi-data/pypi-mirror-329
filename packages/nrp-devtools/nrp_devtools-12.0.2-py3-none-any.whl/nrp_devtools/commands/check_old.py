from typing import Any

from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config.config import OARepoConfig


def check_imagemagick_callable(config: OARepoConfig, **kwargs: Any):
    try:
        run_cmdline("convert", "--version", grab_stdout=True, raise_exception=True)
    except:
        check_failed(
            "ImageMagick is not callable. Please install ImageMagick on your system.",
            will_fix=False,
        )
