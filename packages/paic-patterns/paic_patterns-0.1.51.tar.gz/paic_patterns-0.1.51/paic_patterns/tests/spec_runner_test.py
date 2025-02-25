import pytest
import yaml
from pathlib import Path
from unittest import mock

from ..modules.aider_llm_models import TESTING_MODEL
from ..modules.spec_module import spec_file_to_aider_instance, spec_file_to_load_file
from ..modules.spec_module import (
    build_new_plan,
    parse_spec_file,
    replace_context_in_template,
    REFLECTION_PROMPT_PREFIX,
)
from ..modules.spec_runner import run_spec, run_spec_self_build


def test_run_spec(tmp_path):
    plan_name = "test_spec"
    # Create a new spec file in current working directory
    spec_file_path = build_new_plan(plan_name, "list")

    # Move it (or rewrite) into tmp_path so we can modify it safely
    final_spec_path = tmp_path / f"{plan_name}.yaml"
    Path(spec_file_path).rename(final_spec_path)

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

    # Assert or check that expected changes occurred (example placeholder)
    # For now, just ensure no exceptions and file remains
    assert final_spec_path.exists()

    assert "def add" in test_py.read_text().lower()
    assert "def multiply" in test_py.read_text().lower()
    assert "def subtract" in test_py.read_text().lower()
    assert "def divide" in test_py.read_text().lower()


def test_run_spec_architect_mode(tmp_path):
    plan_name = "test_spec_architect"
    spec_file_path = build_new_plan(plan_name, "list")
    final_spec_path = tmp_path / f"{plan_name}.yaml"
    Path(spec_file_path).rename(final_spec_path)

    data = yaml.safe_load(final_spec_path.read_text())
    data["architect"] = True  # Set to architect mode
    data["main_model"] = TESTING_MODEL
    data["editor_model"] = TESTING_MODEL
    data["tasks"] = [
        {"title": "Add", "prompt": "Write a function to add two numbers."},
        {"title": "Multiply", "prompt": "Write a function to multiply two numbers."},
    ]

    test_py = tmp_path / "architect_file.py"
    test_py.write_text("# initial architect content\n")
    data["editable_context"] = [str(test_py)]
    data["readonly_context"] = []

    final_spec_path.write_text(yaml.safe_dump(data))

    run_spec(str(final_spec_path))

    content = test_py.read_text().lower()
    assert "def add" in content
    assert "def multiply" in content


def test_run_spec_self_build(tmp_path):
    """Test the self-build functionality of spec runner"""
    plan_name = "test_spec_self_build"
    spec_file_path = build_new_plan(plan_name, "list")
    final_spec_path = tmp_path / f"{plan_name}.yaml"
    Path(spec_file_path).rename(final_spec_path)

    # Create initial spec data with math API implementation
    data = yaml.safe_load(final_spec_path.read_text())
    data["high_level_objective"] = "Build a simple math API with basic operations"
    data[
        "implementation_details"
    ] = """
    Create a math API with separate files for each operation:
    - add.py: Contains add function
    - subtract.py: Contains subtract function
    - multiply.py: Contains multiply function
    - divide.py: Contains divide function
    
    Each function should take two parameters and return the result.
    """

    # Add just the first task as template
    data["tasks"] = [
        {
            "title": "Create add function",
            "prompt": "Create add.py with a function that takes two parameters and returns their sum. The function should be named 'add' and use type hints.",
        }
    ]

    data["main_model"] = TESTING_MODEL
    data["editor_model"] = TESTING_MODEL
    data["editable_context"] = [str(final_spec_path)]

    # Write updated spec file
    final_spec_path.write_text(yaml.safe_dump(data))

    # Run self-build
    run_spec_self_build(str(final_spec_path))

    # Read and parse updated spec
    updated_spec = parse_spec_file(str(final_spec_path))

    # Verify more tasks were added
    assert len(updated_spec.tasks) > 1, "No new tasks were added"

    # Verify first task remains unchanged
    assert updated_spec.tasks[0].title == "Create add function"

    # Verify new tasks follow similar pattern and are related to math operations
    task_titles = [task.title.lower() if task.title else "" for task in updated_spec.tasks]
    expected_keywords = ["subtract", "multiply", "divide"]

    for keyword in expected_keywords:
        assert any(
            keyword in title for title in task_titles
        ), f"No task found for {keyword} operation"

    # Verify each task has a title and prompt
    for task in updated_spec.tasks:
        assert task.title, "Task missing title"
        assert task.prompt, "Task missing prompt"


