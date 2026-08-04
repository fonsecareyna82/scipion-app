from scipion.install.funcs import CommandDef, CondaCommandDef


def test_command_def():
    myCmd = CommandDef("ls -l", "lolo") \
        .append("cd ..", ["one", "two"]) \
        .append("cd .", sep="?")

    assert myCmd.getCommands()[0][0] == "ls -l && cd .. ? cd ."
    assert myCmd.getCommands()[0][1] == ["lolo", "one", "two"]


def test_conda_command_def():
    cmds = CondaCommandDef("modelangelo-3.0")
    cmds.create('python=3.9').activate().cd('model-angelo') \
        .pipInstall('-r requirements.txt') \
        .condaInstall('-y torchvision torchaudio cudatoolkit=11.3 -c pytorch') \
        .pipInstall('-e .').touch('../env-installed.txt')

    commands = cmds.getCommands()
    assert len(commands) == 1
    assert "conda create -y -n modelangelo-3.0 python=3.9" in commands[0][0]
