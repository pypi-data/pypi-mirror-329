import json
import pytest
from paic_patterns.modules.director_intelligence import evaluate_task
from paic_patterns.modules.data_types import EvaluationRequest, SpecFileListDirector, EvaluationResult


class DummyMessage:
    def __init__(self, content):
        self.content = content


class DummyChoice:
    def __init__(self, message):
        self.message = message


class DummyCompletion:
    def __init__(self, choices):
        self.choices = choices


def dummy_create_success(*args, **kwargs):
    # Create a dummy success JSON, wrapped in markdown fences to test parsing
    response_json = {"success": True, "feedback": "Looks good"}
    content = "```json\n" + json.dumps(response_json) + "\n```"
    return DummyCompletion([DummyChoice(DummyMessage(content))])


def dummy_create_failure(*args, **kwargs):
    # Create a dummy failure JSON; no markdown fences needed
    response_json = {"success": False, "feedback": "Needs improvement"}
    content = json.dumps(response_json)
    return DummyCompletion([DummyChoice(DummyMessage(content))])


@pytest.fixture
def dummy_success(monkeypatch):
    monkeypatch.setattr("paic_patterns.modules.director_intelligence.client.beta.chat.completions.create", dummy_create_success)


@pytest.fixture
def dummy_failure(monkeypatch):
    monkeypatch.setattr("paic_patterns.modules.director_intelligence.client.beta.chat.completions.create", dummy_create_failure)


@pytest.fixture
def dummy_evaluation_request():
    dummy_spec = SpecFileListDirector(
        plan_name="dummy_plan",
        pattern="list-director",
        architect=True,
        main_model="dummy-model",
        editor_model="dummy-editor",
        evaluator_model="dummy-evaluator-model",
        editable_context=["file1.py"],
        readonly_context=["file2.py"],
        high_level_objective="Dummy high level objective",
        implementation_details="Dummy implementation details",
        tasks=[],
        fail_fast=False
    )
    return EvaluationRequest(
        spec=dummy_spec,
        evaluator_command_result="Dummy command result",
        prompt="Dummy prompt",
        editable_context=["file1.py"],
        readonly_context=["file2.py"]
    )


def test_evaluate_task_success(dummy_success, dummy_evaluation_request):
    result = evaluate_task(dummy_evaluation_request)
    assert isinstance(result, EvaluationResult)
    assert result.success is True
    assert result.feedback == "Looks good"


def test_evaluate_task_failure(dummy_failure, dummy_evaluation_request):
    result = evaluate_task(dummy_evaluation_request)
    assert isinstance(result, EvaluationResult)
    assert result.success is False
    assert result.feedback == "Needs improvement"


# Add a dummy create function that returns invalid JSON output
def dummy_create_invalid(*args, **kwargs):
    # Return output that is not valid JSON (e.g., missing braces or plain text)
    content = "This is not valid JSON"
    return DummyCompletion([DummyChoice(DummyMessage(content))])


@pytest.fixture
def dummy_invalid(monkeypatch):
    monkeypatch.setattr(
        "paic_patterns.modules.director_intelligence.client.beta.chat.completions.create",
        dummy_create_invalid
    )


def test_evaluate_task_invalid(dummy_invalid, dummy_evaluation_request):
    # Expect evaluate_task to raise an exception when parsing fails.
    with pytest.raises(Exception):
        evaluate_task(dummy_evaluation_request)
