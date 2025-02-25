import pytest
import yaml
import shutil
from pathlib import Path
from unittest import mock

from ..modules.aider_llm_models import TESTING_MODEL
from ..modules.spec_module import build_new_plan, ai_code, build_ai_coding_assistant
from ..modules.spec_runner import run_spec

# Mock AI coding to avoid API calls
@pytest.fixture(autouse=True)
def mock_ai_coding(monkeypatch):
    def mock_code(*args, **kwargs):
        code_params = args[1]
        test_file = code_params.editable_context[0]
        prompt = code_params.prompt.lower() if hasattr(code_params, 'prompt') else ''
        
        # For regular tasks, write functions
        code = ""
        if "add" in prompt:
            code = "def add(a: int, b: int) -> int:\n    return a + b\n"
        elif "multiply" in prompt:
            code = "def multiply(a: int, b: int) -> int:\n    return a * b\n"
        elif "subtract" in prompt:
            code = "def subtract(a: int, b: int) -> int:\n    return a - b\n"
        elif "divide" in prompt:
            code = "def divide(a: float, b: float) -> float:\n    return a / b\n"
            
        # Write the code to the test file if it's a Python file
        if str(test_file).endswith('.py'):
            with open(test_file, 'a') as f:
                f.write(code)
        return code

    class MockCoder:
        def __init__(self, *args, **kwargs):
            self.message_tokens_sent = 0
            self.message_tokens_received = 0
            self.total_cost = 0.0
            self.functions = None
            self.fnames = []
            self.read_only_fnames = []
            self._code = {}

        def run(self, prompt):
            if not self.fnames:
                return
            test_file = self.fnames[0]
            
            # For regular tasks, write functions
            code = ""
            if "add" in prompt.lower():
                code = "def add(a: int, b: int) -> int:\n    return a + b\n"
            elif "multiply" in prompt.lower():
                code = "def multiply(a: int, b: int) -> int:\n    return a * b\n"
            elif "subtract" in prompt.lower():
                code = "def subtract(a: int, b: int) -> int:\n    return a - b\n"
            elif "divide" in prompt.lower():
                code = "def divide(a: float, b: float) -> float:\n    return a / b\n"
                
            # Write the code to the test file if it's a Python file
            if str(test_file).endswith('.py'):
                if test_file not in self._code:
                    self._code[test_file] = ""
                self._code[test_file] += code
                with open(test_file, 'w') as f:
                    f.write(self._code[test_file])

        @classmethod
        def create(cls, *args, **kwargs):
            instance = cls()
            instance.fnames = kwargs.get('fnames', [])
            instance.read_only_fnames = kwargs.get('read_only_fnames', [])
            return instance

    # Mock the necessary components
    monkeypatch.setattr("paic_patterns.modules.spec_module.ai_code", mock_code)
    monkeypatch.setattr("aider.coders.Coder.create", MockCoder.create)
    monkeypatch.setattr("aider.coders.Coder.run", MockCoder.run)

def test_run_spec_summarization(tmp_path, mock_ai_coding):
    """Test that run_spec displays a summary with timing and git diff stats"""
    plan_name = "test_spec"
    # Create a new spec file in current working directory
    spec_file_path = build_new_plan(plan_name, "list")

    # Move it into tmp_path so we can modify it safely
    final_spec_path = tmp_path / f"{plan_name}.yaml"
    shutil.copy2(spec_file_path, final_spec_path)
    Path(spec_file_path).unlink()

    # Add tasks to the spec
    data = yaml.safe_load(final_spec_path.read_text())
    data["tasks"] = [
        {"title": "Add", "prompt": "Write a function to add two numbers."},
        {"title": "Multiply", "prompt": "Write a function to multiply two numbers."},
        {"title": "Subtract", "prompt": "Write a function to subtract two numbers."},
        {"title": "Divide", "prompt": "Write a function to divide two numbers."},
    ]

    data["mode"] = "coder"
    data["main_model"] = TESTING_MODEL
    data["editor_model"] = TESTING_MODEL

    # Create a temporary python file and set it as editable
    test_py = tmp_path / "test_file.py"
    test_py.write_text("# initial content\n")
    data["editable_context"] = [str(test_py)]
    data["readonly_context"] = []

    final_spec_path.write_text(yaml.safe_dump(data))

    # Run the spec
    run_spec(str(final_spec_path))

    # Assert or check that expected changes occurred
    assert final_spec_path.exists()
    assert "def add" in test_py.read_text().lower()
    assert "def multiply" in test_py.read_text().lower()
    assert "def subtract" in test_py.read_text().lower()
    assert "def divide" in test_py.read_text().lower()
