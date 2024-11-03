import os
import argparse
import logging
import toml
import httpx
from torbot.modules.api import get_ip
from torbot.modules.color import color
from torbot.modules.updater import check_version
from torbot.modules.info import execute_all
from torbot.modules.linktree import LinkTree

def setup_logging(verbose: bool) -> None:
    """Set up logging configuration."""
    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=logging_level, 
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S")

def print_tor_ip_address(client: httpx.Client) -> None:
    """Displays the IP address obtained via Tor Project's API, with error handling."""
    try:
        resp = get_ip(client)
        if resp:
            print(resp.get("header", "No header available"))
            print(color(resp.get("body", "No body available"), "yellow"))
        else:
            logging.error("Failed to retrieve IP address: empty response.")
    except httpx.RequestError as e:
        logging.error(f"HTTP request error when fetching IP: {e}")
    except Exception as e:
        logging.error(f"Unexpected error retrieving IP: {e}")

def fetch_geolocation_info(ip: str) -> None:
    """Fetches and prints geolocation information for a given IP."""
    try:
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY&ip={ip}"
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"IP: {data['ip']}, Country: {data['country_name']}, City: {data['city']}")
    except httpx.RequestError as e:
        logging.error(f"Request error for geolocation: {e}")
    except ValueError:
        logging.error("Error decoding JSON response from geolocation API.")
    except Exception as e:
        logging.error(f"Unexpected error fetching geolocation: {e}")

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
    """Main execution function for the OSINT tool."""
    args = arg_parser.parse_args()
    setup_logging(args.v)

    if not args.url:
        arg_parser.print_help()
        sys.exit("Error: URL is a required argument.")

    if args.version:
        print(f"TorBot Version: {version}")
        sys.exit()

    if args.update:
        try:
            check_version()
        except Exception as e:
            logging.error(f"Failed to check or update version: {e}")
            sys.exit()

    socks5_proxy = f"socks5://{args.host}:{args.port}" if not args.disable_socks5 else None

    try:
        with httpx.Client(timeout=60, proxies=socks5_proxy) as client:
            if not args.quiet:
                print_header(version)
                print_tor_ip_address(client)

            if args.info:
                execute_all(client, args.url)

            if args.geolocation:
                ip_address = client.get(args.url).ip  # Assuming you can get IP from URL here.
                fetch_geolocation_info(ip_address)

            tree = LinkTree(url=args.url, depth=args.depth, client=client)
            tree.load()

            if args.save == "tree":
                tree.save()
            elif args.save == "json":
                tree.saveJSON()

            if args.visualize == "table" or not args.visualize:
                tree.showTable()
            elif args.visualize == "tree":
                print(tree)
            elif args.visualize == "json":
                tree.showJSON()
            else:
                logging.warning(f"Visualization type '{args.visualize}' not supported.")

    except httpx.RequestError as e:
        logging.error(f"HTTP request error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during client operations: {e}")

def set_arguments() -> argparse.ArgumentParser:
    """Parses user flags passed to TorBot."""
    parser = argparse.ArgumentParser(prog="TorBot", usage="Gather and analyze data from Tor sites.")
    parser.add_argument("-u", "--url", type=str, required=True, help="Specify a website link to crawl")
    parser.add_argument("--depth", type=int, help="Specify max depth of crawler (default 1)", default=1)
    parser.add_argument("--host", type=str, help="IP address for SOCKS5 proxy", default="127.0.0.1")
    parser.add_argument("--port", type=int, help="Port for SOCKS5 proxy", default=9050)
    parser.add_argument("--save", type=str, choices=["tree", "json"], help="Save results in a file")
    parser.add_argument("--visualize", type=str, choices=["table", "tree", "json"], help="Visualizes data collection.")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--version", action="store_true", help="Show current version of TorBot.")
    parser.add_argument("--update", action="store_true", help="Update TorBot to the latest stable version.")
    parser.add_argument("--info", action="store_true", help="Display basic info of the scanned site.")
    parser.add_argument("--geolocation", action="store_true", help="Fetch and display geolocation info for the IP.")
    parser.add_argument("-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--disable-socks5", action="store_true", help="Execute HTTP requests without using SOCKS5 proxy.")
    return parser

if __name__ == "__main__":
    try:
        arg_parser = set_arguments()
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pyproject.toml")

        # Load version from configuration file
        try:
            with open(config_file_path, "r") as f:
                data = toml.load(f)
                version = data.get("project", {}).get("version", "0.0.1")
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
