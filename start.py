import argparse, os
from launcher import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Minecraft launcher')
    subparsers = parser.add_subparsers(dest='command', required=True)

    start_parser = subparsers.add_parser('start', help='start game')
    start_parser.add_argument('--version', type=str, help='version', default='1.21.4')
    start_parser.add_argument('--work_dir', type=str, help='work dir', default=f'{os.getcwd()}/.minecraft')
    start_parser.add_argument('--username', type=str, help='username', default='root')

    download_parser = subparsers.add_parser('download', help='download game')
    download_parser.add_argument('--version', type=str, help='version', default='1.21.4')
    download_parser.add_argument('--work_dir', type=str, help='work dir', default=f'{os.getcwd()}/.minecraft')
    args = parser.parse_args()
    if args.command == 'start':
        main.start_minecraft(args.work_dir, args.version, args.username)
    if args.command == 'download':
        main.download_minecraft(args.version, args.work_dir)
