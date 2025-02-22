from __future__ import annotations

import argparse
import pathlib
import sys
from argparse import RawTextHelpFormatter
from importlib.metadata import PackageNotFoundError, version

from gamesutil.dto.user_instructions_dto import UserInstructionsDTO
from gamesutil.enums.user_request import UserRequest
from gamesutil.exception.unexpected_argument_error import (
    UnexpectedArgumentError,
)
from gamesutil.exception.user_error import UserError
from gamesutil.util.file_importer import FileImporter
from gamesutil.util.gamesutil_logger import GamesutilLogger
from gamesutil.util.static import Static


class Prompt(Static):
    WARNING = (
        "⚠️ " if sys.stdout.encoding.lower().startswith("utf") else "[WARNING]"
    )

    @staticmethod
    def get_user_instructions_dto() -> UserInstructionsDTO:
        parser = argparse.ArgumentParser(
            description="Gamesutil", formatter_class=RawTextHelpFormatter
        )

        request_help_str = "Supported Requests: \n"

        for request in list(UserRequest):
            request_help_str += "-> " + request.value + "\n"

        parser.add_argument(
            "request",
            metavar="Request",
            type=str,
            nargs="?",
            help=request_help_str,
        )

        parser.add_argument(
            "-sm",
            "--save_manifest",
            metavar="save_manifest",
            type=pathlib.Path,
            nargs="+",
            help=("Path to the Save Manifest file"),
            default=None,
        )

        parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help=("Displays version"),
        )

        args, unknown = parser.parse_known_args()

        if unknown:
            raise UnexpectedArgumentError(unknown)

        request = args.request
        save_manifest = args.save_manifest
        is_version = args.version

        if is_version:
            gamesutil_version = ""

            try:
                gamesutil_version = version("gamesutil")

            except PackageNotFoundError:
                pyproject = FileImporter.get_pyproject()
                gamesutil_version = pyproject["project"]["version"]

            GamesutilLogger.get_logger().info(gamesutil_version)
            sys.exit(0)

        if not request:
            description = "Expected a request but none supplied, see -h"
            raise UserError(description)
        if not save_manifest:
            description = "Expected a save_manifest but none supplied, see -h"
            raise UserError(description)

        request = UserRequest.get_user_request_from_str(request)
        save_manifest = save_manifest[0]

        if request is UserRequest.INJECT:
            warning = (
                "⚠️"
                if sys.stdout.encoding.lower().startswith("utf")
                else "[WARNING]"
            )
            confirmation = (
                input(
                    f"{warning} Injection will overwrite hot saves with cold, "
                    "continue? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirmation != "y":
                debug = "Injection cancelled by user"
                GamesutilLogger.get_logger().debug(debug)
                sys.exit(0)

        debug = (
            "Received a User Request:\n"
            f"Request: {request.value if request else None}\n"
            f"Save Manifest: {save_manifest!s}\n"
        )
        GamesutilLogger.get_logger().debug(debug)

        return UserInstructionsDTO(
            request=request,
            save_manifest=save_manifest,
        )

    @staticmethod
    def resolve_steam_id_conflict(steam_ids: list[int]) -> int:
        count = 0
        msg = f"{Prompt.WARNING} Multiple Steam Ids found\n"

        for steam_id in steam_ids:
            count = count + 1
            msg = msg + f"{count}) {steam_id}\n"

        msg = msg + f"Select [1-{count}]: "

        confirmation = input(msg).strip().lower()

        selection = int(confirmation)

        if selection <= 0 or selection > len(steam_ids):
            description = f"Unexpected selection: {selection!s}"
            raise ValueError(description)

        return steam_ids[selection - 1]