def test_new_spec_with_context_file(tmp_path):
    """Test creating a new spec with a context file"""
    # Create a test context file
    context_file = tmp_path / ".aider-context"
    context_content = """
/drop
/add       src/file1.py
/add       src/file2.py
/add       src/file3.py
/read-only  docs/readme.md
/read-only  docs/api.md
"""
    context_file.write_text(context_content)

    # Create new spec with context file
    spec_path = build_new_plan(
        str(tmp_path / "test_plan"), "list", context_file=str(context_file)
    )

    # Load and verify the spec
    spec = parse_spec_file(spec_path)

    # Verify editable context
    assert len(spec.editable_context) == 3
    assert "src/file1.py" in spec.editable_context
    assert "src/file2.py" in spec.editable_context
    assert "src/file3.py" in spec.editable_context

    # Verify readonly context
    assert len(spec.readonly_context) == 2
    assert "docs/readme.md" in spec.readonly_context
    assert "docs/api.md" in spec.readonly_context


def test_new_spec_with_complex_context_file(tmp_path):
    """Test creating spec with complex context file including mixed order and duplicates"""
    context_file = tmp_path / ".aider-context"
    context_content = """
/drop
/add       src/file1.py
/read-only  docs/readme.md
/add       src/file2.py
/drop
/read-only  docs/api.md
/add       src/file1.py  # Duplicate entry
/read-only  docs/readme.md  # Duplicate entry
/invalid    something.txt
random line
/add       src/file3.py
"""
    context_file.write_text(context_content)

    spec_path = build_new_plan(
        str(tmp_path / "test_complex"), "list", context_file=str(context_file)
    )

    spec = parse_spec_file(spec_path)

    # Verify editable context (should deduplicate)
    assert len(spec.editable_context) == 3
    assert "src/file1.py" in spec.editable_context
    assert "src/file2.py" in spec.editable_context
    assert "src/file3.py" in spec.editable_context

    # Verify readonly context (should deduplicate)
    assert len(spec.readonly_context) == 2
    assert "docs/readme.md" in spec.readonly_context
    assert "docs/api.md" in spec.readonly_context


def test_new_spec_with_empty_context_file(tmp_path):
    """Test creating spec with empty context file"""
    context_file = tmp_path / ".aider-context"
    context_file.write_text("")

    spec_path = build_new_plan(
        str(tmp_path / "test_empty"), "list", context_file=str(context_file)
    )

    spec = parse_spec_file(spec_path)

    assert len(spec.editable_context) == 1
    assert len(spec.readonly_context) == 1


def test_new_spec_context_file_integration(tmp_path):
    """Test full integration flow with context file"""
    # Create context file
    context_file = tmp_path / ".aider-context"
    context_content = """
/add       src/math.py
/add       src/utils.py
/read-only  docs/readme.md
"""
    context_file.write_text(context_content)

    # Create spec with context
    spec_path = build_new_plan(
        str(tmp_path / "test_integration"), "list", context_file=str(context_file)
    )

    # Verify spec was created with correct contexts
    spec = parse_spec_file(spec_path)
    assert "src/math.py" in spec.editable_context
    assert "src/utils.py" in spec.editable_context
    assert "docs/readme.md" in spec.readonly_context

    # Generate load file from spec
    load_file_path = spec_file_to_load_file(spec_path)
    load_content = Path(load_file_path).read_text()

    # Verify load file contains correct entries
    assert "/add       src/math.py" in load_content
    assert "/add       src/utils.py" in load_content
    assert "/read-only docs/readme.md" in load_content


def test_run_spec_list_skipping_tasks(tmp_path):
    import yaml
    from pathlib import Path
    from paic_patterns.modules.spec_runner import run_spec
    from paic_patterns.modules.aider_llm_models import TESTING_MODEL

    # Create a temporary editable file (initially empty)
    test_file = tmp_path / "test_skip_list.py"
    test_file.write_text("")

    # Define the spec content with 4 tasks using our simple math examples.
    spec_content = {
        "plan_name": "skip_test",
        "pattern": "list",
        "architect": False,
        "main_model": TESTING_MODEL,
        "editor_model": TESTING_MODEL,
        "editable_context": [str(test_file)],
        "readonly_context": [],
        "high_level_objective": "Simple math operations",
        "implementation_details": "Implement basic math functions",
        "tasks": [
            {"title": "Add", "prompt": "Write `def add(...)` function"},
            {"title": "Multiply", "prompt": "Write `def multiply(...)` function"},
            {"title": "Subtract", "prompt": "Write `def subtract(...)` function"},
            {"title": "Divide", "prompt": "Write `def divide(...)` function"},
        ],
    }
    # Write the spec YAML to a file.
    spec_file = tmp_path / "spec_skip_list.yaml"
    spec_file.write_text(yaml.safe_dump(spec_content))

    # Run the spec with from_task_number set to 3 so that tasks 1 and 2 are skipped.
    run_spec(str(spec_file), from_task_number=3)

    # Read the content of the updated editable file.
    content = test_file.read_text().lower()
    # Assert that only tasks 3 and 4 (Subtract and Divide) were processed.
    assert "def subtract" in content, "Expected subtract function in output"
    assert "def divide" in content, "Expected divide function in output"
    assert "def add" not in content, "Did not expect add function in output"
    assert "def multiply" not in content, "Did not expect multiply function in output"


