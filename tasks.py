from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import os
import sys
import tempfile

from invoke import task

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
    """Lists available tasks and usage."""
    ctx.run("invoke --list")
    log.write('Use "invoke -h <taskname>" to get detailed help for a task.')


@task
def clean(ctx):
    """Cleans the local copy from compiled artifacts."""

    with chdir(REPO_DIR):
        ctx.run("git clean --interactive -x")


@task(
    help={
        "clean": "True to clean repo before building docsstarting.",
        "check_links": "True to check all web links in docs for validity.",
    }
)
def docs(ctx, clean=False, check_links=False):
    """Build package's HTML documentation."""
    if clean:
        clean(ctx)

    with chdir(REPO_DIR):

        opts = "-E" if clean else ""
        ctx.run("sphinx-build {} -b html docs dist/docs".format(opts))

        if check_links:
            linkcheck(ctx)


@task()
def linkcheck(ctx):
    """Check links in documentation."""
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
    UNRELEASED_CHANGELOG_TEMPLATE = (
        "## Unreleased\n\n### Added\n\n### Changed\n\n### Removed\n\n\n## "
    )

    with chdir(REPO_DIR):
        # Preparing changelog for next release
        with open("CHANGELOG.md", "r+") as changelog:
            content = changelog.read()
            changelog.seek(0)
            changelog.write(content.replace("## ", UNRELEASED_CHANGELOG_TEMPLATE, 1))

        ctx.run(
            'git add CHANGELOG.md && git commit -m "Prepare changelog for next release"'
        )


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
            target_dir = source_dir = os.path.abspath(
                "src/compas_convert/rhino/grasshopper_components"
            )
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


@contextlib.contextmanager
def chdir(dirname=None):
    current_dir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_dir)
