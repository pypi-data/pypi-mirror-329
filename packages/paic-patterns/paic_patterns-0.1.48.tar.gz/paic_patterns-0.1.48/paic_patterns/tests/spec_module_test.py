import pytest
from unittest import mock
from pathlib import Path
from ..modules.spec_module import (
    REFLECTION_PROMPT_PREFIX,
    ai_code,
    ping_ai_intelligence,
    spec_file_to_load_file,
    build_ai_coding_assistant,
    build_new_plan,
    spec_file_to_aider_instance,
    parse_aider_context_file,
    replace_context_in_template,
)
from ..modules.data_types import PreparedPrompt
from ..modules.data_types import (
    AICodeParams,
    ModeEnum,
    PaicPatternEnum,
    SpecFileList,
    SpecFileListReflection,
    SpecTask,
    SpecTaskReflection,
    ReasoningEffortV1,
)
import yaml
from ..modules.aider_llm_models import TESTING_MODEL
from ..modules.spec_module import build_prompt_list, build_prompt_list_reflection


@pytest.mark.parametrize(
    "task_count,from_task_number,expected_error",
    [
        (3, None, None),  # Base case - no task number specified
        (3, 0, "Invalid task number; it must be an integer greater than or equal to 1."),  # Less than 1
        (3, 4, "Invalid task number; it must be less than or equal to the total number of tasks in the spec."),  # Greater than task count
    ],
)
def test_validate_task_number(task_count, from_task_number, expected_error):
    """Test validate_task_number with different task numbers and edge cases."""
    from ..modules.spec_module import validate_task_number
    from ..modules.data_types import SpecFileList, SpecTask

    # Create a spec with the specified number of tasks
    spec = SpecFileList(
        plan_name="test_plan",
        pattern="list",
        architect=False,
        main_model="test-model",
        editor_model="test-model",
        editable_context=[],
        readonly_context=[],
        tasks=[SpecTask(title=f"Task {i}", prompt=f"Do task {i}") for i in range(task_count)]
    )

    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            validate_task_number(spec, from_task_number)
    else:
        # Should not raise any exception
        validate_task_number(spec, from_task_number)


def test_ai_code_coder_mode(tmp_path):
    # Create a temporary python file with initial content
    test_file = tmp_path / "hello.py"
    test_file.write_text("# Initial content\n")

    # Setup test parameters
    params = AICodeParams(
        architect=False,
        prompt="Write a hello_world() function in Python",
        model=TESTING_MODEL,
        editor_model=None,
        editable_context=[str(test_file)],
        readonly_context=[],
        settings={
            "auto_commits": False,
            "suggest_shell_commands": False,
            "detect_urls": False,
        },
    )

    # Create coder instance
    coder = build_ai_coding_assistant(params)

    # Run the function with both coder and params
    ai_code(coder, params)

    # Verify the file was modified
    content = test_file.read_text()
    assert "def hello_world():" in content
    assert "print" in content


def test_spec_file_to_load_file(tmp_path):
    # Create dummy spec file with context files
    spec_path = tmp_path / "test_spec.yaml"
    editable1 = tmp_path / "file1.py"
    editable2 = tmp_path / "file2.py"
    readonly1 = tmp_path / "README.md"
    readonly2 = tmp_path / "docs.md"

    # Create dummy files
    editable1.touch()
    editable2.touch()
    readonly1.touch()
    readonly2.touch()

    # Create spec data
    spec_data = SpecFileList(
        plan_name="test_spec",
        pattern=PaicPatternEnum.list,
        architect=False,
        main_model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        editable_context=[str(editable1), str(editable2)],
        readonly_context=[str(readonly1), str(readonly2)],
        tasks=[],
    )
    spec_path.write_text(yaml.safe_dump(spec_data.model_dump(mode="json")))

    # Generate the load file
    load_file_path = spec_file_to_load_file(str(spec_path))
    load_content = Path(load_file_path).read_text().splitlines()

    # Verify structure
    assert load_content[0] == "/drop"
    assert load_content[1] == f"/add       {editable1}"
    assert load_content[2] == f"/add       {editable2}"
    assert load_content[3] == f"/read-only {readonly1}"
    assert load_content[4] == f"/read-only {readonly2}"

    # Verify counts
    assert sum(1 for line in load_content if line.startswith("/drop")) == 1
    assert sum(1 for line in load_content if line.startswith("/add")) == 2
    assert sum(1 for line in load_content if line.startswith("/read-only")) == 2


