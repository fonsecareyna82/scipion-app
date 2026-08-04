import os

import pytest

from scipion.install.funcs import (
    Command, CommandDef, CondaCommandDef, Environment, Target, ansi, mkdir,
)


def test_ansi():
    red = ansi(31)
    assert red("hi") == "\x1b[31mhi\x1b[0m"


def test_mkdir_creates_and_is_idempotent(tmp_path):
    target = tmp_path / "sub" / "dir"
    result = mkdir(str(target))
    assert target.is_dir()
    assert result == str(target)

    # calling again on an already-existing path is a no-op, not an error
    assert mkdir(str(target)) == str(target)


def test_command_existsAll(tmp_path):
    env = Environment()
    existing = tmp_path / "exists.txt"
    existing.write_text("x")

    assert Command(env, "true", targets=str(existing))._existsAll()
    assert not Command(env, "true", targets=str(tmp_path / "missing.txt"))._existsAll()
    assert Command(env, "true")._existsAll()  # no targets -> vacuously true


def test_target_state():
    env = Environment()
    t = Target(env, "mytarget", default=True)

    assert t.isDefault()
    t.setDefault(False)
    assert not t.isDefault()
    assert t.getName() == "mytarget"

    t.addCommand("echo hi")
    assert len(t.getCommands()) == 1

    t.addDep("otherdep")
    assert t.getDeps() == ["otherdep"]


def test_environment_getProcessors():
    assert Environment().getProcessors() == 1
    assert Environment(args=["-j", "4"]).getProcessors() == 4


def test_environment_path_helpers():
    env = Environment()
    assert env.getLibSuffix() == "so"
    assert Environment.getSoftware("foo", "bar").endswith(os.path.join("foo", "bar"))
    assert Environment.getLibFolder("libfoo.so").endswith(
        os.path.join("lib", "libfoo.so")
    )


def test_environment_targets():
    env = Environment()
    t = env.addTarget("foo", default=True)

    assert env.hasTarget("foo")
    assert env.getTarget("foo") is t
    assert t in env.getTargets()

    with pytest.raises(Exception, match="Duplicated target"):
        env.addTarget("foo")

    env.addTargetAlias("foo", "foo2")
    assert env.getTarget("foo2") is t

    with pytest.raises(Exception, match="not found"):
        env.addTargetAlias("nope", "alias")


def test_environment_addTargetDeps():
    env = Environment()
    foo = env.addTarget("foo")
    bar = env.addTarget("bar")

    env._addTargetDeps(bar, ["foo", foo])
    assert bar.getDeps() == ["foo", "foo"]

    with pytest.raises(Exception, match="does not exists"):
        env._addTargetDeps(bar, ["nonexistent"])

    with pytest.raises(Exception, match="should be either string or"):
        env._addTargetDeps(bar, [123])


def test_command_def_isEmpty_and_touch():
    empty = CommandDef("")
    assert empty.isEmpty()

    nonEmpty = CommandDef("echo hi", "a.txt")
    assert not nonEmpty.isEmpty()

    empty.touch("done.txt")
    cmd, targets = empty.getCommands()[-1]
    assert cmd == "touch done.txt"
    assert "done.txt" in targets


def test_command_def_cd_and_append_chaining():
    cmd = CommandDef("ls -l").cd("..").append("pwd", sep="?")
    assert cmd.getCommands()[0][0] == "ls -l && cd .. ? pwd"


def test_conda_command_def_condaInstall_activates_when_empty():
    conda = CondaCommandDef("myenv", "eval hook")
    assert conda.isEmpty()

    conda.condaInstall("numpy")

    command = conda.getCommands()[0][0]
    assert command == "eval hook && conda activate myenv && conda install numpy"


def test_conda_command_def_pipInstall_and_activate():
    conda = CondaCommandDef("myenv")
    conda.activate().pipInstall("-r requirements.txt")

    assert conda.getCommands()[0][0] == (
        "conda activate myenv && python -m pip install -r requirements.txt"
    )