def test_run_spec_list_reflection_skipping_tasks(tmp_path):
    import yaml
    from pathlib import Path
    from paic_patterns.modules.spec_runner import run_spec
    from paic_patterns.modules.aider_llm_models import TESTING_MODEL

    # Create a temporary editable file for the reflection spec.
    test_file = tmp_path / "test_skip_reflection.py"
    test_file.write_text("")

    # Define the spec content with pattern "list-reflection".
    # For simplicity, set reflection_count=0 so each task gives just one prompt.
    spec_content = {
        "plan_name": "skip_reflection_test",
        "pattern": "list-reflection",
        "architect": False,
        "main_model": TESTING_MODEL,
        "editor_model": TESTING_MODEL,
        "editable_context": [str(test_file)],
        "readonly_context": [],
        "high_level_objective": "Simple math operations",
        "implementation_details": "Implement basic math functions",
        "tasks": [
            {"title": "Add", "prompt": "Write add function", "reflection_count": 1},
            {
                "title": "Multiply",
                "prompt": "Write multiply function",
                "reflection_count": 1,
            },
            {
                "title": "Subtract",
                "prompt": "Write subtract function",
                "reflection_count": 1,
            },
            {
                "title": "Divide",
                "prompt": "Write divide function",
                "reflection_count": 1,
            },
        ],
    }
    # Write the spec YAML to a file.
    spec_file = tmp_path / "spec_skip_reflection.yaml"
    spec_file.write_text(yaml.safe_dump(spec_content))

    # Run the spec with from_task_number set to 3 so that only tasks 3 and 4 are processed.
    run_spec(str(spec_file), from_task_number=3)

    # Read the content of the updated editable file.
    content = test_file.read_text().lower()
    # Assert that only tasks 3 and 4 (Subtract and Divide) were executed.
    assert "def subtract" in content, "Expected subtract function in output"
    assert "def divide" in content, "Expected divide function in output"
    assert "def add" not in content, "Did not expect add function in output"
    assert "def multiply" not in content, "Did not expect multiply function in output"


def test_build_prompt_list_reflection():
    """
    Validate build_prompt_list_reflection generates the correct number and ordering
    of prompts from tasks with various reflection_count values.

    - For each task, the original prompt should be followed immediately
      by the appropriate number of reflection prompts.
    - Reflection prompts should contain the reflection_prompt_prefix immediately
      before the original task prompt.
    - Edge cases for reflection_count (0, None, >2) are handled properly.
    """
    from paic_patterns.modules.spec_module import build_prompt_list_reflection
    from paic_patterns.modules.data_types import (
        SpecFileListReflection,
        SpecTaskReflection,
        PreparedPrompt,
    )

    # Define tasks with different reflection counts.
    tasks = [
        # Task 1: reflection_count explicitly set to 1.
        SpecTaskReflection(
            title="Task One",
            prompt="Prompt One",
            reflection_count=1,
            reflection_prompt_prefix="REVIEW: ",
        ),
        # Task 2: reflection_count set to 0 (or could be None to test default behavior).
        SpecTaskReflection(
            title="Task Two",
            prompt="Prompt Two",
            reflection_count=0,
            reflection_prompt_prefix="REVIEW: ",
        ),
        # Task 3: reflection_count set to 2 with a different prefix.
        SpecTaskReflection(
            title="Task Three",
            prompt="Prompt Three",
            reflection_count=2,
            reflection_prompt_prefix="CHECK: ",
        ),
    ]
    # Create a spec instance using the reflection type.
    spec = SpecFileListReflection(
        plan_name="Test Reflection",
        pattern="list-reflection",
        architect=False,
        main_model="dummy-model",
        editor_model="dummy-model",
        editable_context=[],
        readonly_context=[],
        high_level_objective="High Level Objective",
        implementation_details="Implementation Details",
        tasks=tasks,
    )

    # Invoke the reflection prompt builder.
    prepared_prompts = build_prompt_list_reflection(spec)
    assert (
        len(prepared_prompts) == 6
    ), f"Expected 6 prepared prompts but got {len(prepared_prompts)}"
    # Verify type and ordering
    for p in prepared_prompts:
        assert isinstance(p, PreparedPrompt)
    # Verify ordering and prompt content
    assert "Prompt One" in prepared_prompts[0].prompt
    assert prepared_prompts[1].prompt.startswith("REVIEW:")
    assert "Prompt One" in prepared_prompts[1].prompt
    assert "Prompt Two" in prepared_prompts[2].prompt
    assert "Prompt Three" in prepared_prompts[3].prompt
    # Verify task numbers and positions
    expected_task_numbers = [1, 1, 2, 3, 3, 3]
    expected_positions = list(range(6))
    assert [p.task_number for p in prepared_prompts] == expected_task_numbers
    assert [p.position_number for p in prepared_prompts] == expected_positions


