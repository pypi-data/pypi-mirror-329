import argparse
from .scripts.installer import Installer
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description="Installer script")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Subcommands')

    # Create a subparser for the 'install' command
    install_parser = subparsers.add_parser('install', help='Install command')
    install_parser.add_argument('--installer', type=str, default='./installer.yaml', help='Path to the config YAML file')
    install_parser.add_argument('--kube-config', type=str, default='~/kube/config', help='Path to the kube config file')
    install_parser.add_argument('--start-from', type=str, default=None, help='Start from a specific step')
    install_parser.add_argument('--steps', type=str, default=None, help='Only run specific steps, comma separated')
    install_parser.add_argument('--excludes', type=str, default=None, help='Exlude some steps, comma separated')
    install_parser.add_argument('--watch', type=str, default=None, help='Watch for changes')
    args = parser.parse_args()

    # load .env content to environment variables
    load_dotenv()

    if args.command == 'install':
        installer = Installer(installer=args.installer, kube_config=args.kube_config, start_from=args.start_from, steps=args.steps, excludes=args.excludes, watch=args.watch)
        installer.install()

if __name__ == "__main__":
    main()
