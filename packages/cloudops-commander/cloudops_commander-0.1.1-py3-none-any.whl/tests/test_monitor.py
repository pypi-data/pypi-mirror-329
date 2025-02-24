from cloudops_commander.monitor import watch

def test_monitor_watch(capsys):
    watch(service="test_service", alert_callback=lambda msg: print(f"Alert: {msg}"))
    output = capsys.readouterr().out
    assert "Monitoring service 'test_service'" in output
    assert "Service test_service is healthy!" in output
