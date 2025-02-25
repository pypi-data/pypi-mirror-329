from altrustworthyai.provider._environment import EnvironmentDetector


def test_environment_detector():
    # Default
    detector = EnvironmentDetector()
    envs = detector.detect()
    assert len(envs) == 0

    # Check if assertion succeeds
    detector.checks["always_true"] = lambda: True
    envs = detector.detect()
    assert len(envs) == 1
    assert envs[0] == "always_true"
