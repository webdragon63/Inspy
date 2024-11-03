import os
import argparse
import sys
import logging
import toml
import httpx

from torbot.modules.api import get_ip
from torbot.modules.color import color
from torbot.modules.updater import check_version
from torbot.modules.info import execute_all
from torbot.modules.linktree import LinkTree


def print_tor_ip_address(client: httpx.Client) -> None:
    """
    Displays the IP address obtained via Tor Project's API, with error handling.
    """
    try:
        resp = get_ip(client)
        print(resp.get("header", "No header available"))
        print(color(resp.get("body", "No body available"), "yellow"))
    except Exception as e:
        logging.error(f"Failed to retrieve IP address: {e}")


def print_header(version: str = "Unknown") -> None:
    """
    Prints the TorBot banner including version and license.
    """
    license_msg = color("LICENSE: GNU Public License v3", "red")
    banner = r"""
                              ░▀█▀░█▀█░█▀▀░█▀█░█░█
                              ░░█░░█░█░▀▀█░█▀▀░░█░
                              ░▀▀▀░▀░▀░▀▀▀░▀░░░░▀░
                                                                                                                
 ---------ＡＮ  ＡＤＶＡＮＣＥ  ＤＡＲＫＷＥＢ  ＯＳＩＮＴ  ＴＯＯＬ----------
    """
    banner = color(banner, "red")

    title = f"""
                                    {banner}
               Inspy - Dark Web OSINT Tool
               GitHub : https://github.com/webdragon63/Inspy.git
               Version: {version}
            """
    print(title)


def run(arg_parser: argparse.ArgumentParser, version: str) -> None:
    args = arg_parser.parse_args()

    # setup logging
    date_fmt = "%d-%b-%y %H:%M:%S"
    logging_fmt = "%(asctime)s - %(levelname)s - %(message)s"
    logging_lvl = logging.DEBUG if args.v else logging.INFO
    logging.basicConfig(level=logging_lvl, format=logging_fmt, datefmt=date_fmt)

    # Ensure URL is provided
    if not args.url:
        arg_parser.print_help()
        sys.exit("Error: URL is a required argument.")

    # Display version information
    if args.version:
        print(f"TorBot Version: {version}")
        sys.exit()

    # Update TorBot version if requested
    if args.update:
        try:
            check_version()
        except Exception as e:
            logging.error(f"Failed to check or update version: {e}")
        sys.exit()

    # Configure SOCKS5 proxy settings
    socks5_proxy = f"socks5://{args.host}:{args.port}" if not args.disable_socks5 else None
    try:
        with httpx.Client(timeout=60, proxies=socks5_proxy) as client:
            # Display header and IP address if not in quiet mode
            if not args.quiet:
                print_header(version)
                print_tor_ip_address(client)

            # Execute site info gathering if requested
            if args.info:
                try:
                    execute_all(client, args.url)
                except Exception as e:
                    logging.error(f"Error executing site info gathering: {e}")

            # Load and display LinkTree
            try:
                tree = LinkTree(url=args.url, depth=args.depth, client=client)
                tree.load()

                # Save data if requested
                if args.save == "tree":
                    tree.save()
                elif args.save == "json":
                    tree.saveJSON()

                # Display LinkTree based on visualization option
                if args.visualize == "table" or not args.visualize:
                    tree.showTable()
                elif args.visualize == "tree":
                    print(tree)
                elif args.visualize == "json":
                    tree.showJSON()

            except Exception as e:
                logging.error(f"Failed to load or display LinkTree: {e}")

    except httpx.RequestError as e:
        logging.error(f"HTTP request error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during client operations: {e}")

    print("\n\n")


def set_arguments() -> argparse.ArgumentParser:
    """
    Parses user flags passed to TorBot
    """
    parser = argparse.ArgumentParser(
        prog="TorBot", usage="Gather and analyze data from Tor sites."
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="Specify a website link to crawl"
    )
    parser.add_argument(
        "--depth", type=int, help="Specify max depth of crawler (default 1)", default=1
    )
    parser.add_argument(
        "--host", type=str, help="IP address for SOCKS5 proxy", default="127.0.0.1"
    )
    parser.add_argument("--port", type=int, help="Port for SOCKS5 proxy", default=9050)
    parser.add_argument(
        "--save", type=str, choices=["tree", "json"], help="Save results in a file"
    )
    parser.add_argument(
        "--visualize",
        type=str,
        choices=["table", "tree", "json"],
        help="Visualizes data collection.",
    )
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument(
        "--version", action="store_true", help="Show current version of TorBot."
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update TorBot to the latest stable version",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display basic info of the scanned site. Only supports a single URL.",
    )
    parser.add_argument("-v", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--disable-socks5",
        action="store_true",
        help="Executes HTTP requests without using SOCKS5 proxy",
    )

    return parser


if __name__ == "__main__":
    try:
        arg_parser = set_arguments()
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pyproject.toml")

        # Load version from configuration file
        try:
            with open(config_file_path, "r") as f:
                data = toml.load(f)
                version = data.get("project", {}).get("version", "0.0.1")  # Default if not found
        except FileNotFoundError:
            logging.warning("Configuration file not found, using default version.")
            version = "0.0.1"
        except toml.TomlDecodeError as e:
            logging.error(f"Error parsing TOML file: {e}")
            version = "0.0.1"
        except Exception as e:
            logging.error(f"Unexpected error loading version: {e}")
            version = "0.0.1"

        # Run main program
        run(arg_parser, version)

    except KeyboardInterrupt:
        print("Interrupt received! Exiting cleanly...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
