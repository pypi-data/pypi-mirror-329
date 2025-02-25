import yaml
import pytest
from pathlib import Path
from pydantic import ValidationError
from paic_patterns.modules.spec_templates import (
    template_spec_file_list,
    template_spec_file_list_reflection,
    template_spec_file_markdown,
)
from paic_patterns.modules.spec_module import build_new_plan
from paic_patterns.modules.data_types import SpecFileList, SpecFileListReflection


# Helper function to fill in placeholders in a template
def fill_template(template_str: str) -> str:
    # Replace required placeholders with dummy values.
    return (
        template_str.replace("__plan_name__", "dummy")
        .replace("__main_model__", "dummy-main")
        .replace("__editor_model__", "dummy-editor")
        .replace("__editable_context__", '\n  - "./path/to/file.py"')
        .replace("__readonly_context__", '\n  - "./path/to/file.py"')
    )


def test_template_spec_file_list():
    """
    Validate the default non-reflection template:
      - It has exactly 3 tasks.
      - Each task has the required keys (title and prompt).
      - The YAML produces a valid SpecFileList instance.
    """
    filled = fill_template(template_spec_file_list)
    data = yaml.safe_load(filled)
    # Validate that basic fields exist
    assert "plan_name" in data
    assert "pattern" in data and data["pattern"] == "list"
    assert "tasks" in data and isinstance(data["tasks"], list)
    assert (
        len(data["tasks"]) == 3
    ), "There should be exactly 3 tasks in the default template"
    for task in data["tasks"]:
        assert "title" in task
        assert "prompt" in task
        # The non-reflection tasks should not have reflection fields
        assert "reflection_count" not in task
        assert "reflection_prompt_prefix" not in task
    # Validate that the model can be instantiated from the data.
    spec = SpecFileList(**data)
    assert spec.plan_name == "dummy"


def test_template_spec_file_list_reflection():
    """
    Validate the reflection template:
      - It has exactly 3 tasks.
      - Each task has the extra fields: reflection_count and reflection_prompt_prefix.
      - The reflection_prompt_prefix defaults to the expected message.
      - The YAML produces a valid SpecFileListReflection instance.
    """
    filled = fill_template(template_spec_file_list_reflection)
    data = yaml.safe_load(filled)
    # Validate that the pattern is set to list-reflection
    assert "pattern" in data and data["pattern"] == "list-reflection"
    # Validate tasks presence and structure
    assert "tasks" in data and isinstance(data["tasks"], list)
    assert (
        len(data["tasks"]) == 3
    ), "There should be exactly 3 tasks in the reflection template"
    for task in data["tasks"]:
        assert "title" in task
        assert "prompt" in task
        assert (
            "reflection_count" in task
        ), "Each reflection task must have reflection_count"
        assert task["reflection_count"] == 1
        # The default template NO LONGER includes a reflection_prompt_prefix key.
        assert (
            "reflection_prompt_prefix" not in task
        ), "reflection_prompt_prefix should not be in raw YAML template"

    spec = SpecFileListReflection(**data)
    assert spec.pattern == "list-reflection"


def test_template_spec_file_markdown():
    """
    Test the markdown template:
    - Verify it contains the required placeholders
    - Verify the structure matches the expected format
    """
    # Test the raw template string
    assert "__plan_name__" in template_spec_file_markdown
    assert "__editable_context__" in template_spec_file_markdown
    assert "__readonly_context__" in template_spec_file_markdown
    
    # Verify key sections are present
    assert "# __plan_name__" in template_spec_file_markdown
    assert "## High-Level Objective" in template_spec_file_markdown
    assert "## Mid-Level Objective" in template_spec_file_markdown
    assert "## Implementation Notes" in template_spec_file_markdown
    assert "## Context" in template_spec_file_markdown
    assert "### Editable context" in template_spec_file_markdown
    assert "### Readonly context" in template_spec_file_markdown
    assert "## Low-Level Tasks" in template_spec_file_markdown


