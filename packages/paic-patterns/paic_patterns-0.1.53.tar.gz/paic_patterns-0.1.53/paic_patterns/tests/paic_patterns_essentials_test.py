import pytest
import yaml
import shutil
import os
from pathlib import Path

from ..modules.aider_llm_models import TESTING_MODEL
from ..modules.spec_module import (
    build_new_plan,
    parse_spec_file,
    spec_file_to_aider_instance,
    ping_ai_intelligence,
    spec_file_to_load_file,
)
from ..modules.spec_runner import run_spec, run_spec_self_build
from ..modules.data_types import PaicPatternEnum

# No mocks - using real API calls


# ------ Pattern Tests ------


def test_spec_run_list_pattern(tmp_path):
    """Test running spec with list pattern"""
    plan_name = "test_list_run"
    spec_file_path = build_new_plan(plan_name, "list")
    final_spec_path = tmp_path / f"{plan_name}.yml"
    shutil.copy2(spec_file_path, final_spec_path)
    Path(spec_file_path).unlink()

    # Add test tasks
    data = yaml.safe_load(final_spec_path.read_text())
    data["tasks"] = [
        {"title": "Test Task", "prompt": "CREATE test_function() -> True"},
        {
            "title": "Add Function",
            "prompt": "CREATE add_numbers(a, b) that adds two numbers and returns the result",
        },
        {
            "title": "Multiply Function",
            "prompt": "CREATE multiply_numbers(a, b) that multiplies two numbers and returns the result",
        },
    ]
    data["main_model"] = TESTING_MODEL
    data["editor_model"] = TESTING_MODEL

    # Create test file and update paths
    test_py = tmp_path / "test_file.py"
    test_py.write_text("# Initial content\n")
    data["editable_context"] = [str(test_py)]
    data["readonly_context"] = []

    final_spec_path.write_text(yaml.safe_dump(data))

    run_spec(str(final_spec_path))

    content = test_py.read_text()
    assert "def test_function" in content
    assert "return True" in content
    assert "def add_numbers" in content
    assert "def multiply_numbers" in content


def test_run_spec_list_reflection(tmp_path):
    """
    Test that a spec file with pattern 'list-reflection' processes tasks and reflections
    correctly, modifying the editable file with both original and reflection outputs.
    """
    import yaml
    from paic_patterns.modules.aider_llm_models import TESTING_MODEL
    from paic_patterns.modules.spec_runner import run_spec

    # Create a temporary file for editable_context
    test_file = tmp_path / "test_reflection.py"
    test_file.write_text("")  # start empty

    spec_content = {
        "plan_name": "test_reflection",
        "pattern": "list-reflection",
        "architect": False,
        "main_model": TESTING_MODEL,
        "editor_model": TESTING_MODEL,
        "editable_context": [str(test_file)],
        "readonly_context": [],
        "high_level_objective": "Simple math functions",
        "implementation_details": "Each function should perform a basic math operation",
        "tasks": [
            {
                "title": "Add",
                "prompt": "Write add function",
                "reflection_count": 1,
                "reflection_prompt_prefix": "add comments to the function definitions",
            },
            {
                "title": "Multiply",
                "prompt": "Write multiply function",
            },
            {
                "title": "Subtract",
                "prompt": "Write subtract function",
                "reflection_count": 2,
                "reflection_prompt_prefix": "add comments to the function definitions",
            },
        ],
    }
    spec_file = tmp_path / "spec_reflection.yaml"
    spec_file.write_text(yaml.safe_dump(spec_content))

    run_spec(str(spec_file))

    # Read the content of the editable file
    content = test_file.read_text().lower()

    # Check that the outputs from processing the tasks are present
    # For task "Add", expect the original function output and that function comments were added.
    assert "def add" in content, "Missing add function output"
    # Verify that at least one line in the file is a comment (a '#' at the start)
    assert any(
        line.strip().startswith("#") for line in content.splitlines()
    ), "Missing function comments for add function"

    # For task "Multiply", expect only the original output (no reflection comments)
    assert "def multiply" in content, "Missing multiply function output"

    # For task "Subtract", expect the original function output and that function comments were added.
    assert "def subtract" in content, "Missing subtract function output"
    comment_lines = [
        line
        for line in content.splitlines()
        if line.strip().startswith("#") or line.strip().startswith('"""')
    ]
    assert len(comment_lines) >= 1, "Expected function comments for subtract function"


