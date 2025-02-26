import logging
import time
from pathlib import Path
from typing import Optional
import yaml
from unittest import mock
from .summarize import display_run_summary
from .data_types import (
    AICodeParams,
    SpecFileList,
    SpecFileListReflection,
    SpecTask,
    PaicPatternEnum,
)
from .spec_module import (
    parse_spec_file,
    build_prompt_list,
    build_prompt_list_reflection,
    ai_code,
    build_ai_coding_assistant,
)
from .spec_director_runner import run_spec_list_director

logger = logging.getLogger(name="paic_patterns")


def run_spec(spec_path: str, from_task_number: Optional[int] = None):
    start_time = time.time()
    try:
        # Validate API key before running spec
        from .member_runner import validate_api_key

        if not validate_api_key():
            raise ValueError("Invalid or expired API key")
        logger.info(
            "📝 Parsing spec file", extra={"rich_type": "text", "value": spec_path}
        )
        spec = parse_spec_file(spec_path, from_task_number)
        spec.config_from_task_number = from_task_number
        logger.info(
            "Parsed spec",
            extra={
                "rich_type": "json",
                "value": spec.model_dump(),
                # "value": {
                #     "plan_name": spec.plan_name,
                #     "pattern": spec.pattern,
                #     "task_count": len(spec.tasks),
                # },
            },
        )
        if spec.pattern == PaicPatternEnum.list_reflection:
            run_spec_list_reflection(spec)
        elif spec.pattern == PaicPatternEnum.list_director:
            run_spec_list_director(spec)
        else:
            # Default handler for standard list pattern and any unrecognized patterns
            run_spec_list(spec)

        display_run_summary(start_time)
    except Exception as e:
        display_run_summary(start_time, success=False, error=e)
        raise


def run_spec_list(spec: SpecFileList):
    logger.info(
        "🤖 Building Prompts & AI Coding Assistant",
    )
    prompts = build_prompt_list(spec)
    settings = {}
    if spec.reasoning_effort:
        settings["reasoning_effort"] = spec.reasoning_effort
    code_params = AICodeParams(
        architect=spec.architect,
        prompt="",
        model=spec.main_model,
        editor_model=spec.editor_model,
        editable_context=spec.editable_context,
        readonly_context=spec.readonly_context,
        settings=settings,
    )
    coder = build_ai_coding_assistant(code_params)
    logger.info(
        f"🚀 Executing Spec Prompt '{spec.plan_name}'",
    )
    for prep in prompts:
        if (
            spec.config_from_task_number is not None
            and prep.task_number < spec.config_from_task_number
        ):
            task_title = (
                spec.tasks[prep.task_number - 1].title
                if spec.tasks[prep.task_number - 1].title
                else "Untitled Task"
            )
            logger.info(
                "⚙️ Skipping task",
                extra={
                    "rich_type": "panel",
                    "value": f"{prep.task_number} - {task_title}",
                },
            )
            continue
        task_title = (
            spec.tasks[prep.task_number - 1].title
            if spec.tasks[prep.task_number - 1].title
            else "Untitled Task"
        )
        logger.info(
            f"🚀 Running Task ({prep.task_number}/{len(spec.tasks)})",
            extra={"rich_type": "panel", "value": task_title},
        )
        logger.info(
            "📝 Prompt",
            extra={
                "rich_type": "code",
                "value": prep.prompt.strip(),
                "language": "markdown",
            },
        )
        code_params.prompt = prep.prompt
        ai_code(coder, code_params)
    logger.info(
        f"🎉 Completed Running Spec Prompt '{spec.plan_name}'",
    )