def test_ai_code_architect_mode(tmp_path):
    # Create a temporary python file with initial content
    test_file = tmp_path / "hello.py"
    test_file.write_text("# Initial content\n")

    # Setup test parameters for architect mode
    params = AICodeParams(
        architect=True,
        prompt="Write a hello_world() function in Python",
        model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        editable_context=[str(test_file)],
        readonly_context=[],
        settings={
            "auto_commits": False,
            "suggest_shell_commands": False,
            "detect_urls": False,
        },
    )

    # Create coder instance
    coder = build_ai_coding_assistant(params)

    # Run the architect mode implementation
    ai_code(coder, params)

    # Verify the file was modified as expected
    content = test_file.read_text()
    assert "def hello_world():" in content
    assert "print" in content


@pytest.mark.parametrize(
    "plan_name,expected_filename",
    [
        ("my_spec", "my_spec.yml"),
        ("already_yaml.yaml", "already_yaml.yaml"),
        ("already_yml.yml", "already_yml.yml"),
        ("dir/my_spec", "dir/my_spec.yml"),
        ("path/to/spec", "path/to/spec.yml"),
        ("deeply/nested/path/feature", "deeply/nested/path/feature.yml"),
    ],
)
def test_build_new_plan_filename(tmp_path, plan_name, expected_filename):
    # Build spec in tmp directory
    spec_file_path = build_new_plan(str(tmp_path / plan_name), "list")
    assert plan_name in str(spec_file_path)

    # 1. Compare the entire filename (base + extension)
    assert Path(spec_file_path).name == Path(expected_filename).name, (
        f"Filename mismatch:\n"
        f"  Actual: {Path(spec_file_path).name}\n"
        f"  Expected: {Path(expected_filename).name}"
    )

    # 2. (Optional) Compare the full relative path from tmp_path, if you
    #    want to ensure that directory structure also matches.
    #    This ensures 'dir/my_spec.yml' vs. 'path/to/spec.yml' are correct.
    assert Path(spec_file_path).relative_to(tmp_path) == Path(expected_filename), (
        f"Path mismatch:\n"
        f"  Actual: {Path(spec_file_path).relative_to(tmp_path)}\n"
        f"  Expected: {Path(expected_filename)}"
    )

    # Load and verify the created spec
    with open(spec_file_path) as f:
        spec_data = yaml.safe_load(f)

    assert spec_data["plan_name"] == Path(spec_file_path).stem
    assert spec_data["pattern"] == "list"
    assert spec_data["editable_context"] == ["./path/to/file.py"]
    assert spec_data["readonly_context"] == ["./path/to/file.py"]


def test_build_new_plan_with_context_file(tmp_path):
    """Test creating new plan with context file"""
    # Create a test context file
    context_file = tmp_path / ".aider-context"
    context_content = """
/add       src/file1.py
/add       src/file2.py
/read-only  docs/readme.md
"""
    context_file.write_text(context_content)

    # Create new plan with context file
    plan_path = build_new_plan(
        str(tmp_path / "test_plan"), "list", context_file=str(context_file)
    )

    # Load and verify the created spec
    with open(plan_path) as f:
        spec_data = yaml.safe_load(f)

    assert len(spec_data["editable_context"]) == 2
    assert "src/file1.py" in spec_data["editable_context"]
    assert "src/file2.py" in spec_data["editable_context"]

    assert len(spec_data["readonly_context"]) == 1
    assert "docs/readme.md" in spec_data["readonly_context"]


