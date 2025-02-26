import pytest
from click.testing import CliRunner

from ml_gcam import config
from ml_gcam.cli import cli

COMMANDS = [
    # core stuff
    "cli",
    "core:input-main",
    "core:input-parse",
    "core:input-defaults",
    "core:input-check",
    "core:output-explore",
    "interpolate:sample",
    "interpolate:make-inputs",
    "interpolate:make-configs",

    # data extracts
    "data:create-extracts",
    "data:create-scenarios",
    "data:create-targets",

    # training
    "training:run",
    "training:sweep-init",
    "training:sweep-run",

    # sample size experiments
    "training:sample-size",
    "evaluate:sample-size",
    "plot:sample-size",

    # cartesian experiments
    "training:cartesian",
    "evaluate:cartesian",
    "plot:cartesian",
    "table:cartesian",

    # sensitivity experiments
    "evaluate:sensitivity",
    # "plot:sensitivity",
    "plot:sensitivity-one-to-one",
    "table:sensitivity",

    # fraction of binary experiments
    "training:fraction-binary",
    "evaluate:fraction-binary",
    "table:fraction-binary",

    # debugging a checkpoint
    # "debug:checkpoint",

    # tables and plots from rest of paper
    "plot:map",
    "plot:previous-adoption",
    "plot:interp_vs_binary_targets",
    "table:outputs",
    "table:inputs",
    "table:datasets",
]


@pytest.fixture(scope="session")
def commands():
    return [cli] + [
        item
        for sublist in [source.commands.values() for source in cli.sources]
        for item in sublist
    ]


def test_group_works():
    runner = CliRunner()
    import os
    import random
    import string

    key = "".join(random.choices(string.ascii_letters, k=20))

    og = config.group
    _ = runner.invoke(cli)
    assert config.group == og, "group changed before and after cli invocation"

    _ = runner.invoke(cli, ["--group", key])
    assert config.group == key, "--group did not change config"

    os.environ["ML_GCAM__GROUP"] = key
    _ = runner.invoke(cli)
    assert config.group == key, "ML_GCAM__GROUP did not change config"


def test_debug_works():
    runner = CliRunner()
    import os

    og = bool(int(config.pretend))
    _ = runner.invoke(cli)
    assert (
        bool(int(config.pretend)) == og
    ), "pretend changed before and after cli invocation"

    arg = "--no-pretend" if og else "--pretend"
    _ = runner.invoke(cli, [arg])
    assert bool(int(config.pretend)) != og, "--pretend did not change config"

    os.environ["ML_GCAM__PRETEND"] = "0" if og else "1"
    _ = runner.invoke(cli)
    assert bool(int(config.pretend)) != og, "ML_GCAM__PRETEND did not change config"


def test_main_commands_exist(commands):
    runner = CliRunner()
    for command in commands:
        result = runner.invoke(command, ["--help"])
        assert (
            result.exit_code == 0
        ), f"help test failed for {command.name}, the command does not exit cleanly."
        assert (
            "Usage:" in result.output
        ), f"help output for {command.name} should include 'Usage:' line"


def test_help_option_available(commands):
    names = [c.name for c in commands]
    for command in COMMANDS:
        assert command in names, f"{command} is not in list of available commands"


def test_commands_with_checkpoint(commands):
    keep = [
        "training:run",
        "training:sample-size",
        "training:cartesian",
        "plot:map",
        "plot:previous-adoption",
        "evaluate:checkpoint",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--checkpoint_path" in result.output
        ), f"help output for {command.name} should include '--checkpoint_path'"


def test_commands_with_train_source(commands):
    keep = [
        "training:run",
        "training:sample-size",
        "training:cartesian",
        "evaluate:sample-size",
        "evaluate:checkpoint",
        "plot:map",
        "plot:previous-adoption",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--train_source" in result.output
        ), f"help output for {command.name} should include '--train_source'"


def test_commands_with_dev_source(commands):
    keep = [
        "training:run",
        "training:sample-size",
        "training:cartesian",
        "plot:map",
        "plot:previous-adoption",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--dev_source" in result.output
        ), f"help output for {command.name} should include '--dev_source'"


def test_commands_with_targets_path(commands):
    keep = [
        "training:run",
        "training:sample-size",
        "training:cartesian",
        "plot:map",
        "plot:previous-adoption",
        "plot:interp_vs_binary_targets",
        "table:datasets",
        "evaluate:cartesian",
        "evaluate:sample-size",
        "evaluate:checkpoint",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--targets_path" in result.output
        ), f"help output for {command.name} should include '--targets_path'"


def test_commands_with_save_path(commands):
    keep = [
        "plot:cartesian",
        "plot:map",
        "plot:previous-adoption",
        "plot:interp_vs_binary_targets",
        "table:outputs",
        "table:inputs",
        "table:datasets",
        "table:cartesian",
        "evaluate:cartesian",
        "evaluate:sample-size",
        "data:create-extracts",
        "data:create-scenarios",
        "data:create-targets",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--save_path" in result.output
        ), f"help output for {command.name} should include '--save_path'"


def test_commands_with_force(commands):
    keep = [
        "plot:cartesian",
        "plot:map",
        "plot:previous-adoption",
        "plot:interp_vs_binary_targets",
        "table:outputs",
        "table:inputs",
        "table:datasets",
        "table:cartesian",
        "evaluate:cartesian",
        "evaluate:sample-size",
        "data:create-extracts",
        "data:create-scenarios",
        "data:create-targets",
    ]
    check = [c for c in commands if c.name in keep]

    runner = CliRunner()
    for command in check:
        result = runner.invoke(command, ["--help"])
        assert (
            "--force" in result.output
        ), f"help output for {command.name} should include '--force'"
