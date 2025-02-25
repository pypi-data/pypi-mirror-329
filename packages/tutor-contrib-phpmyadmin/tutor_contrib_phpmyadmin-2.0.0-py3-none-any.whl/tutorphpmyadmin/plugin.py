import os
import sys
from glob import glob

import click
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Support for older Python versions
if sys.version_info >= (3, 9):
    import importlib_resources
else:
    import pkg_resources

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

########################################
# CONFIGURATION
########################################

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'PHPMYADMIN_'.
        ("PHPMYADMIN_VERSION", __version__),
        ("PHPMYADMIN_HOST", "phpmyadmin.{{ LMS_HOST }}"),
        ("PHPMYADMIN_PORT", "8081"),
        # https://hub.docker.com/_/phpmyadmin
        ("PHPMYADMIN_DOCKER_IMAGE", "phpmyadmin:5.2.1"),
        ("PHPMYADMIN_UPLOAD_LIMIT", "50M"),
    ]
)

########################################
# TEMPLATE RENDERING
########################################


def get_template_full_path(package_name: str, *template_path: str) -> str:
    if sys.version_info >= (3, 9):
        return str(
            importlib_resources.files(package_name)
            / os.path.join("templates", *template_path)
        )
    else:
        resource_path = pkg_resources.resource_filename(package_name, "")
        return os.path.join(resource_path, "templates", *template_path)


tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        get_template_full_path("tutorphpmyadmin", ""),
    ]
)

tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorphpmyadmin/templates/phpmyadmin/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/phpmyadmin/build``.
    [
        ("phpmyadmin/build", "plugins"),
        ("phpmyadmin/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
########################################

# For each file in tutorphpmyadmin/patches,
# apply a patch based on the file's name and contents.
if sys.version_info >= (3, 9):
    glob_pattern = str(importlib_resources.files("tutorphpmyadmin") / "patches" / "*")
else:
    glob_pattern = os.path.join(
        pkg_resources.resource_filename("tutorphpmyadmin", "patches"), "*"
    )

for path in glob(glob_pattern):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