def test_parse_spec_file(tmp_path):
    """
    Validate that YAML specs are parsed correctly based on the 'pattern' field.

    - When the spec declares 'pattern: list', parse_spec_file returns a SpecFileList.
    - When the spec declares 'pattern: list-reflection', parse_spec_file returns a SpecFileListReflection.
    - Fields from the YAML are correctly populated.
    - For an invalid pattern, no reflection conversion is made.
    """
    import yaml
    from paic_patterns.modules.spec_module import parse_spec_file
    from paic_patterns.modules.data_types import (
        SpecFileList,
        SpecFileListReflection,
        PaicPatternEnum,
    )

    # Prepare a YAML spec for the 'list' pattern.
    spec_content_list = {
        "plan_name": "List Spec",
        "pattern": "list",
        "architect": False,
        "main_model": "dummy",
        "editor_model": "dummy",
        "editable_context": ["file.py"],
        "readonly_context": [],
        "high_level_objective": "Objective",
        "implementation_details": "Details",
        "tasks": [{"title": "Task", "prompt": "Do something"}],
    }
    list_file = tmp_path / "list_spec.yaml"
    list_file.write_text(yaml.safe_dump(spec_content_list))
    spec_list = parse_spec_file(str(list_file))
    # Expect type SpecFileList (not reflection)
    assert isinstance(spec_list, SpecFileList)
    assert spec_list.pattern == PaicPatternEnum.list

    # Now a YAML spec for the 'list-reflection' pattern.
    spec_content_reflection = {
        "plan_name": "Reflection Spec",
        "pattern": "list-reflection",
        "architect": False,
        "main_model": "dummy",
        "editor_model": "dummy",
        "editable_context": ["file.py"],
        "readonly_context": [],
        "high_level_objective": "Objective",
        "implementation_details": "Details",
        "tasks": [
            {
                "title": "Task",
                "prompt": "Do something",
                "reflection_count": 1,
                "reflection_prompt_prefix": "REVIEW: ",
            }
        ],
    }
    reflection_file = tmp_path / "reflection_spec.yaml"
    reflection_file.write_text(yaml.safe_dump(spec_content_reflection))
    spec_reflection = parse_spec_file(str(reflection_file))
    # Expect conversion to SpecFileListReflection.
    assert isinstance(spec_reflection, SpecFileListReflection)
    assert spec_reflection.pattern == PaicPatternEnum.list_reflection

    # Test an invalid pattern: it should remain as given (no conversion occurs).
    spec_content_invalid = spec_content_list.copy()
    spec_content_invalid["pattern"] = "invalid"
    invalid_file = tmp_path / "invalid_spec.yaml"
    invalid_file.write_text(yaml.safe_dump(spec_content_invalid))
    spec_invalid = parse_spec_file(str(invalid_file))
    # Since conversion only happens for list-reflection, invalid remains as base type.
    assert not isinstance(spec_invalid, SpecFileListReflection)
    assert spec_invalid.pattern == "invalid"


def test_run_spec_list(tmp_path):
    """
    Test that a spec file with pattern 'list' (non-reflection) processes
    exactly one prompt per task and modifies the editable file.
    """
    import yaml
    from paic_patterns.modules.aider_llm_models import TESTING_MODEL
    from paic_patterns.modules.spec_runner import run_spec

    # Create a temporary file to serve as the editable context
    test_file = tmp_path / "test_list.py"
    test_file.write_text("")  # start with an empty file

    # Create spec content with pattern 'list' and include the editable file
    spec_content = {
        "plan_name": "test_list",
        "pattern": "list",
        "architect": False,
        "main_model": TESTING_MODEL,
        "editor_model": TESTING_MODEL,
        "editable_context": [str(test_file)],
        "readonly_context": [],
        "high_level_objective": "Simple math functions",
        "implementation_details": "Each function should perform a basic math operation",
        "tasks": [
            {"title": "Add", "prompt": "Write add function"},
            {"title": "Multiply", "prompt": "Write multiply function"},
            {"title": "Subtract", "prompt": "Write subtract function"},
        ],
    }
    spec_file = tmp_path / "spec_list.yaml"
    spec_file.write_text(yaml.safe_dump(spec_content))

    # Call the real run_spec
    run_spec(str(spec_file))

    # Now, open the editable file and check that it was updated
    content = test_file.read_text().lower()
    # Here, we assume that the dummy coder produces code containing the function definitions
    assert "def add" in content
    assert "def multiply" in content
    assert "def subtract" in content


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
