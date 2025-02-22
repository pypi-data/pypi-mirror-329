from zenith.base import NAME, get_greeting


def test_base_constant():
    assert NAME == "zenith"


def test_get_greeting_default():
    # When no name is provided, the default should be "World"
    assert get_greeting() == "Hello, World!"


def test_get_greeting_custom():
    # Test with a custom name
    assert get_greeting("Alice") == "Hello, Alice!"
