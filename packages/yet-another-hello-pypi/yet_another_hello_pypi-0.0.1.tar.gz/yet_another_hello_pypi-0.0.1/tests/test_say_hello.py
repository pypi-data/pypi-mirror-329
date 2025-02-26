from yet_another_hello_pypi import say_hello

def test_say_hello():
    result = say_hello("PyPI")
    assert result == "Hello, PyPI."
    print("Test passed")

if __name__ == "__main__":
    test_say_hello()
