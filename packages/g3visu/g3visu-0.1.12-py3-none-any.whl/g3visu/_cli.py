import argparse
import json
import os
import logging

from .meta import MetaProject, MetaZone
from .site import SiteSVG
from .typeinfo import TypeInfo
from .utils import ensure_token_set


logger = logging.getLogger('g3visu.meta')


def create_meta_files(
    system_config: dict, zone_name: str, output_dir: str, shv_user: str, shv_password: str
) -> None:
    # create the meta project and meta zone file data
    meta_project = MetaProject.model_validate_system_config(
        system_config, shv_user=shv_user, shv_password=shv_password
        )
    meta_zone = MetaZone.model_validate_system_config(
        system_config, name=zone_name
        )
    # create output directories and file paths
    meta_project_path = os.path.join(output_dir, '_meta.json')
    zone_dir = os.path.join(output_dir, zone_name)
    meta_zone_path = os.path.join(zone_dir, '_meta.json')
    os.makedirs(zone_dir, exist_ok=True)
    # write the file data to the output files
    with open(meta_project_path, 'w', encoding='utf-8') as f:
        f.write(meta_project.model_dump_json(indent=4, by_alias=True))
    with open(meta_zone_path, 'w', encoding='utf-8') as f:
        f.write(meta_zone.model_dump_json(indent=4, by_alias=True))


def create_site_svg_file(
    system_config: dict,
    zone_name: str,
    output_dir: str,
    visu_types_path: str | None = None
) -> None:
    # create the site svg file and update it from the system config
    if visu_types_path:
        site_svg = SiteSVG.from_local(visu_types_path)
    else:
        site_svg = SiteSVG.from_sites_repo()
    site_svg.update_from_system_config(system_config, zone_name)  # type: ignore  # noqa
    # write the file data to the output file
    site_svg.to_file(file_path=os.path.join(output_dir, 'site.svg'))


def create_type_info_file(
    system_config: dict, zone_name: str, output_dir: str
) -> None:
    # create the type info file and update it from the system config
    type_info = TypeInfo.model_validate_sites_repo()
    type_info.update_from_system_config(system_config, zone_name)  # type: ignore  # noqa
    # write the file data to the output file
    type_info_path = os.path.join(output_dir, 'typeInfo.cpon')
    with open(type_info_path, 'w', encoding='utf-8') as f:
        f.write(type_info.model_dump_cpon(indent=1, exclude_unset=True))


def valid_system_config(system_config_arg: str) -> tuple[str, str]:
    parts = system_config_arg.strip().split('@')
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f'System config path argument must be formatted as '
            f'"<path>@<zone_name>", got "{system_config_arg}".'
            )
    if not all(parts):
        raise argparse.ArgumentTypeError(
            f'Each part separated by "@" must be non-empty in the argument '
            f'"{system_config_arg}".'
            )
    return (parts[0], parts[1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate meta JSON files")
    parser.add_argument(
        "system_config",
        type=valid_system_config,
        help=(
            'Path to the system config JSON file with the specified software '
            'zone name. Format as follows: "<path>@<zone_name>", e.g., '
            '"/path/to/system_config.json@Z01".'
            )
        )
    parser.add_argument(
        "--visu-types",
        type=str,
        required=False,
        default=None,
        help=(
            'Path to a local `visu-types-g3.svg` file. If not provided, '
            'the file will be downloaded from the Gitlab repository.'
            )
        )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=False,
        choices=['meta', 'typeinfo', 'site-svg'],
        help=(
            'Specify the type of file to generate. If not provided, '
            'all files will be generated.'
            )
        )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=os.getcwd(),
        help="Path to the output directory",
        )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        required=False,
        help="Siteware default SHV user name",
        )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        required=False,
        help="Siteware default SHV user password",
        )
    parser.add_argument(
        '--log-level',
        type=str,
        required=False,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level.'
        )
    return parser.parse_args()


def main() -> None:
    # parse and validate the system config
    args = parse_args()
    logging.basicConfig(
        level=args.log_level,
        format='[%(name)s] %(levelname)s:%(message)s'
        )
    system_config_path, zone_name = args.system_config
    if not os.path.isfile(system_config_path):
        logger.error(f"System config file not found: {system_config_path}")
        raise SystemExit(1)
    with open(system_config_path, 'r', encoding='utf-8') as f:
        system_config = json.load(f)
    ensure_token_set()
    # create output directories and file paths
    zone_dir = os.path.join(args.output_dir, zone_name)
    zone_file_dir = os.path.join(zone_dir, '_files')
    os.makedirs(zone_file_dir, exist_ok=True)
    # create and write the files
    if args.file is None or args.file == 'meta':
        create_meta_files(system_config, zone_name, args.output_dir, args.user, args.password)
    if args.file is None or args.file == 'typeinfo':
        create_type_info_file(system_config, zone_name, zone_file_dir)
    if args.file is None or args.file == 'site-svg':
        create_site_svg_file(
            system_config, zone_name, zone_file_dir, args.visu_types
            )
