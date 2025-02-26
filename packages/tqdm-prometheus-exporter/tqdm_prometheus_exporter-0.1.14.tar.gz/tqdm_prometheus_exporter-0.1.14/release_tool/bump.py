'''Entry point for the release tool'''
from argparse import ArgumentParser

from release_tool.release import FullRelease, LocalRelease, DryRunRelease

# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

MODE_DEFAULT = 'dry-run'
mode_impl_map = {
    'full': FullRelease,  # full shebang, commit, github-release, push, tag, etc
    'local': LocalRelease,  # do commit, but dont push or have external effects
    MODE_DEFAULT: DryRunRelease  # only touch local files
}


def get_parser():
    parser = ArgumentParser(description='Bump version')

    release_types = DryRunRelease.version_components.keys()

    parser.add_argument('release_type', choices=release_types, type=str,
                        help='Version component bump')
    parser.add_argument('--mode', '-m', choices=mode_impl_map.keys(), type=str,
                        default=MODE_DEFAULT, help=f"Release method (default: {MODE_DEFAULT})")

    return parser


def main():
    parser = get_parser()

    opts = parser.parse_args()
    if opts.release_type not in DryRunRelease.version_components:
        parser.print_help()
        return

    release_class = mode_impl_map[opts.mode]
    release = release_class(opts.release_type)

    print(f"Starting release: {release}")
    release.do_release()


if __name__ == '__main__':
    main()
