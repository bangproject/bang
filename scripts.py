# This is a temporary workaround till Poetry supports scripts, see
# https://github.com/sdispater/poetry/issues/241.
from subprocess import check_call


def pre_commit() -> None:
    check_call(["pre-commit", "run", "--all-files"])


def test() -> None:
    check_call(["pytest", "tests/"])


def coverage() -> None:
    check_call(["pytest", "--cov", "."])
