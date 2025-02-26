import os
from typing import Optional

import click

from tinybird.tb.modules.datafile.common import (
    Datafile,
    DatafileKind,
    DatafileSyntaxError,
    format_filename,
    parse,
)
from tinybird.tb.modules.datafile.exceptions import ParseException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def parse_datasource(
    filename: str,
    replace_includes: bool = True,
    content: Optional[str] = None,
    skip_eval: bool = False,
    hide_folders: bool = False,
    add_context_to_datafile_syntax_errors: bool = True,
) -> Datafile:
    basepath = ""
    if not content:
        with open(filename) as file:
            s = file.read()
        basepath = os.path.dirname(filename)
    else:
        s = content

    filename = format_filename(filename, hide_folders)
    try:
        doc = parse(
            s, "default", basepath, replace_includes=replace_includes, skip_eval=skip_eval, kind=DatafileKind.datasource
        )
        doc.validate()
    except DatafileSyntaxError as e:
        try:
            if add_context_to_datafile_syntax_errors:
                e.get_context_from_file_contents(s)
        finally:
            raise e
    # TODO(eclbg): all these exceptions that trigger a ClickException shouldn't be here, as this code will only run in
    # the server soon
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(filename=filename, lineno=e.lineno, error=e)
        ) from None

    return doc