def test_run_spec_list_director(tmp_path):
    """Test running spec with list-director pattern using math functions"""
    import yaml
    from pathlib import Path
    from ..modules.aider_llm_models import TESTING_MODEL
    from ..modules.spec_runner import run_spec

    # Create a temporary file to serve as the editable context
    test_file = tmp_path / "test_director.py"
    test_file.write_text("# Initial content\n")

    # Create a test script to evaluate the math functions
    test_eval = tmp_path / "test_eval.py"
    test_eval.write_text(
        """
import sys
import importlib.util

# Load the module dynamically
spec = importlib.util.spec_from_file_location("test_module", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Test the add function
result = module.add(5, 3)
print(f"add(5, 3) = {result}")
assert result == 8, f"Expected 8, got {result}"

# Test the multiply function
result = module.multiply(4, 7)
print(f"multiply(4, 7) = {result}")
assert result == 28, f"Expected 28, got {result}"

print("All tests passed!")
"""
    )

    # Create spec content with pattern 'list-director'
    spec_content = {
        "plan_name": "test_director",
        "pattern": "list-director",
        "architect": True,
        "main_model": TESTING_MODEL,
        "editor_model": TESTING_MODEL,
        "evaluator_model": "o3-mini",
        "editable_context": [str(test_file)],
        "readonly_context": [],
        "high_level_objective": "Implement basic math functions",
        "implementation_details": "Create functions for addition and multiplication",
        "tasks": [
            {
                "title": "Implement Addition Function",
                "prompt": "Create a function in the file:\n`add(a, b)` that returns the sum of two numbers",
            },
            {
                "title": "Implement Subtraction Function",
                "prompt": "Create a function in the file:\n`subtract(a, b)` that returns the difference of two numbers (a - b)",
            },
            {
                "title": "Implement Multiplication Function",
                "prompt": "Create a function in the file:\n`multiply(a, b)` that returns the product of two numbers",
                "evaluator_count": 1,
                "evaluator_command": f"python {test_eval} {test_file}",
            },
        ],
        "fail_fast": True,
    }

    spec_file = tmp_path / "spec_director.yaml"
    spec_file.write_text(yaml.safe_dump(spec_content))

    # Run the spec
    run_spec(str(spec_file))

    # Verify the content of the file
    content = test_file.read_text().lower()
    assert "def add" in content, "Missing add function"
    assert "def multiply" in content, "Missing multiply function"
    assert "def subtract" in content, "Missing subtract function"


def test_create_markdown_pattern(tmp_path):
    """Test creating a new spec with markdown pattern"""
    # Create a plan name with spaces to test replacement
    plan_name = "test markdown pattern"
    expected_filename = "test_markdown_pattern.md"
    
    # Generate the markdown spec file
    spec_file_path = build_new_plan(str(tmp_path / plan_name), "markdown")
    
    # Read the content of the generated file
    content = Path(spec_file_path).read_text()
    
    # Verify the file was created with the correct name
    assert Path(spec_file_path).name == expected_filename
    
    # Verify the plan name was properly replaced in the content
    assert f"# {plan_name.replace(' ', '_')}" in content
    
    # Verify other placeholders were replaced
    assert "__plan_name__" not in content
    assert "__editable_context__" not in content
    assert "__readonly_context__" not in content
    
    # Verify default values were inserted for context
    assert "./path/to/file.py" in content
    
    # Verify the file has the expected markdown structure based on the template
    assert "## High-Level Objective" in content
    assert "## Mid-Level Objective" in content
    assert "## Implementation Notes" in content
    assert "## Context" in content
    assert "### Editable context" in content
    assert "### Readonly context" in content
    assert "## Low-Level Tasks" in content
    assert "> Ordered from start to finish" in content


# ------ Self-build Tests ------


def test_spec_self_build_essentials(tmp_path):
    """Test self-build functionality with essential tasks"""
    plan_name = "test_self_build"
    spec_file_path = build_new_plan(plan_name, "list")
    final_spec_path = tmp_path / f"{plan_name}.yml"
    shutil.copy2(spec_file_path, final_spec_path)
    Path(spec_file_path).unlink()

    data = yaml.safe_load(final_spec_path.read_text())
    data["high_level_objective"] = "Create basic calculator"
    data["implementation_details"] = "Implement add, multiply and subtract functions"
    data["tasks"] = [
        {"title": "Create Add Function", "prompt": "CREATE add(a, b) -> int"},
    ]
    data["main_model"] = TESTING_MODEL
    data["editor_model"] = TESTING_MODEL
    data["editable_context"] = []
    data["readonly_context"] = []

    final_spec_path.write_text(yaml.safe_dump(data))

    run_spec_self_build(str(final_spec_path))

    updated_spec = parse_spec_file(str(final_spec_path))
    assert len(updated_spec.tasks) > 1
    assert any("add" in (task.title or "").lower() for task in updated_spec.tasks)
    assert any("subtract" in (task.title or "").lower() for task in updated_spec.tasks)
    assert any("multiply" in (task.title or "").lower() for task in updated_spec.tasks)

    # Verify each task has required fields
    for task in updated_spec.tasks:
        assert task.title, "Task missing title"
        assert task.prompt, "Task missing prompt"
