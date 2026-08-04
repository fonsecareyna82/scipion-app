import os

import pytest

from scipion.utils import (
    getInstallPath, getModuleFolder, getScipionAppPath, getScipionHome,
    getScriptsPath, getTemplatesPath,
)


def test_path_helpers_are_relative_to_the_package():
    base = getScipionAppPath()
    assert base.endswith("scipion")
    assert getInstallPath() == os.path.join(base, "install")
    assert getScriptsPath() == os.path.join(base, "scripts")
    assert getTemplatesPath() == os.path.join(base, "templates")


def test_getScipionHome_unset(monkeypatch):
    monkeypatch.delenv("SCIPION_HOME", raising=False)
    with pytest.raises(SystemExit, match="must be set"):
        getScipionHome()


def test_getScipionHome_nonexistent_path(monkeypatch, tmp_path):
    monkeypatch.setenv("SCIPION_HOME", str(tmp_path / "does-not-exist"))
    with pytest.raises(SystemExit, match="does not exists"):
        getScipionHome()


def test_getScipionHome_not_a_folder(monkeypatch, tmp_path):
    aFile = tmp_path / "a_file"
    aFile.write_text("x")
    monkeypatch.setenv("SCIPION_HOME", str(aFile))
    with pytest.raises(SystemExit, match="not a folder"):
        getScipionHome()


def test_getScipionHome_valid(monkeypatch, tmp_path):
    monkeypatch.setenv("SCIPION_HOME", str(tmp_path))
    assert getScipionHome() == str(tmp_path)


def test_getModuleFolder():
    assert getModuleFolder("os") == os.path.dirname(os.__file__)

    with pytest.raises(ModuleNotFoundError):
        getModuleFolder("this_module_does_not_exist_xyz")