def test_ai_code_with_directory_context(tmp_path):
    # Create a math directory with multiple Python files
    math_dir = tmp_path / "math"
    math_dir.mkdir()

    # Create multiple Python files with initial content
    files = {
        "add.py": "# Initial add content\n",
        "subtract.py": "# Initial subtract content\n",
        "multiply.py": "# Initial multiply content\n",
        "divide.py": "# Initial divide content\n",
    }

    # Create files and collect their paths
    file_paths = []
    for fname, content in files.items():
        file_path = math_dir / fname
        file_path.write_text(content)
        file_paths.append(str(file_path.absolute()))  # Use absolute paths

    # Setup test parameters using absolute file paths
    params = AICodeParams(
        architect=True,
        prompt="""Implement these math functions:
        - add.py: function add(a, b) that returns a + b
        - subtract.py: function subtract(a, b) that returns a - b
        - multiply.py: function multiply(a, b) that returns a * b
        - divide.py: function divide(a, b) that returns a / b""",
        model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        editable_context=file_paths,
        readonly_context=[],
        settings={
            "auto_commits": False,
            "suggest_shell_commands": False,
            "detect_urls": False,
        },
    )

    # Create coder instance
    coder = build_ai_coding_assistant(params)

    # Run the AI coding
    ai_code(coder, params)

    # Verify each file was modified with appropriate function using absolute paths
    assert "def add(a, b):" in (math_dir / "add.py").read_text()
    assert "return a + b" in (math_dir / "add.py").read_text()

    assert "def subtract(a, b):" in (math_dir / "subtract.py").read_text()
    assert "return a - b" in (math_dir / "subtract.py").read_text()

    assert "def multiply(a, b):" in (math_dir / "multiply.py").read_text()
    assert "return a * b" in (math_dir / "multiply.py").read_text()

    assert "def divide(a, b):" in (math_dir / "divide.py").read_text()
    assert "return a / b" in (math_dir / "divide.py").read_text()


@pytest.mark.parametrize(
    "spec_data,expected_sections",
    [
        # Test case 1: All sections present
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": "Create math functions",
                "implementation_details": "Use Python",
                "tasks": [{"title": "Add", "prompt": "Write add function"}],
            },
            [
                "# Plan: 'test_plan'",
                "",
                "## Instructions",
                "- You are an expert software engineer.",
                "- You're building a new feature task by task based on a complete spec aka plan.",
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.",
                "- You'll be given a task, and you'll need to write the code to complete the task.",
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.",
                "- The key is to generate the code that satisfies the task.",
                "",
                "## High Level Objective",
                "Create math functions",
                "",
                "## Implementation Details",
                "Use Python",
                "",
                "## Task: 'Add'",
                "Write add function",
            ],
        ),
        # Test case 2: Optional sections missing
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": None,
                "implementation_details": None,
                "tasks": [{"title": "", "prompt": "Write function"}],
            },
            [
                "# Plan: 'test_plan'",
                "",
                "## Instructions",
                "- You are an expert software engineer.",
                "- You're building a new feature task by task based on a complete spec aka plan.",
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.",
                "- You'll be given a task, and you'll need to write the code to complete the task.",
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.",
                "- The key is to generate the code that satisfies the task.",
                "",
                "## Task:",
                "Write function",
            ],
        ),
    ],
)
def test_section_spacing(spec_data, expected_sections):
    """Test that sections are properly separated by two newlines in build_prompt_list"""
    spec = SpecFileList(
        plan_name=spec_data["plan_name"],
        pattern="list",
        architect=True,
        main_model="dummy-model",
        editor_model="dummy-model",
        editable_context=[],
        readonly_context=[],
        high_level_objective=spec_data.get("high_level_objective"),
        implementation_details=spec_data.get("implementation_details"),
        tasks=[SpecTask(**t) for t in spec_data["tasks"]],
    )
    prepared = build_prompt_list(spec)
    assert len(prepared) == 1
    
    # Split the prompt into sections and verify spacing
    sections = prepared[0].prompt.strip().split("\n")
    assert sections == expected_sections