def test_build_new_plan_markdown_pattern(tmp_path):
    """Test creating a new markdown spec file"""
    # Test creating a new markdown spec file
    spec_path = tmp_path / "test_spec"
    filename = build_new_plan(str(spec_path), "markdown")
    
    # Verify the file was created with .md extension
    assert filename.endswith(".md")
    
    # Read the file content
    content = Path(filename).read_text()
    
    # Verify the template sections are properly replaced
    assert "# test_spec" in content  # __plan_name__ should be replaced
    assert "./path/to/file.py" in content  # default context path
    
    # Verify key sections are present
    assert "## High-Level Objective" in content
    assert "## Mid-Level Objective" in content
    assert "## Implementation Notes" in content
    assert "## Context" in content
    assert "### Editable context" in content
    assert "### Readonly context" in content
    assert "## Low-Level Tasks" in content


def test_build_new_plan_markdown_pattern_with_context(tmp_path):
    """Test creating a new markdown spec file with context"""
    # Create a mock context file
    context_file = tmp_path / ".aider-context"
    context_file.write_text("""
/add       src/file1.py
/read-only docs/readme.md
""")
    
    # Test creating a new markdown spec file with context
    spec_path = tmp_path / "test_spec"
    filename = build_new_plan(str(spec_path), "markdown", context_file=str(context_file))
    
    # Read the file content
    content = Path(filename).read_text()
    
    # Verify the context was properly replaced
    assert 'src/file1.py' in content
    assert 'docs/readme.md' in content


def test_spec_run_markdown_file(tmp_path):
    """Test that running a markdown file raises an error"""
    from paic_patterns.commands.spec_commands import run
    import typer
    
    # Create a test markdown file
    test_file = tmp_path / "test_spec.md"
    test_file.write_text("# Test Spec")
    
    # Verify that trying to run the markdown file raises an error
    with pytest.raises(typer.Exit):
        run(str(test_file))


def test_template_compatibility():
    """
    Ensure both templates share a consistent base structure:
      - The common fields (plan_name, architect, main_model, etc.) have identical keys.
      - The non-reflection template tasks do NOT include reflection fields.
      - The reflection template tasks include the extra reflection fields.
    """
    filled_list = fill_template(template_spec_file_list)
    filled_reflection = fill_template(template_spec_file_list_reflection)
    data_list = yaml.safe_load(filled_list)
    data_reflection = yaml.safe_load(filled_reflection)
    # Compare common fields at the root level
    common_fields = [
        "plan_name",
        "architect",
        "main_model",
        "editor_model",
        "editable_context",
        "readonly_context",
        "high_level_objective",
        "implementation_details",
    ]
    for field in common_fields:
        assert (
            field in data_list and field in data_reflection
        ), f"The field '{field}' should appear in both templates"
        # (The actual values may differ due to default strings; we check existence.)
    # Check tasks length consistency
    assert len(data_list.get("tasks", [])) == len(data_reflection.get("tasks", [])) == 3
    # Validate tasks differences
    for task_list, task_refl in zip(data_list["tasks"], data_reflection["tasks"]):
        # In the base template, keys should be exactly title and prompt (apart from any formatting)
        for key in task_list.keys():
            assert key in [
                "title",
                "prompt",
            ], f"Non-reflection task should only contain 'title' and 'prompt', found {key}"
        # In the reflection template, extra keys must be present.
        assert (
            "reflection_count" in task_refl
        ), "Reflection task missing key: reflection_count"
        # The reflection template should not include a reflection_prompt_prefix key in raw YAML.
        assert (
            "reflection_prompt_prefix" not in task_refl
        ), "reflection_prompt_prefix should not be in raw YAML for reflection template"
    # Finally, ensure instantiation works for both models
    try:
        _ = SpecFileList(**data_list)
        _ = SpecFileListReflection(**data_reflection)
    except ValidationError as e:
        pytest.fail(f"Model instantiation failed: {e}")
