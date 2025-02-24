from click.testing import CliRunner
from bird_ospf_map.cli import cli

class TestBirdOSPFMap:
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
