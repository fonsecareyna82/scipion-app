import os

from scipion.install.find_deps import isElf


def test_isElf_real_magic_bytes(tmp_path):
    elfLike = tmp_path / "elf_like"
    elfLike.write_bytes(b"\x7fELF" + b"\x00" * 10)
    assert isElf(str(elfLike))


def test_isElf_non_elf_file(tmp_path):
    notElf = tmp_path / "not_elf"
    notElf.write_text("hello world")
    assert not isElf(str(notElf))


def test_isElf_missing_file(tmp_path):
    assert not isElf(str(tmp_path / "missing"))
