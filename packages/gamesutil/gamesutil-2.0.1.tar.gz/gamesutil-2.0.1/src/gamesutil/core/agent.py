import os
import shutil
import zlib
from pathlib import Path

from gamesutil.dto.bootstrap_paths_dto import BootstrapPathsDTO
from gamesutil.dto.save_manifest_dto import SaveManifestDTO
from gamesutil.dto.user_instructions_dto import UserInstructionsDTO
from gamesutil.enums.user_request import UserRequest
from gamesutil.util.gamesutil_logger import GamesutilLogger


class Agent:
    def __init__(
        self,
        user_instructions_dto: UserInstructionsDTO,
        bootstrap_paths_dto: BootstrapPathsDTO,
        save_manifest_dto: SaveManifestDTO,
        steam_id: int,
    ) -> None:
        self.user_instructions_dto = user_instructions_dto
        self.bootsrap_paths_dto = bootstrap_paths_dto
        self.save_manifest_dto = save_manifest_dto
        self.steam_id = steam_id

    def do(self) -> None:
        if self.user_instructions_dto.request is UserRequest.COLLECT:
            self.__collect()
        else:
            self.__inject()

    def __collect(self) -> None:
        hot_location = self.save_manifest_dto.hot_location
        cold_location = self.save_manifest_dto.cold_location
        cold_location_old = (
            self.save_manifest_dto.cold_location.parent.joinpath(
                "old", self.save_manifest_dto.cold_location.name
            )
        )
        hot_location = Path(os.path.expandvars(hot_location)).resolve()
        cold_location = Path(os.path.expandvars(cold_location)).resolve()
        cold_location_old = Path(
            os.path.expandvars(cold_location_old)
        ).resolve()
        cold_name = self.save_manifest_dto.cold_name
        hot_location = Path(
            str(hot_location).replace("{STEAM_ID}", str(self.steam_id))
        )

        if not hot_location.exists():
            description = (
                f"WARNING: ({cold_name}) save location "
                f"not found - Skipping...\n"
                f"{hot_location!s}"
            )
            GamesutilLogger.get_logger().warning(description)
            return

        cold_location_exists = cold_location.exists()
        cold_location.mkdir(parents=True, exist_ok=True)
        if not cold_location_exists:
            debug = (
                f"Cold Location did not exist: {cold_location}"
                f" - Creating..."
            )
            GamesutilLogger.get_logger().debug(debug)

        if self.__is_locations_eq(cold_name, hot_location, cold_location):
            description = f"Save ({cold_name}) has not changed - Skipping..."
            GamesutilLogger.get_logger().info(description)
            return
        else:
            cold_location_old.mkdir(parents=True, exist_ok=True)
            shutil.rmtree(cold_location_old)
            cold_location_old.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                cold_location, cold_location_old, dirs_exist_ok=True
            )

            shutil.rmtree(cold_location)
            cold_location.mkdir(parents=True, exist_ok=True)
            description = (
                "Cold location is dirty - Deleting existing and recreating"
            )
            GamesutilLogger.get_logger().debug(description)

        description = f"-> Collecting {cold_name}"
        GamesutilLogger.get_logger().info(description)
        debug = f"{hot_location} -> {cold_location}"
        GamesutilLogger.get_logger().debug(debug)
        shutil.copytree(hot_location, cold_location, dirs_exist_ok=True)

    def __inject(self) -> None:
        hot_location = self.save_manifest_dto.hot_location
        cold_location = self.save_manifest_dto.cold_location
        cold_name = self.save_manifest_dto.cold_name
        hot_location = Path(os.path.expandvars(hot_location)).resolve()
        cold_location = Path(os.path.expandvars(cold_location)).resolve()
        hot_location = Path(
            str(hot_location).replace("{STEAM_ID}", str(self.steam_id))
        )

        if not cold_location.exists():
            description = (
                f"WARNING: ({cold_name}) cold location "
                f"not found - Skipping...\n"
                f"{cold_location!s}"
            )
            GamesutilLogger.get_logger().warning(description)
            return

        hot_location_exists = hot_location.exists()
        hot_location.mkdir(parents=True, exist_ok=True)
        if not hot_location_exists:
            debug = (
                f"Hot Location did not exist: {hot_location}" f" - Creating..."
            )
            GamesutilLogger.get_logger().debug(debug)

        if self.__is_locations_eq(cold_name, hot_location, cold_location):
            description = f"Save ({cold_name}) has not changed - Skipping..."
            GamesutilLogger.get_logger().info(description)
            return
        else:
            shutil.rmtree(hot_location)
            hot_location.mkdir(parents=True, exist_ok=True)
            description = (
                "Hot location is dirty - Deleting existing and recreating"
            )
            GamesutilLogger.get_logger().debug(description)

        description = f"-> Injecting {cold_name}"
        GamesutilLogger.get_logger().info(description)
        debug = f"{cold_location} -> {hot_location}"
        GamesutilLogger.get_logger().debug(debug)
        shutil.copytree(cold_location, hot_location, dirs_exist_ok=True)

    def __is_locations_eq(
        self, display_name: str, location_a: Path, location_b: Path
    ) -> bool:
        result_a = self.__get_crc_hash(location_a, location_a)
        result_b = self.__get_crc_hash(location_b, location_b)
        is_eq = result_a == result_b

        description = (
            f"{display_name} CRC results: {result_a} - {result_b} -> "
            f"is_eq: {is_eq}"
        )
        GamesutilLogger.get_logger().debug(description)

        return is_eq

    def __get_crc_hash(self, location: Path, parent_location: Path) -> int:
        crc = 0
        crc = (
            zlib.crc32(
                self.__get_crc_from_path(location, parent_location), crc
            )
            & 0xFFFFFFFF
        )
        crc = zlib.crc32(self.__get_crc_from_attr(location), crc) & 0xFFFFFFFF

        if location.is_file():
            crc = (
                zlib.crc32(self.__get_crc_from_file_contents(location), crc)
                & 0xFFFFFFFF
            )

        if location.is_dir():
            children = sorted(location.iterdir(), key=lambda p: p.name)
            for child in children:
                child_crc = self.__get_crc_hash(child, parent_location)
                crc = (
                    zlib.crc32(child_crc.to_bytes(4, "little"), crc)
                    & 0xFFFFFFFF
                )

        return crc

    def __get_crc_from_path(
        self, location: Path, parent_location: Path
    ) -> bytes:
        return str(location.relative_to(parent_location)).encode("utf-8")

    def __get_crc_from_attr(self, location: Path) -> bytes:
        stat = location.stat()
        if location.is_dir():
            return f"{stat.st_mode}".encode()
        else:
            return f"{stat.st_size}:{stat.st_mode}".encode()

    def __get_crc_from_file_contents(self, location: Path) -> bytes:
        file_crc = 0
        with location.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                file_crc = zlib.crc32(chunk, file_crc) & 0xFFFFFFFF
        return file_crc.to_bytes(4, "little", signed=False)
