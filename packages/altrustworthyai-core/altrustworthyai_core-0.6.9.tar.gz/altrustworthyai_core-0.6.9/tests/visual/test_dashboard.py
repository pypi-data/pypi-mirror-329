from time import sleep

import pytest
from altrustworthyai.visual.dashboard import AppRunner


@pytest.mark.slow
def test_random_port():
    for _ in range(10):
        app_runner = AppRunner()
        app_runner.start()
        sleep(20)
        is_alive = app_runner.ping()
        app_runner.stop()
        if is_alive:
            break
    assert is_alive
