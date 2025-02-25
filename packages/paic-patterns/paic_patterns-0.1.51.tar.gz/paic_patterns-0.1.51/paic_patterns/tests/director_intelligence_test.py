import json
import pytest
from paic_patterns.modules.director_intelligence import evaluate_task
from paic_patterns.modules.data_types import EvaluationRequest, SpecFileListDirector, EvaluationResult


class DummyMessage:
    def __init__(self, content):
        self.parsed = content


class DummyChoice:
    def __init__(self, message):
        self.message = message


class DummyCompletion:
    def __init__(self, choices):
        self.choices = choices


class MockOpenAIClient:
    def __init__(self, mock_response):
        self.beta = self.Beta(mock_response)

    class Beta:
        def __init__(self, mock_response):
            self.chat = self.Chat(mock_response)

        class Chat:
            def __init__(self, mock_response):
                self.completions = self.Completions(mock_response)

            class Completions:
                def __init__(self, mock_response):
                    self.mock_response = mock_response

                def parse(self, *args, **kwargs):
                    return self.mock_response


def dummy_create_success(*args, **kwargs):
    return DummyCompletion([DummyChoice(DummyMessage(EvaluationResult(success=True, feedback="Looks good")))])


def dummy_create_failure(*args, **kwargs):
    return DummyCompletion([DummyChoice(DummyMessage(EvaluationResult(success=False, feedback="Needs improvement")))])


def dummy_create_invalid(*args, **kwargs):
    return DummyCompletion([DummyChoice(DummyMessage("This is not valid JSON"))])


@pytest.fixture
def dummy_success(monkeypatch):
    mock_client = MockOpenAIClient(dummy_create_success())
    monkeypatch.setattr("paic_patterns.modules.director_intelligence.get_openai_client", lambda: mock_client)


@pytest.fixture
def dummy_failure(monkeypatch):
    mock_client = MockOpenAIClient(dummy_create_failure())
    monkeypatch.setattr("paic_patterns.modules.director_intelligence.get_openai_client", lambda: mock_client)


@pytest.fixture
def dummy_invalid(monkeypatch):
    mock_client = MockOpenAIClient(dummy_create_invalid())
    monkeypatch.setattr("paic_patterns.modules.director_intelligence.get_openai_client", lambda: mock_client)


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
        evaluator_command="dummy command",
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


def test_evaluate_task_invalid(dummy_invalid, dummy_evaluation_request):
    result = evaluate_task(dummy_evaluation_request)
    assert isinstance(result, EvaluationResult)
    assert result.success is False
    assert "Error evaluating task" in result.feedback
