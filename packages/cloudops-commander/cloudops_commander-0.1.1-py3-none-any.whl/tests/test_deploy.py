import pytest
from cloudops_commander.deploy import deploy

def test_deploy_decorator_simulated(capsys):
    @deploy(target="gcp", region="europe-west1")
    def dummy():
        print("Deploying dummy app...")
    dummy()
    captured = capsys.readouterr().out
    assert "Deploying dummy app..." in captured
    assert "completed" in captured