@pytest.mark.parametrize(
    "spec_data,expected_sections,expected_reflection_count",
    [
        # Test case 1: All sections present with multiple reflections
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": "Create math functions",
                "implementation_details": "Use Python",
                "tasks": [{
                    "title": "Add",
                    "prompt": "Write add function",
                    "reflection_count": 2,
                    "reflection_prompt_prefix": "Custom reflection prefix"
                }],
            },
            [
                "# Plan: 'test_plan'",
                "",
                "## Instructions",
                "- You are an expert software engineer.",
                "- You're building a new feature task by task based on a complete spec aka plan.",
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.",
                "- You'll be given a task, and you'll need to write the code to complete the task.",
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.",
                "- The key is to generate the code that satisfies the task.",
                "",
                "## High Level Objective",
                "Create math functions",
                "",
                "## Implementation Details",
                "Use Python",
                "",
                "## Task: 'Add'",
                "Write add function"
            ],
            2  # Expected number of reflection prompts
        ),
        # Test case 2: Optional sections missing, default reflection count
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": None,
                "implementation_details": None,
                "tasks": [{
                    "title": "",
                    "prompt": "Write function",
                    "reflection_count": None
                }],
            },
            [
                "# Plan: 'test_plan'",
                "",
                "## Instructions",
                "- You are an expert software engineer.",
                "- You're building a new feature task by task based on a complete spec aka plan.",
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.",
                "- You'll be given a task, and you'll need to write the code to complete the task.",
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.",
                "- The key is to generate the code that satisfies the task.",
                "",
                "## Task:",
                "Write function"
            ],
            1  # Default reflection count
        ),
    ],
)
def test_reflection_section_spacing(spec_data, expected_sections, expected_reflection_count):
    """Test that sections are properly separated by two newlines in build_prompt_list_reflection and verifies reflection count behavior"""
    spec = SpecFileListReflection(
        plan_name=spec_data["plan_name"],
        pattern="list",
        architect=True,
        main_model="dummy-model",
        editor_model="dummy-model",
        editable_context=[],
        readonly_context=[],
        high_level_objective=spec_data.get("high_level_objective"),
        implementation_details=spec_data.get("implementation_details"),
        tasks=[SpecTaskReflection(**t) for t in spec_data["tasks"]],
    )
    prepared = build_prompt_list_reflection(spec)
    
    # First prompt should match the original format
    assert len(prepared) == 1 + expected_reflection_count  # Original + reflection prompts
    sections = prepared[0].prompt.strip().split("\n")
    assert sections == expected_sections
    
    # Verify reflection prompts
    for i in range(expected_reflection_count):
        reflection_prompt = prepared[i + 1].prompt
        prefix = spec_data["tasks"][0].get("reflection_prompt_prefix", REFLECTION_PROMPT_PREFIX)
        assert reflection_prompt.startswith(prefix + "\n\n")
        reflection_sections = reflection_prompt.strip().split("\n")[2:]  # Skip prefix and empty line
        assert reflection_sections == expected_sections
    spec = SpecFileList(
        plan_name=spec_data["plan_name"],
        pattern="list",
        architect=True,
        main_model="dummy-model",
        editor_model="dummy-model",
        editable_context=[],
        readonly_context=[],
        high_level_objective=spec_data.get("high_level_objective"),
        implementation_details=spec_data.get("implementation_details"),
        tasks=[SpecTask(**t) for t in spec_data["tasks"]],
    )
    prepared = build_prompt_list(spec)
    assert len(prepared) == 1
    
    # Split the prompt into sections and verify spacing
    sections = prepared[0].prompt.strip().split("\n")
    assert sections == expected_sections


