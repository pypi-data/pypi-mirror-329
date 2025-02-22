import hashlib
from io import StringIO
import os
import subprocess
from typing import Generator
import toml

from git import Repo


class DryRunRelease():
    version_components = {'major': 0, 'minor': 1, 'patch': 2}

    def __init__(self, bump_type):
        self.bump_type = bump_type

        self.from_version, self.to_version = DryRunRelease.determine_version_numbers(
            self.bump_type)

        os.makedirs('release', exist_ok=True)

    @staticmethod
    def determine_version_numbers(version_increment: str):
        toml_str = DryRunRelease.read_current_toml()

        version_str = toml_str['project']['version']
        version_parts = version_str.split('.')

        version_parts[DryRunRelease.version_components[version_increment]] = str(
            int(version_parts[DryRunRelease.version_components[version_increment]]) + 1)
        new_version = '.'.join(version_parts)

        toml_str['project']['version'] = new_version

        return (version_str, new_version)

    def __repr__(self):
        return f"{self.from_version} + {self.bump_type} => {self.to_version}"

    def do_release(self):
        self.bump_version()
        self.execute_buildtool()
        self.write_changelog()
        self.write_changes()
        self.create_tag()
        self.push()
        self.create_github_release()

    def bump_version(self):
        toml_content = self.read_current_toml()
        toml_content['project']['version'] = self.to_version

        with open('pyproject.toml', 'wt', encoding='utf-8') as f:
            f.write(toml.dumps(toml_content))
        with open("release/version.new.txt", 'wt', encoding='utf-8') as f:
            f.write(self.to_version)
        with open("release/version.old.txt", 'wt', encoding='utf-8') as f:
            f.write(self.from_version)
        with open("release/changes.md", 'wt', encoding='utf-8') as f:
            f.write(self.get_full_changelog())

    def execute_buildtool(self):
        subprocess.run(['uv', 'sync'], check=True)

    def write_changes(self):
        pass  # only for reals

    def create_tag(self):
        pass  # only for reals

    def push(self):
        pass  # only for reals

    def get_changes(self, head=True):
        lines = DryRunRelease.get_release_changes(
            self.from_version, 'HEAD' if head else self.to_version)

        return '\n'.join(DryRunRelease.format_release(lines))

    def get_full_changelog(self):
        buf = StringIO()

        buf.write(
            f"# [{self.to_version}](https://github.com/arrowed/tqdm-prometheus-exporter/releases/tag/release/{self.to_version})\n\n")
        buf.write(self.get_changes())
        buf.write("\n\n")
        buf.write(
            "## Also available from \n\n")
        buf.write(" - [PyPi]({self.pypi_release_url(self.to_version)})\n\n")
        buf.write(
            "## Release hashes\n\n")

        for artifact, hashes in self.get_hashes(self.get_release_files(self.to_version)):
            buf.write(f" - {os.path.basename(artifact)}\n")
            for alg, h in hashes.items():
                buf.write(f"   - {alg}: `{h}`\n")

        buf.write("\n")

        return buf.getvalue()

    def write_changelog(self):
        existing = ""
        if os.path.exists('CHANGELOG.md'):
            with open('CHANGELOG.md', 'rt', encoding="utf-8") as f:
                existing = f.read()

        with open('CHANGELOG.md', 'wt', encoding='utf-8') as f:
            f.write(self.get_full_changelog())
            f.write(existing)

    def create_github_release(self):
        pass

    def pypi_release_url(self, version) -> str:
        return f"https://pypi.org/project/tqdm-prometheus-exporter/{version}/"

    def get_release_files(self, version) -> Generator[str, None, None]:
        found = False
        for base, _, files in os.walk('dist'):
            for filename in files:
                if f"-{version}.tar.gz" in filename or f"-{version}-" in filename:
                    found = True
                    yield os.path.join(base, filename)

        if not found:
            raise ValueError(f"No dist file for release {version} found")

    def get_hashes(self, files) -> Generator[tuple[str, list[str]], None, None]:

        for filename in files:
            with open(filename, 'rb') as v:
                content = v.read()

            hashes = {}
            for m in ['md5', 'sha256']:
                hashes[m] = hashlib.new(m, content).hexdigest()

            yield (filename, hashes)

    @staticmethod
    def read_current_toml():
        with open('pyproject.toml', 'rt', encoding='utf-8') as f:
            toml_content = toml.loads(f.read())
        return toml_content

    @staticmethod
    def get_release_changes(from_version, to_version="HEAD"):
        r = Repo('.')

        prefix = "release/"
        if to_version.upper().strip() == "HEAD":
            prefix = ""

        o = r.git.log(
            f"release/{from_version}...{prefix}{to_version}", oneline=True)
        return o

    @staticmethod
    def format_release(result):
        for line in result.split('\n'):
            if line:
                commit_sha = line.split(' ')[0]
                message = ' '.join(line.split(' ')[1:])
                # todo add link to issues with \#<issue_number>
                yield f"* [{commit_sha}](https://github.com/arrowed/tqdm-prometheus-exporter/commit/{commit_sha}) {message}"


class LocalRelease(DryRunRelease):

    def write_changes(self):
        super().write_changes()

        r = Repo('.')
        r.git.add('pyproject.toml')
        r.git.add('CHANGELOG.md')
        r.git.add('uv.lock')
        r.git.commit(message=f"Release [{self.bump_type}] version to {
                     self.to_version}")

    def create_tag(self):
        r = Repo('.')
        r.git.tag(f"release/{self.to_version}")


class FullRelease(LocalRelease):
    def __init__(self, bump_type):
        super().__init__(bump_type)

    def bump_version(self):
        super().bump_version()

    def push(self):
        r = Repo('.')
        r.git.push('origin')
        r.git.push('origin', '--tags')

    def create_github_release(self):
        artifacts = self.get_release_files(self.to_version)

        subprocess.run(['gh', 'release', 'create', self.to_version, '--notes-file=release/changes.md',
                       '--latest=True', f"--title={self.to_version}", *artifacts], check=True)
