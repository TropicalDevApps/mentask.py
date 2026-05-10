from unittest.mock import patch

from mentask.core.compression import ContextCompressor, ContextSnapper


def test_smart_compress_basic():
    content = "Hello world\n# comment\nprint('hi')"
    compressed = ContextCompressor.smart_compress(content)
    assert "Hello world" in compressed
    assert "# comment" not in compressed
    assert "print('hi')" in compressed


def test_smart_compress_code_blocks():
    content = """
    Some text
    ```python
    # This is a comment
    x = 10  # inline comment
    print(x)
    ```
    """
    compressed = ContextCompressor.smart_compress(content)
    assert "# This is a comment" not in compressed
    assert "# inline comment" not in compressed
    assert "x = 10" in compressed
    assert "print(x)" in compressed


def test_smart_compress_multiple_blocks():
    content = """
    ```python
    # first
    a = 1
    ```
    middle
    ```javascript
    // second
    let b = 2;
    ```
    """
    compressed = ContextCompressor.smart_compress(content)
    assert "# first" not in compressed
    assert "// second" not in compressed
    assert "a = 1" in compressed
    assert "let b = 2;" in compressed


def test_smart_compress_mixed_content():
    content = """
    Here is some code:
    ```python
    # comment
    x = 10
    ```
    And some text outside.
    """
    compressed = ContextCompressor.smart_compress(content)
    assert "# comment" not in compressed
    assert "x = 10" in compressed
    assert "Here is some code" in compressed


def test_compress_code_aliases():
    python_code = "# full line comment\nprint('py')"
    assert ContextCompressor.compress_code(python_code, "py") == "print('py')"

    js_code = "console.log('js'); // comment"
    assert ContextCompressor.compress_code(js_code, "js") == "console.log('js');"

    ts_code = "let x: number = 1; /* comment */"
    assert ContextCompressor.compress_code(ts_code, "ts") == "let x: number = 1;"


def test_compress_code_c_style():
    c_code = "int main() { return 0; } // c comment"
    assert ContextCompressor.compress_code(c_code, "c") == "int main() { return 0; }"

    cpp_code = "std::cout << 'cpp'; /* cpp comment */"
    assert ContextCompressor.compress_code(cpp_code, "cpp") == "std::cout << 'cpp';"

    java_code = "System.out.println('java'); // java comment"
    assert ContextCompressor.compress_code(java_code, "java") == "System.out.println('java');"

    ts_code_full = "const a: string = 'ts'; // ts comment"
    assert ContextCompressor.compress_code(ts_code_full, "typescript") == "const a: string = 'ts';"


def test_compress_code_unknown_language():
    code = "Some code // comment \n\n # another comment"
    compressed = ContextCompressor.compress_code(code, "unknown")
    # For unknown languages, it should just compress whitespace
    assert compressed == "Some code // comment \n # another comment"

    compressed_empty_lang = ContextCompressor.compress_code(code)
    assert compressed_empty_lang == "Some code // comment \n # another comment"


def test_smart_compress_code_replacer_edge_cases():
    # Empty code block without language
    content = "```\n```"
    assert ContextCompressor.smart_compress(content) == "```\n\n```"

    # Empty code block with language
    content = "```python\n```"
    assert ContextCompressor.smart_compress(content) == "```python\n\n```"

    # Unclosed code block
    content = "```javascript\n// comment\nlet x = 1;"
    assert ContextCompressor.smart_compress(content) == "```javascript\nlet x = 1;\n```"

    # Only language, no body, no newline
    content = "```python"
    assert ContextCompressor.smart_compress(content) == "```python\n\n```"

    # No language, no body, no newline
    content = "```"
    assert ContextCompressor.smart_compress(content) == "```\n\n```"


@patch("mentask.core.models_hub.ModelsHub.sync")
def test_get_token_status_safe(mock_sync):
    snapper = ContextSnapper("default")
    status = snapper.get_token_status(64000)
    assert status["tokens"] == 64000
    assert status["limit"] == 128000
    assert status["percentage"] == 50.0
    assert status["is_dangerous"] is False


@patch("mentask.core.models_hub.ModelsHub.sync")
def test_get_token_status_dangerous(mock_sync):
    snapper = ContextSnapper("default")
    status = snapper.get_token_status(120000)
    assert status["tokens"] == 120000
    assert status["limit"] == 128000
    assert status["percentage"] == 93.75
    assert status["is_dangerous"] is True


@patch("mentask.core.models_hub.ModelsHub.sync")
def test_get_token_status_boundary(mock_sync):
    snapper = ContextSnapper("default")

    # Exactly 90% is not dangerous according to current_tokens > (self.limit * 0.90)
    limit = 128000
    status = snapper.get_token_status(int(limit * 0.90))
    assert status["is_dangerous"] is False

    # Just above 90%
    status = snapper.get_token_status(int(limit * 0.90) + 1)
    assert status["is_dangerous"] is True
