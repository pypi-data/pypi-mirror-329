from __future__ import annotations

import ctypes.wintypes
import json
import os
import platform
from pathlib import Path

import toml
from jsonschema import validate

from gamesutil.dto.bootstrap_paths_dto import BootstrapPathsDTO
from gamesutil.dto.save_manifest_dto import SaveManifestDTO
from gamesutil.exception.bootstrap_error import BootstrapError
from gamesutil.util.gamesutil_logger import GamesutilLogger

if platform.system() == "Windows":
    import win32evtlog  # pyright: ignore # noqa: PGH003
    import win32evtlogutil  # pyright: ignore # noqa: PGH003

import yaml

from gamesutil.util.static import Static


class FileImporter(Static):
    encoding = "utf-8"

    @staticmethod
    def get_path_from_str(
        path_candidate: str,
        is_dir_expected: bool = False,
        is_file_expected: bool = False,
    ) -> Path:
        """
        Get pathlib.Path from a str

        Args:
            path_candidate (str): The likely Path
            is_dir_expected (bool): Is the path expected to be a dir?
            is_file_expected (bool): Is the path expected to be a file?

        Returns:
            A pathlib.Path

        Raises:
            ValueError: If path_candidate is not supplied or path doesn't exist
            or path does not meet is_dir_expected/is_file_expected condition
        """
        if not path_candidate:
            description = "Expected a path candidate but none supplied "
            raise ValueError(description)

        path = Path(path_candidate)

        if not path.exists():
            description = f"Path candidate ({path_candidate}) does not exist"
            raise ValueError(description)

        if is_dir_expected and not path.is_dir():
            description = (
                f"Expected a dir for ({path_candidate}) but this is not a dir"
            )
            raise ValueError(description)

        if is_file_expected and not path.is_file():
            description = (
                f"Expected a file for ({path_candidate}) but path not a file"
                f"candidate is not a file {path_candidate}"
            )
            raise ValueError(description)

        return path

    @staticmethod
    def get_save_manifest_dtos(
        save_manifest_file_location: Path,
    ) -> list[SaveManifestDTO]:
        schema_file_location = (
            FileImporter.get_project_root()
            / "gamesutil"
            / "schemas"
            / "v2"
            / "save_manifest_schema.json"
        )
        with schema_file_location.open(encoding=FileImporter.encoding) as file:
            schema_dict = json.load(file)

        with save_manifest_file_location.open(
            encoding=FileImporter.encoding,
        ) as file:
            save_manifest = json.load(file)
            validate(instance=save_manifest, schema=schema_dict)
            records = []
            cold_location = Path(save_manifest["coldLocation"])
            saves = save_manifest["saves"]
            for record in saves:
                cold_name = record["coldName"]
                hot_location_str = record["hotLocation"]

                if not cold_name:
                    description = (
                        "WARNING: Encountered a manifest "
                        "record without coldName - Skipping..."
                    )
                    GamesutilLogger.get_logger().warning(description)
                    continue

                if not hot_location_str:
                    description = (
                        "WARNING: Encountered a manifest "
                        "record without hotLocation - Skipping..."
                    )
                    GamesutilLogger.get_logger().warning(description)
                    continue

                hot_location = Path(hot_location_str)
                records.append(
                    SaveManifestDTO(
                        cold_name=cold_name,
                        cold_location=cold_location / cold_name,
                        hot_location=hot_location,
                    )
                )
            return records

    @staticmethod
    def manifest_has_steam_id(
        save_manifest_file_location: Path,
    ) -> bool:
        schema_file_location = (
            FileImporter.get_project_root()
            / "gamesutil"
            / "schemas"
            / "v2"
            / "save_manifest_schema.json"
        )
        with schema_file_location.open(encoding=FileImporter.encoding) as file:
            schema_dict = json.load(file)

        with save_manifest_file_location.open(
            encoding=FileImporter.encoding,
        ) as file:
            save_manifest = json.load(file)
            validate(instance=save_manifest, schema=schema_dict)

            saves = save_manifest["saves"]
            for record in saves:
                location_str = record["hotLocation"]

                if location_str and "{STEAM_ID}" in location_str:
                    return True

            return False

    @staticmethod
    def get_logging_config(logging_config_path: Path) -> dict:
        with logging_config_path.open(
            "r", errors="strict", encoding=FileImporter.encoding
        ) as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_project_root() -> Path:
        """
        Gets the root of this project

        Returns:
            pathlib.Path: The project's root
        """
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_pyproject() -> dict:
        return toml.load(
            FileImporter.get_project_root().parent / "pyproject.toml"
        )

    @staticmethod
    def bootstrap() -> BootstrapPathsDTO:
        try:
            home_folder = Path()
            program_files_32bit_folder = Path()
            system = platform.system()

            if system == "Windows":
                csidl_personal = 5
                shgfp_type_current = 0

                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(  # pyright: ignore # noqa: PGH003
                    None, csidl_personal, None, shgfp_type_current, buf
                )
                home_folder = buf.value or ""
                if not home_folder:
                    description = "Could not locate Documents folder"
                    raise FileNotFoundError(description)  # noqa: TRY301

                csidl = 26

                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(  # pyright: ignore # noqa: PGH003
                    None,
                    csidl,
                    None,
                    0,  # shgfp_type
                    buf,
                )
                program_files_32bit_folder = buf.value or ""
                if program_files_32bit_folder:
                    steam_dir = (
                        Path(program_files_32bit_folder) / "Steam" / "userdata"
                    )
                    steam_ids = [
                        x.name for x in steam_dir.iterdir() if x.is_dir()
                    ]
                    steam_ids = [int(x) for x in steam_ids]
                else:
                    steam_ids = []

            elif system == "Linux":
                home_folder = os.getenv("HOME") or ""
                if os.getenv("XDG_DATA_HOME"):
                    steam_dir = (
                        Path(
                            os.path.expandvars(
                                os.getenv("XDG_DATA_HOME") or ""
                            )
                        ).resolve()
                        / "Steam"
                        / "userdata"
                    )
                    steam_ids = [
                        x.name for x in steam_dir.iterdir() if x.is_dir()
                    ]
                    steam_ids = [int(x) for x in steam_ids]
                else:
                    steam_ids = []
            else:
                description = f"Unsupported OS: {system}"
                raise OSError(description)  # noqa: TRY301

            gamesutil_dir = Path(home_folder) / "gamesutil"
            log_dir = gamesutil_dir / "log"
            gamesutil_dir.mkdir(exist_ok=True)
            log_dir.mkdir(exist_ok=True)

            return BootstrapPathsDTO(log_dir=log_dir, steam_ids=steam_ids)

        except Exception as e:
            if platform.system == "Windows":
                win32evtlogutil.ReportEvent(  # pyright: ignore # noqa: PGH003
                    "plexutil",
                    eventID=1,
                    eventType=win32evtlog.EVENTLOG_ERROR_TYPE,  # pyright: ignore # noqa: PGH003
                    strings=[""],
                )
            if e.args and len(e.args) >= 0:
                raise BootstrapError(e.args[0]) from e

            raise BootstrapError from e
