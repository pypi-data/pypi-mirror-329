import os
import sys
from fcntl import fcntl, F_SETFL, F_GETFL
from select import select

from pushy import PushyAPI, Feed

import argparse


async def main():
    parser = argparse.ArgumentParser(description='Pushy CLI')
    parser.add_argument('--api-key', type=str, required=False)
    sub = parser.add_subparsers(dest='action', required=True)

    parser_send = sub.add_parser('send', help='Send a notification')
    parser_send.add_argument('--mode', '-m', type=str, required=False, default='text')
    parser_send.add_argument('--tag', '-t', dest='tags', type=str, action='append', required=False, default=[])

    input_group = parser_send.add_mutually_exclusive_group()
    input_group.add_argument('--str', '--text', '-s', type=str, required=False, default=None)
    input_group.add_argument('--continuous', '-c', action='store_true', required=False)

    args = parser.parse_args()

    if args.action == 'send':
        api = await PushyAPI.create()
        feed = Feed(api, args.api_key)
        if args.str is not None:
            post = await feed.send_text(args.str, mode=args.mode, tags=args.tags)
            print(post.post_key)
        elif args.continuous:
            fcntl(sys.stdin, F_SETFL, fcntl(sys.stdin, F_GETFL) | os.O_NONBLOCK)
            while True:
                select([sys.stdin], [], [])
                try:
                    text = sys.stdin.read()
                    if not text:
                        break
                    post = await feed.send_text(text, mode=args.mode, tags=args.tags)
                    print(post.post_key)
                except BlockingIOError:
                    pass
        else:
            post = await feed.send_text(sys.stdin.read(), mode=args.mode, tags=args.tags)
            print(post.post_key)


def main_sync():
    import asyncio
    asyncio.run(main())
