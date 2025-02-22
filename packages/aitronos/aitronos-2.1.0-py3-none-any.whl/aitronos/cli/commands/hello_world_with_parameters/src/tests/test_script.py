from ..main.hello_world import main  # Using relative import


class TestHelloWorld:
    def test_hello_world(self):
        name = "Alice"
        expected_output = f'### Hello, World! \nAnd a warm welcome to the streamlined development to you, {name}'
        actual_output = main(name)
        assert actual_output == expected_output, f"Expected: {expected_output}, but got: {actual_output}"
