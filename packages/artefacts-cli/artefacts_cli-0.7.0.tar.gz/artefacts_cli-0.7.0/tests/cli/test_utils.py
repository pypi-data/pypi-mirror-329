import pytest

from artefacts.cli import WarpJob, WarpRun
from artefacts.cli.app import APIConf
from artefacts.cli.utils import add_output_from_default


@pytest.fixture
def new_run(project_with_key):
    job = WarpJob(
        project_with_key, APIConf(project_with_key), "jobname", {}, dryrun=True
    )
    return WarpRun(job=job, scenario={}, run_n=0)


def test_adds_nothing_on_missing_default_output(new_run, mocker, project_with_key):
    path = mocker.patch("artefacts.cli.utils.ARTEFACTS_DEFAULT_OUTPUT_DIR")
    mocked = {
        "exists.return_value": False,
        "is_dir.return_value": True,
    }
    path.configure_mock(**mocked)
    add_output_from_default(new_run)
    assert len(new_run.uploads) == 0