@pytest.mark.parametrize(
    "spec_data,expected_prompts",
    [
        # Case 1: Single task, with both high level objective and implementation details present.
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": "Create math functions",
                "implementation_details": "Use Python",
                "tasks": [{"title": "Add", "prompt": "Write add function"}],
            },
            [
                "# Plan: 'test_plan'\n\n"
                "## Instructions\n"
                "- You are an expert software engineer.\n"
                "- You're building a new feature task by task based on a complete spec aka plan.\n"
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.\n"
                "- You'll be given a task, and you'll need to write the code to complete the task.\n"
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.\n"
                "- The key is to generate the code that satisfies the task.\n"
                "\n\n## High Level Objective\nCreate math functions"
                "\n\n\n## Implementation Details\nUse Python"
                "\n\n\n## Task: 'Add'\n"
                "Write add function\n\n\n"
            ],
        ),
        # Case 2: Multiple tasks. Only the first task includes "## Implementation Details".
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": "Create math functions",
                "implementation_details": "Use Python",
                "tasks": [
                    {"title": "Add", "prompt": "Write add function"},
                    {"title": "Subtract", "prompt": "Write subtract function"},
                ],
            },
            [
                "# Plan: 'test_plan'\n\n"
                "## Instructions\n"
                "- You are an expert software engineer.\n"
                "- You're building a new feature task by task based on a complete spec aka plan.\n"
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.\n"
                "- You'll be given a task, and you'll need to write the code to complete the task.\n"
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.\n"
                "- The key is to generate the code that satisfies the task.\n"
                "\n\n## High Level Objective\nCreate math functions"
                "\n\n## Implementation Details\nUse Python"
                "\n\n## Task: 'Add'\n"
                "Write add function\n\n",
                "# Plan: 'test_plan'\n\n"
                "## Instructions\n"
                "- You are an expert software engineer.\n"
                "- You're building a new feature task by task based on a complete spec aka plan.\n"
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.\n"
                "- You'll be given a task, and you'll need to write the code to complete the task.\n"
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.\n"
                "- The key is to generate the code that satisfies the task.\n"
                "\n\n## High Level Objective\nCreate math functions"
                "\n\n## Task: 'Subtract'\n"
                "Write subtract function\n\n",
            ],
        ),
        # Case 3: Missing high_level_objective
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": None,
                "implementation_details": "Use Python",
                "tasks": [{"title": "", "prompt": "Write function without title"}],
            },
            [
                "# Plan: 'test_plan'\n\n"
                "## Instructions\n"
                "- You are an expert software engineer.\n"
                "- You're building a new feature task by task based on a complete spec aka plan.\n"
                "- To inform your engineering, take the High Level Objective and Implementation Details into account if provided.\n"
                "- You'll be given a task, and you'll need to write the code to complete the task.\n"
                "- Focus your engineering efforts on the individual task at hand, use the high level objective and implementation details to inform your work, but don't let it overwhelm your focus.\n"
                "- The key is to generate the code that satisfies the task.\n"
                "\n\n## Implementation Details\nUse Python"
                "\n\n## Task:\n"
                "Write function without title\n\n"
            ],
        ),
    ],
)
def test_build_prompt_list(spec_data, expected_prompts):
    # Convert dict to SpecFileList instance
    spec = SpecFileList(
        plan_name=spec_data["plan_name"],
        pattern="list",
        architect=True,
        main_model="dummy-model",
        editor_model="dummy-model",
        editable_context=[],
        readonly_context=[],
        high_level_objective=spec_data.get("high_level_objective"),
        implementation_details=spec_data.get("implementation_details"),
        tasks=[SpecTask(**t) for t in spec_data["tasks"]],
    )
    prepared = build_prompt_list(spec)
    assert len(prepared) == len(expected_prompts)
    for i, prep in enumerate(prepared):
         assert isinstance(prep, PreparedPrompt)
         assert prep.prompt == expected_prompts[i]
         assert prep.task_number == i + 1
         assert prep.position_number == i


