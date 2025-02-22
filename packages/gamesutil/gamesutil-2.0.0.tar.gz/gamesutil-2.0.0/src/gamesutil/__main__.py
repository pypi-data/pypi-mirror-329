import sys

from jsonschema.exceptions import ValidationError

from gamesutil.core.agent import Agent
from gamesutil.core.prompt import Prompt
from gamesutil.exception.bootstrap_error import BootstrapError
from gamesutil.exception.unexpected_argument_error import (
    UnexpectedArgumentError,
)
from gamesutil.exception.user_error import UserError
from gamesutil.util.file_importer import FileImporter
from gamesutil.util.gamesutil_logger import GamesutilLogger


def main() -> None:
    try:
        bootstrap_paths_dto = FileImporter.bootstrap()

        log_dir = bootstrap_paths_dto.log_dir

        log_config_file_path = (
            FileImporter.get_project_root()
            / "gamesutil"
            / "config"
            / "log_config.yaml"
        )

        log_config = FileImporter.get_logging_config(log_config_file_path)

        GamesutilLogger(log_dir, log_config)

        instructions_dto = Prompt.get_user_instructions_dto()
        save_manifest = instructions_dto.save_manifest
        save_manifest_dtos = FileImporter.get_save_manifest_dtos(save_manifest)

        steam_ids = bootstrap_paths_dto.steam_ids

        if FileImporter.manifest_has_steam_id(save_manifest):
            if len(steam_ids) == 1:
                steam_id = steam_ids[0]
            elif len(steam_ids) > 1:
                steam_id = Prompt.resolve_steam_id_conflict(steam_ids)
            else:
                steam_id = 0
        else:
            steam_id = 0

        for save_manifest_dto in save_manifest_dtos:
            Agent(
                user_instructions_dto=instructions_dto,
                bootstrap_paths_dto=bootstrap_paths_dto,
                save_manifest_dto=save_manifest_dto,
                steam_id=steam_id,
            ).do()

        sys.exit(0)

    except SystemExit as e:
        if e.code == 0:
            description = "Successful System Exit"
            GamesutilLogger.get_logger().debug(description)
        else:
            description = "\n=====Unexpected Error=====\n" f"{e!s}"
            GamesutilLogger.get_logger().exception(description)
            raise

    except UnexpectedArgumentError as e:
        sys.tracebacklimit = 0
        description = (
            "\n=====User Argument Error=====\n"
            "These arguments are unrecognized: \n"
        )
        for argument in e.args[0]:
            description += "-> " + argument + "\n"
        GamesutilLogger.get_logger().error(description)
        sys.exit(1)

    except UserError as e:
        sys.tracebacklimit = 0
        description = "\n=====User Error=====\n" f"{e!s}"
        GamesutilLogger.get_logger().error(description)

    except ValidationError as e:
        sys.tracebacklimit = 0
        description = "\n=====Invalid Schema Error=====\n" f"{e!s}"
        GamesutilLogger.get_logger().error(description)

    # No regular logger can be expected to be initialized
    except BootstrapError as e:
        description = "\n=====Program Initialization Error=====\n" f"{e!s}"
        e.args = (description,)
        raise

    except Exception as e:  # noqa: BLE001
        description = "\n=====Unexpected Error=====\n" f"{e!s}"
        GamesutilLogger.get_logger().exception(description)


if __name__ == "__main__":
    main()
