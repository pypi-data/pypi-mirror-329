import pytest
import logging
import subprocess
from paic_patterns.modules.aider_llm_models import TESTING_MODEL
from paic_patterns.modules.spec_director_runner import run_spec_list_director
from paic_patterns.modules.data_types import (
    SpecFileListDirector,
    SpecTaskDirector,
    EvaluationResult,
)


class DummyProcess:
    def __init__(self, returncode=0, stdout="dummy output", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def dummy_subprocess_run_success(*args, **kwargs):
    return DummyProcess(returncode=0, stdout="dummy output", stderr="")


def dummy_evaluate_success(request):
    # Always returns success.
    return EvaluationResult(success=True, feedback="Success feedback")


def dummy_evaluate_failure(request):
    # Always returns failure.
    return EvaluationResult(success=False, feedback="Failure feedback")


def dummy_ai_code(coder, params):
    # Simulate AI coding with no side effects.
    pass


@pytest.fixture
def dummy_spec_success(tmp_path):
    # Create a spec for the success case with one director task.
    spec = SpecFileListDirector(
        plan_name="TestDirectorSuccess",
        pattern="list-director",
        architect=True,
        main_model="dummy-main",
        editor_model="dummy-editor",
        evaluator_model="dummy-evaluator",
        editable_context=["file1.py"],
        readonly_context=["file2.py"],
        high_level_objective="Dummy objective",
        implementation_details="Dummy implementation details",
        tasks=[
            SpecTaskDirector(
                title="Add Two Numbers",
                prompt="Implement add(a, b) that returns a + b",
                evaluator_count=2,
                evaluator_command="uv run python -c 'print(42)'",
            )
        ],
        fail_fast=False,
    )
    return spec


@pytest.fixture
def dummy_spec_failure(tmp_path):
    # Create a spec for the failure case with one director task, fail_fast set to True.
    spec = SpecFileListDirector(
        plan_name="TestDirectorFailure",
        pattern="list-director",
        architect=True,
        main_model="dummy-main",
        editor_model="dummy-editor",
        evaluator_model="dummy-evaluator",
        editable_context=["file1.py"],
        readonly_context=["file2.py"],
        high_level_objective="Dummy objective",
        implementation_details="Dummy implementation details",
        tasks=[
            SpecTaskDirector(
                title="Multiply Two Numbers",
                prompt="Implement multiply(a, b) that returns a * b",
                evaluator_count=1,
                evaluator_command="uv run python -c 'print(42)'",
            )
        ],
        fail_fast=True,
    )
    return spec


def test_run_spec_list_director_success(monkeypatch, dummy_spec_success):
    # Patch evaluate_task to always return success.
    monkeypatch.setattr(
        "paic_patterns.modules.director_intelligence.evaluate_task",
        dummy_evaluate_success,
    )
    # Patch ai_code to do nothing.
    monkeypatch.setattr(
        "paic_patterns.modules.spec_director_runner.ai_code", dummy_ai_code
    )
    # Patch subprocess.run to simulate a successful command execution.
    monkeypatch.setattr(subprocess, "run", dummy_subprocess_run_success)

    # Run the director spec; it should complete without raising exceptions.
    run_spec_list_director(dummy_spec_success)


def test_run_spec_list_director_fail_fast(monkeypatch, dummy_spec_failure):
    # Patch evaluate_task to always return failure.
    monkeypatch.setattr(
        "paic_patterns.modules.director_intelligence.evaluate_task",
        dummy_evaluate_failure,
    )
    # Patch ai_code to do nothing.
    monkeypatch.setattr(
        "paic_patterns.modules.spec_director_runner.ai_code", dummy_ai_code
    )
    # Patch subprocess.run to simulate a successful command execution.
    monkeypatch.setattr(subprocess, "run", dummy_subprocess_run_success)

    with pytest.raises(RuntimeError) as excinfo:
        run_spec_list_director(dummy_spec_failure)
    assert "did not succeed after" in str(excinfo.value)


def test_run_spec_list_director_no_evaluation(tmp_path):
    """Test running a director task without evaluation configuration using a real math example."""
    # Create a math file with initial content
    math_file = tmp_path / "math.py"
    math_file.write_text("# Math operations file\n")

    # Create a spec with no evaluator settings
    spec = SpecFileListDirector(
        plan_name="TestNoEval",
        pattern="list-director",
        architect=True,
        main_model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        evaluator_model=TESTING_MODEL,
        editable_context=[str(math_file)],
        readonly_context=[],
        tasks=[
            SpecTaskDirector(
                title="Add Function",
                prompt="Implement add(a, b) that returns a + b",
                # No evaluator_count or evaluator_command
            )
        ],
        fail_fast=False,
    )

    # Run the spec with real implementation
    run_spec_list_director(spec)

    # Verify the file was modified with the add function
    content = math_file.read_text()
    assert "def add(a, b):" in content
