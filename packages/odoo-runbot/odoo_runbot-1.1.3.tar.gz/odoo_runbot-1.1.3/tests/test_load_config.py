import pathlib

from odoo_runbot import runbot_env
from odoo_runbot.runbot_env import RunbotExcludeWarning, RunbotStepConfig, RunbotToolConfig, StepAction


def test_minimal_config():
    """[tool.runbot]
    modules = ["module_to_test"]
    """
    config_path = pathlib.Path(__file__).resolve().parent.joinpath("sample_config", "pyproject_minimal.toml")
    config = runbot_env.RunbotToolConfig.load_from_toml(config_path)
    global_module = ["module_to_test"]
    assert config == RunbotToolConfig(
        include_current_project=True,
        steps=[
            RunbotStepConfig(
                name="Runbot default Step",
                modules=global_module,
                action=StepAction.TESTS,
                test_tags=[],
                coverage=True,
                log_filters=[],
            ),
        ],
        pretty=True,
    )


def test_load_config():
    config_path = pathlib.Path(__file__).resolve().parent.joinpath("sample_config", "pyproject_complex.toml")
    config = runbot_env.RunbotToolConfig.load_from_toml(config_path)

    global_regex = [
        runbot_env.RunbotExcludeWarning(
            name="Global Logger Filter 1",
            regex=r".*global-regex-warning-1.*",
        ),
        runbot_env.RunbotExcludeWarning(
            name="global-regex-warning-2",
            regex=r".*global-regex-warning-2.*",
            min_match=1,
            max_match=1,
        ),
    ]
    global_module = ["labadis_test", "labadis_crm_test"]
    global_coverage = False

    assert config == RunbotToolConfig(
        include_current_project=True,
        steps=[
            RunbotStepConfig(
                name="Warmup",
                modules=["labadis_config"],
                action=StepAction.INSTALL,
                test_tags=[],
                coverage=global_coverage,
                log_filters=[
                    *global_regex,
                    RunbotExcludeWarning(
                        regex=".*Post install test regex-warnings.*",
                        name="Step Warmup - Logger Filter 3",
                        min_match=1,
                        max_match=1,
                    ),
                ],
            ),
            RunbotStepConfig(
                name="Do tests",
                modules=global_module,
                action=StepAction.TESTS,
                test_tags=["+at-install", "-post-install"],
                coverage=True,
                log_filters=[
                    *global_regex,
                    RunbotExcludeWarning(
                        regex=".*global-regex-warning-2.*",
                        name="global-regex-warning-2",
                        min_match=1,
                        max_match=1,
                    ),
                ],
            ),
            RunbotStepConfig(
                name="Post install test",
                modules=["labadis_crm_test"],
                action=StepAction.TESTS,
                test_tags=["-at-install", "+post-install"],
                coverage=True,
                log_filters=[
                    *global_regex,
                    RunbotExcludeWarning(
                        regex=".*Post install test regex-warnings.*",
                        name="ddd",
                        min_match=2,
                        max_match=2,
                    ),
                ],
            ),
        ],
        pretty=True,
    )


def test_min_max_match_log_filter():
    assert RunbotExcludeWarning(name="A", regex="A", min_match=2) == RunbotExcludeWarning(
        name="A",
        regex="A",
        min_match=2,
        max_match=2,
    ), "Assert Min and max match follow each other if not set"
    assert RunbotExcludeWarning(name="A", regex="A", min_match=10, max_match=2) == RunbotExcludeWarning(
        name="A",
        regex="A",
        max_match=10,
        min_match=10,
    ), "Assert Min and max match follow each other if not set"
    assert RunbotExcludeWarning(name="A", regex="A", min_match=-1) == RunbotExcludeWarning(
        name="A",
        regex="A",
        max_match=1,
        min_match=0,
    ), "Assert if Min is -1 then this means 0 min match"
    assert RunbotExcludeWarning(name="A", regex="A", min_match=0) == RunbotExcludeWarning(
        name="A",
        regex="A",
        max_match=1,
        min_match=0,
    ), "Assert if Min is 0 then this means 0 min match"
    assert RunbotExcludeWarning(name="A", regex="A", max_match=0) == RunbotExcludeWarning(
        name="A",
        regex="A",
        max_match=0,
        min_match=0,
    ), "Assert if Max is 0 means exacly 0 match possible"
    assert RunbotExcludeWarning(name="A", regex="A", max_match=999) == RunbotExcludeWarning(
        name="A",
        regex="A",
        max_match=100,
        min_match=1,
    ), "Assert if Max can't be more than 100If you want more than 100, you should fix this logger :-)"
