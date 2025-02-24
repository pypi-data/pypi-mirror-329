from affect import Success


def test_success() -> None:
    success_result = Success(value="Test Value")
    assert success_result.is_ok() is True
    assert success_result.value == "Test Value"
