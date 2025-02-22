"""
Template tags
"""

# Standard Library
import os

# Django
from django.conf import settings
from django.template.defaulttags import register
from django.templatetags.static import static
from django.utils.safestring import mark_safe

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from app_utils.urls import reverse_absolute

# AA Fleet Pings
from fleetpings import __title__, __version__
from fleetpings.helper.static_files import calculate_integrity_hash

logger = LoggerAddTag(my_logger=get_extension_logger(__name__), prefix=__title__)


@register.simple_tag
def fleetpings_reverse_url(view: str, *args) -> str:
    """
    Reverse URL

    :param view:
    :type view:
    :param args:
    :type args:
    :return:
    :rtype:
    """

    return reverse_absolute(viewname=view, args=list(args))


@register.simple_tag
def fleetpings_static(relative_file_path: str, script_type: str = None) -> str | None:
    """
    Versioned static URL

    :param relative_file_path: The file path relative to the `aa-fleetpings/fleetpings/static/fleetpings` folder
    :type relative_file_path: str
    :param script_type: The script type
    :type script_type: str
    :return: Versioned static URL
    :rtype: str
    """

    logger.debug(f"Getting versioned static URL for: {relative_file_path}")

    file_type = os.path.splitext(relative_file_path)[1][1:]

    logger.debug(f"File extension: {file_type}")

    # Only support CSS and JS files
    if file_type not in ["css", "js"]:
        raise ValueError(f"Unsupported file type: {file_type}")

    static_file_path = os.path.join("fleetpings", relative_file_path)
    static_url = static(static_file_path)

    # Integrity hash calculation only for non-debug mode
    sri_string = (
        f' integrity="{calculate_integrity_hash(relative_file_path)}" crossorigin="anonymous"'
        if not settings.DEBUG
        else ""
    )

    # Versioned URL for CSS and JS files
    # Add version query parameter to break browser caches when changing the app version
    # Do not add version query parameter for libs as they are already versioned through their file path
    versioned_url = (
        static_url
        if relative_file_path.startswith("libs/")
        else static_url + "?v=" + __version__
    )

    # Return the versioned URL with integrity hash for CSS
    if file_type == "css":
        return mark_safe(f'<link rel="stylesheet" href="{versioned_url}"{sri_string}>')

    # Return the versioned URL with integrity hash for JS files
    if file_type == "js":
        js_type = f' type="{script_type}"' if script_type else ""

        return mark_safe(
            f'<script{js_type} src="{versioned_url}"{sri_string}></script>'
        )

    return None