def test_spec_file_to_aider_instance_architect(tmp_path):
    # Create dummy context files
    spec_path = tmp_path / "architect_spec.yaml"
    editable_file = tmp_path / "math.py"

    # Write initial content to the editable file
    editable_file.write_text(
        """
def multiply(a, b):
    return a * b
"""
    )

    # Create spec data with architect=True and an additional task
    spec_data = SpecFileList(
        plan_name="architect_spec",
        pattern=PaicPatternEnum.list,
        architect=True,
        main_model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        editable_context=[str(editable_file)],
        readonly_context=[],
        high_level_objective="Enhance math operations",
        implementation_details="Add a magnitude function to the multiply operation.",
        tasks=[
            SpecTask(
                title="Enhance multiply function",
                prompt="Add a magnitude(number, mag) method that 10x's the number based on mag.",
            )
        ],
    )
    spec_path.write_text(yaml.safe_dump(spec_data.model_dump(mode="json")))

    # Mock os.execvp to prevent actual execution
    with mock.patch("os.execvp") as mock_execvp:
        spec_file_to_aider_instance(str(spec_path))

        # Verify that os.execvp was called with the correct arguments
        expected_args = [
            "aider",
            "--model",
            spec_data.main_model,
            "--editor-model",
            spec_data.editor_model,
            "--architect",
            "--load",
            spec_file_to_load_file(str(spec_path)),
            "--yes-always",
            "--no-auto-commit",
            "--no-suggest-shell-commands",
            "--no-detect-urls",
        ]
        mock_execvp.assert_called_once_with("aider", expected_args)


def test_spec_file_to_aider_instance_non_architect(tmp_path):
    # Create dummy context files
    spec_path = tmp_path / "non_architect_spec.yaml"
    editable_file = tmp_path / "math_non_architect.py"

    # Write initial content to the editable file
    editable_file.write_text(
        """
def multiply(a, b):
    return a * b
"""
    )

    # Create spec data with architect=False and an additional task
    spec_data = SpecFileList(
        plan_name="non_architect_spec",
        pattern=PaicPatternEnum.list,
        architect=False,
        main_model=TESTING_MODEL,
        editor_model=None,  # editor_model is not used when architect=False
        editable_context=[str(editable_file)],
        readonly_context=[],
        high_level_objective="Enhance math operations without architecture",
        implementation_details="Add a magnitude function to the multiply operation.",
        tasks=[
            SpecTask(
                title="Enhance multiply function",
                prompt="Add a magnitude(number, mag) method that 10x's the number based on mag.",
            )
        ],
    )
    spec_path.write_text(yaml.safe_dump(spec_data.model_dump(mode="json")))

    # Mock os.execvp to prevent actual execution
    with mock.patch("os.execvp") as mock_execvp:
        spec_file_to_aider_instance(str(spec_path))

        # Verify that os.execvp was called with the correct arguments
        expected_args = [
            "aider",
            "--model",
            spec_data.main_model,
            "--load",
            spec_file_to_load_file(str(spec_path)),
            "--yes-always",
            "--no-auto-commit",
            "--no-suggest-shell-commands",
            "--no-detect-urls",
        ]
        mock_execvp.assert_called_once_with("aider", expected_args)


def test_parse_aider_context_file(tmp_path):
    """Test parsing of aider context files"""
    # Create a test context file
    context_file = tmp_path / ".aider-context"
    context_content = """
/drop
/add       src/file1.py
/add       src/file2.py
/add       src/file3.py
/read-only  docs/readme.md
/read-only  docs/api.md
/drop
/add       src/file4.py
/read-only  docs/contributing.md
"""
    context_file.write_text(context_content)

    # Parse the context file
    editable_context, readonly_context = parse_aider_context_file(str(context_file))

    # Verify editable context files
    assert len(editable_context) == 4
    assert "src/file1.py" in editable_context
    assert "src/file2.py" in editable_context
    assert "src/file3.py" in editable_context
    assert "src/file4.py" in editable_context

    # Verify readonly context files
    assert len(readonly_context) == 3
    assert "docs/readme.md" in readonly_context
    assert "docs/api.md" in readonly_context
    assert "docs/contributing.md" in readonly_context


