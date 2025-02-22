from ..main.hello_world import main  # Using relative import


class TestHelloWorld:
    def test_hello_world(self):
        expected_output = '### Hello, World! \nAnd a warm welcome to the streamlined development to you, John Doe'
        actual_output = main()
        assert actual_output == expected_output, f"Expected: {expected_output}, but got: {actual_output}"
