"""Parses an nginx.conf file and handle the errors"""

import io

import crossplane


class ParseError(BaseException):
    pass


def _format_error(error: dict):
    msg = io.StringIO()
    msg.write(error["file"])
    if error["line"] is not None:
        msg.write(f"({error['line']})")
    fault = error["error"] or "unknown error"
    msg.write(f": {fault}")
    return msg.getvalue()


def _handle_errors(errors: list):
    if not errors:
        return

    raise ParseError("\n".join(_format_error(error) for error in errors))


def parse(path: str) -> list[dict]:
    """Parses a path and handle errors"""
    root = crossplane.parse(path)
    _handle_errors(root["errors"])

    parsed_list = []
    for config in root["config"]:
        _handle_errors(config["errors"])
        parsed_list.append(config["parsed"])
    return parsed_list