def run_spec_list_reflection(spec: SpecFileListReflection):
    logger.info(
        "🤖 Building Prompts & AI Coding Assistant",
    )
    # Use the new reflection-specific prompt builder
    prompts = build_prompt_list_reflection(spec)
    settings = {}
    if spec.reasoning_effort:
        settings["reasoning_effort"] = spec.reasoning_effort
    code_params = AICodeParams(
        architect=spec.architect,
        prompt="",
        model=spec.main_model,
        editor_model=spec.editor_model,
        editable_context=spec.editable_context,
        readonly_context=spec.readonly_context,
        settings=settings,
    )
    coder = build_ai_coding_assistant(code_params)
    logger.info(
        f"🚀 Executing Spec Prompt '{spec.plan_name}'",
    )
    for prep in prompts:
        if (
            spec.config_from_task_number is not None
            and prep.task_number < spec.config_from_task_number
        ):
            logger.info(
                "⚙️ Skipping task",
                extra={
                    "rich_type": "panel",
                    "value": f"{prep.task_number} - Reflection Task",
                },
            )
            continue

        logger.info(
            "📝 Prompt",
            extra={
                "rich_type": "code",
                "value": prep.prompt.strip(),
                "language": "markdown",
            },
        )
        code_params.prompt = prep.prompt
        ai_code(coder, code_params)
    logger.info(
        f"🎉 Completed Running Spec Reflection Prompt '{spec.plan_name}'",
    )


def run_spec_self_build(spec_path: str) -> None:
    """Self-build tasks in a spec file based on existing content"""
    # Validate API key before running spec self-build
    from .member_runner import validate_api_key

    if not validate_api_key():
        raise ValueError("Invalid or expired API key")

    logger.info(
        "📝 Loading spec file for self-build",
        extra={"rich_type": "text", "value": spec_path},
    )
    spec = parse_spec_file(spec_path)

    # Validate required fields
    if not spec.high_level_objective:
        msg = "In order to run self-build the high_level_objective must be filled out."
        logger.error(msg)
        raise ValueError(msg)

    if not spec.implementation_details:
        msg = (
            "In order to run self-build the implementation_details must be filled out."
        )
        logger.error(msg)
        raise ValueError(msg)

    if not spec.tasks or len(spec.tasks) < 1:
        msg = "In order to run self-build at least one task with title and prompt must exist."
        logger.error(msg)
        raise ValueError(msg)

    # Format existing tasks for prompt
    existing_tasks = ""
    for i, task in enumerate(spec.tasks):
        existing_tasks += f"\n### Task ({i+1}): '{task.title}'\n{task.prompt}\n"

    # Build the self-build prompt
    prompt = f"""Based on the high level objective, implementation details, instructions, and existing tasks, build out the rest of the tasks.

## Instructions

- Pay close attention to the existing task and specifically how the prompt is written. Use the same structure and style.
- Break up the implementation details into smaller, manageable chunks again referring to the existing tasks as a guide.
- We want individual tasks to be small so they can be completed in a single session.
- Your job is exclusively to add the tasks to the list of tasks. We're not writing any code.
- Heavily base your new task on the implementation details. Look for lists and patterns in the implementation details you can break into tasks.
- Be verbose with your details. Include any information that will be helpful for the individual task.
- Use indentation, bullets, and formatting to communicate clear if it's useful for the task at hand.
- Focus your generation on 'title' and 'prompt' fields. Simply copy any other fields from the existing tasks. For example if you see 'reflection_count', simply copy it for every new task you create.

## High Level Objective
{spec.high_level_objective}

## Implementation Details
{spec.implementation_details}

## Existing Tasks to work from
{existing_tasks}

---

When you're ready, add the new task to the list of tasks."""

    # Create AI coding assistant with spec file as editable context
    code_params = AICodeParams(
        architect=False,
        prompt=prompt,
        model=spec.main_model,
        editor_model=spec.editor_model,
        editable_context=[spec_path],
        readonly_context=[],
        settings={},
        use_git=False,
    )

    logger.info(
        "🤖 Building AI Coding Assistant for self-build",
    )
    coder = build_ai_coding_assistant(code_params)

    logger.info(
        "🚀 Running self-build prompt",
    )
    ai_code(coder, code_params)

    logger.info(
        "✅ Completed self-build of tasks",
    )
