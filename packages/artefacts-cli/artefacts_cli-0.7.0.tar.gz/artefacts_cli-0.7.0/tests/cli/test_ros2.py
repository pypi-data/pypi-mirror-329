import os
import yaml
from unittest.mock import patch
import pytest

from artefacts.cli import WarpJob, WarpRun
from artefacts.cli.app import APIConf
from artefacts.cli.ros2 import generate_scenario_parameter_output, run_ros2_tests


def test_generate_parameter_output(tmp_path):
    params = {"turtle/speed": 5}
    file_path = tmp_path / "params.yaml"
    generate_scenario_parameter_output(params, file_path)
    with open(file_path) as f:
        ros2_params = yaml.load(f, Loader=yaml.Loader)
    assert ros2_params == {"turtle": {"ros__parameters": {"speed": 5}}}


@patch("os.path.exists", return_value=False)
@patch("artefacts.cli.ros2.run_and_save_logs")
@pytest.mark.ros2
def test_passing_launch_arguments(mock_run_and_save_logs, _mock_exists):
    os.environ["ARTEFACTS_JOB_ID"] = "test_job_id"
    os.environ["ARTEFACTS_KEY"] = "test_key"
    job = WarpJob("test_project_id", APIConf("sdfs"), "test_jobname", {}, dryrun=True)
    scenario = {
        "ros_testfile": "test.launch.py",
        "launch_arguments": {"arg1": "val1", "arg2": "val2"},
    }
    run = WarpRun(job, scenario, 0)

    run_ros2_tests(run)

    mock_run_and_save_logs.assert_called_once()
    assert (
        " test.launch.py arg1:=val1 arg2:=val2"
        in mock_run_and_save_logs.call_args[0][0]
    ), (
        "Launch arguments should be passed to the test command after the launch file path"
    )
