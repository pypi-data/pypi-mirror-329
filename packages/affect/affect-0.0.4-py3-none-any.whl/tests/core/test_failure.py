from affect import Failure


def test_failure() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.is_ok() is False
    assert failure_result.value == "Test Error"
