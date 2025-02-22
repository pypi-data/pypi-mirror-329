from argparse import ArgumentParser

from release_tool.release import FullRelease, LocalRelease, DryRunRelease

safety_default = 'dry-run'
safety = {
    'full': FullRelease,  # full shebang, commit, github-release, push, tag, etc
    'local': LocalRelease,  # do commit, but dont push or have external effects
    safety_default: DryRunRelease  # only touch local files
}


def get_parser():
    parser = ArgumentParser(description='Bump version')
    parser.add_argument('release_type', type=str, choices=DryRunRelease.version_components.keys(
    ), help='Version component bump')
    parser.add_argument('--method', '-m', type=str, choices=safety.keys(),
                        default=safety_default, help=f"Release method (default: {safety_default})")

    return parser


def main():
    parser = get_parser()

    opts = parser.parse_args()
    if opts.release_type not in DryRunRelease.version_components:
        parser.print_help()
        return

    release_class = safety[opts.method]
    release = release_class(opts.release_type)

    print(f"Starting release: {release}")
    release.do_release()


if __name__ == '__main__':
    main()