def test_parse_aider_context_file_empty(tmp_path):
    """Test parsing empty context file"""
    context_file = tmp_path / ".aider-context"
    context_file.write_text("")

    editable_context, readonly_context = parse_aider_context_file(str(context_file))

    assert len(editable_context) == 0
    assert len(readonly_context) == 0


def test_parse_aider_context_file_only_drops(tmp_path):
    """Test parsing context file with only /drop commands"""
    context_file = tmp_path / ".aider-context"
    context_file.write_text(
        """
/drop
/drop
/drop
"""
    )

    editable_context, readonly_context = parse_aider_context_file(str(context_file))

    assert len(editable_context) == 0
    assert len(readonly_context) == 0


def test_parse_aider_context_file_invalid_lines(tmp_path):
    """Test parsing context file with invalid lines"""
    context_file = tmp_path / ".aider-context"
    context_file.write_text(
        """
invalid line
/add       src/file1.py
another invalid line
/read-only  docs/readme.md
/invalid    something.txt
"""
    )

    editable_context, readonly_context = parse_aider_context_file(str(context_file))

    assert len(editable_context) == 1
    assert "src/file1.py" in editable_context
    assert len(readonly_context) == 1
    assert "docs/readme.md" in readonly_context


@pytest.mark.parametrize(
    "template_content, context_content, expected_content",
    [
        (
            """editable_context: __editable_context__
readonly_context: __readonly_context__""",
            """
/add       src/file1.py
/read-only  docs/readme.md
""",
            """editable_context:
  - "src/file1.py"
readonly_context:
  - \"docs/readme.md\"""",
        ),
        (
            """editable_context: __editable_context__
readonly_context: __readonly_context__""",
            "",  # Empty context file
            """editable_context:
  - "./path/to/file.py"
readonly_context:
  - "./path/to/file.py\"""",
        ),
        (
            """editable_context: __editable_context__
readonly_context: __readonly_context__""",
            """
/add       src/file1.py
/add       src/file2.py
/read-only  docs/readme.md
/read-only  docs/api.md
""",
            """editable_context:
  - "src/file1.py"
  - "src/file2.py"
readonly_context:
  - "docs/readme.md"
  - "docs/api.md\"""",
        ),
    ],
)
def test_replace_context_in_template(
    tmp_path, template_content, context_content, expected_content
):
    # Create a temporary context file
    context_file = tmp_path / ".aider-context"
    context_file.write_text(context_content)

    # Call the function
    updated_content = replace_context_in_template(template_content, str(context_file))

    # Assert the content matches the expected result
    assert updated_content == expected_content


def test_build_ai_coding_assistant_with_reasoning_effort():
    """Test that reasoning_effort is properly passed through to model.extra_params"""
    from paic_patterns.modules.data_types import AICodeParams, ReasoningEffortV1
    from paic_patterns.modules.spec_module import build_ai_coding_assistant
    from paic_patterns.modules.aider_llm_models import TESTING_MODEL

    # Test with architect mode
    params = AICodeParams(
        architect=True,
        prompt="test prompt",
        model=TESTING_MODEL,
        editor_model=TESTING_MODEL,
        editable_context=[],
        readonly_context=[],
        settings={"reasoning_effort": ReasoningEffortV1.high},
    )
    coder = build_ai_coding_assistant(params)
    assert coder.main_model.extra_params == {"reasoning_effort": ReasoningEffortV1.high}

    # Test with non-architect mode
    params = AICodeParams(
        architect=False,
        prompt="test prompt",
        model=TESTING_MODEL,
        editor_model=None,
        editable_context=[],
        readonly_context=[],
        settings={"reasoning_effort": ReasoningEffortV1.low},
    )
    coder = build_ai_coding_assistant(params)
    assert coder.main_model.extra_params == {"reasoning_effort": ReasoningEffortV1.low}
