import pytest

from paic_patterns.modules.spec_module import (
    SpecFileList,
    SpecFileListReflection,
    SpecTask,
    SpecTaskReflection,
)
from paic_patterns.modules.spec_runner import (
    build_prompt_list,
    build_prompt_list_reflection,
)
from paic_patterns.modules.aider_llm_models import REFLECTION_PROMPT_PREFIX
from paic_patterns.modules.spec_module import PreparedPrompt


# ------------- SKIPPING TESTS -------------
pytestmark = pytest.mark.skip(
    reason="These tests are temporarily disabled for maintenance"
)


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
                "tasks": [
                    {
                        "title": "Add",
                        "prompt": "Write add function",
                        "reflection_count": 2,
                        "reflection_prompt_prefix": "Custom reflection prefix",
                    }
                ],
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
            2,  # Expected number of reflection prompts
        ),
        # Test case 2: Optional sections missing, default reflection count
        (
            {
                "plan_name": "test_plan",
                "high_level_objective": None,
                "implementation_details": None,
                "tasks": [
                    {"title": "", "prompt": "Write function", "reflection_count": None}
                ],
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
            1,  # Default reflection count
        ),
    ],
)
def test_reflection_section_spacing(
    spec_data, expected_sections, expected_reflection_count
):
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
    assert (
        len(prepared) == 1 + expected_reflection_count
    )  # Original + reflection prompts
    sections = prepared[0].prompt.strip().split("\n")
    assert sections == expected_sections

    # Verify reflection prompts
    for i in range(expected_reflection_count):
        reflection_prompt = prepared[i + 1].prompt
        prefix = spec_data["tasks"][0].get(
            "reflection_prompt_prefix", REFLECTION_PROMPT_PREFIX
        )
        assert reflection_prompt.startswith(prefix + "\n\n")
        reflection_sections = reflection_prompt.strip().split("\n")[
            2:
        ]  # Skip prefix and empty line
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
