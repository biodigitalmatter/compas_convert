from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import os
import sys
import tempfile

from invoke import task
from invoke.exceptions import UnexpectedExit

REPO_DIR = os.path.dirname(__file__)


class Log(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.out = out
        self.err = err

    def flush(self):
        self.out.flush()
        self.err.flush()

    def write(self, message):
        self.flush()
        self.out.write(message + "\n")
        self.out.flush()

    def info(self, message):
        self.write("[INFO] %s" % message)

    def warn(self, message):
        self.write("[WARN] %s" % message)


log = Log()


@task(default=True)
def help(ctx):
    """List available tasks and usage."""
    ctx.run("invoke --list")
    log.write('Use "invoke -h <taskname>" to get detailed help for a task.')


@task
def clean(ctx, interactive=True):
    """Cleans the local copy from compiled artifacts."""

    cmd = "git clean -xd"

    if interactive:
        cmd += " --interactive"

    with chdir(REPO_DIR):  # change dir to show paths relative to repo root
        ctx.run(cmd)


@task(
    help={
        "clean": "True to clean repo before building docsstarting.",
        "check_links": "True to check all web links in docs for validity.",
    }
)
def docs(ctx, clean=False, check_links=False):
    """Build package's HTML documentation."""
    pass  # not implemented yet
    # if clean:
    #     clean(ctx)

    # with chdir(REPO_DIR):

    #     opts = "-E" if clean else ""
    #     ctx.run("sphinx-build {} -b html docs dist/docs".format(opts))

    #     if check_links:
    #         linkcheck(ctx)


@task()
def check(ctx):
    """Check the consistency of documentation, coding style and a few other things."""
    with chdir(REPO_DIR):
        log.write("Running all pre-commit hooks on whole repository.")
        ctx.run("pre-commit run --all-files")


@task
def build(ctx):
    """Build project."""
    with chdir(REPO_DIR):
        ctx.run("python -m build")


@task
def raise_if_dirty(ctx):
    """Raise if there's modified or untracked files in repository."""
    try:
        ctx.run('test -z "$(git status --porcelain)"')
    except UnexpectedExit:
        raise Exception("Working directory contains changes or untracked files.")


@task()
def linkcheck(ctx):
    """Check links in documentation."""
    with chdir(REPO_DIR):
        log.write("Running link check...")
        ctx.run("sphinx-build -b linkcheck docs dist/docs")


@task(
    help={
        "doctest": "True to run doctest on all modules, otherwise False.",
    }
)
def test(ctx, doctest=False):
    """Run all tests."""
    with chdir(REPO_DIR):
        cmd = ["pytest"]
        if doctest:
            cmd.append("--doctest-modules")

        ctx.run(" ".join(cmd))


@task
def prepare_changelog(ctx):
    """Prepare changelog for next release."""
    unreleased_changelog_template = (
        "## Unreleased\n\n### Added\n\n### Changed\n\n### Removed\n\n\n## "
    )
    commit_msg = "[skip ci] Prepare changelog for next release"

    with chdir(REPO_DIR):
        # Preparing changelog for next release
        with open("CHANGELOG.md", "r+") as changelog:
            content = changelog.read()
            changelog.seek(0)
            changelog.write(content.replace("## ", unreleased_changelog_template, 1))

        ctx.run('git add CHANGELOG.md && git commit -m "{}"'.format(commit_msg))


@task(
    help={
        "gh_io_folder": "Folder where GH_IO.dll is located. Defaults to the Rhino 6.0 installation folder (platform-specific).",  # noqa: E501
        "ironpython": "Command for running the IronPython executable. Defaults to `ipy`.",  # noqa: E501
    }
)
def build_ghuser_components(ctx, gh_io_folder=None, ironpython=None):
    """Build Grasshopper user objects from source"""
    with chdir(dirname=REPO_DIR):
        with tempfile.TemporaryDirectory("actions.ghcomponentizer") as action_dir:
            source_dir = os.path.abspath(
                "src/compas_convert/rhino/grasshopper_components"
            )
            target_dir = os.path.join(source_dir, "ghuser")
            repo_url = (
                "https://github.com/compas-dev/compas-actions.ghpython_components.git"
            )
            ctx.run("git clone {} {}".format(repo_url, action_dir))
            if not gh_io_folder:
                import compas_ghpython

                gh_io_folder = compas_ghpython.get_grasshopper_plugin_path("6.0")

            if not ironpython:
                ironpython = "ipy"

            gh_io_folder = os.path.abspath(gh_io_folder)
            componentizer_script = os.path.join(action_dir, "componentize.py")

            ctx.run(
                '{} {} {} {} --ghio "{}"'.format(
                    ironpython,
                    componentizer_script,
                    source_dir,
                    target_dir,
                    gh_io_folder,
                )
            )


@task(
    pre=[raise_if_dirty, clean, check, test, build, docs, build_ghuser_components],
    help={"new_version": "Version number to release"},
    post=[prepare_changelog],
)
def release(ctx, new_version):
    """Releases the project in one swift command."""
    # Bump version and git tag it
    ctx.run("git -s tag {}".format(new_version))


@contextlib.contextmanager
def chdir(dirname=None):
    current_dir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_dir)
