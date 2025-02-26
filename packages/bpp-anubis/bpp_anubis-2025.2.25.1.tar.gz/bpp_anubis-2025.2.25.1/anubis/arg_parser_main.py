import logging
from argparse import Namespace, ArgumentParser
from pathlib import Path


def parse_arguments() -> tuple[Namespace, list]:
    known: Namespace
    unknown: list
    parser: ArgumentParser = ArgumentParser('Running in parallel mode')

    # anubis-specific stuff
    parser.add_argument('--features', type=str, default=['features'], nargs='*')
    parser.add_argument('--pass-threshold', type=float, default=1.0)
    parser.add_argument('--processes', type=int, default=10)
    parser.add_argument('--unit', type=str, default='example')
    parser.add_argument('--log-level', type=int, default=logging.DEBUG)

    # output files
    # parser.add_argument('--json', type=Path, default=None)
    parser.add_argument('--aggregate', type=Path, default=None)
    parser.add_argument('--junit', type=Path, default=None)
    parser.add_argument('--log-file', type=Path, default=None)
    parser.add_argument('--output', type=Path, default=Path('.output'))

    # flags
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--hide-failed', action='store_true')
    parser.add_argument('--hide-passed', action='store_true')
    parser.add_argument('--hide-summary', action='store_true')
    parser.add_argument('--pass-with-no-tests', action='store_true')
    parser.add_argument('--quiet', default=False, action='store_true')
    parser.add_argument('--delete-output', default=False, action='store_true')
    parser.add_argument('--log-std-out', action='store_true')

    # sent directly to behave
    parser.add_argument('--tags', type=str, nargs='*', action='append', default=[])
    parser.add_argument('-D', action='append')

    known, unknown = parser.parse_known_args()
    known.aggregate = known.output.joinpath('results.json') if known.aggregate is None else known.aggregate
    known.junit = known.output.joinpath('results.xml') if known.junit is None else known.junit
    known.log_file = known.output.joinpath('logs', 'anubis.log') if known.log_file is None else known.log_file

    # update user definitions
    user_defs: Namespace = Namespace()
    for user_def in known.D:
        data = user_def.split('=')
        setattr(user_defs, data[0], True if len(data) == 1 else data[-1])
    known.D = user_defs

    return known, unknown
