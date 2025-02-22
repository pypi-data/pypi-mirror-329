import subprocess
import logging
import shlex
from paic_patterns.modules.data_types import (
    AICodeParams,
    EvaluationRequest,
    SpecFileListDirector,
)

from paic_patterns.modules.spec_module import (
    build_ai_coding_assistant,
    ai_code,
    build_prompt_list_director,
)
from paic_patterns.modules.director_intelligence import evaluate_task

logger = logging.getLogger("paic_patterns")


def execute_evaluator_command(evaluator_command: str) -> str:
    """
    Execute the evaluator command safely using shlex.split and return the combined output.
    Logs a warning if the command returns a non-zero exit code, and logs an error on exceptions.
    """
    try:
        logger.info(
            "💻 Evaluator Command",
            extra={"rich_type": "code", "value": evaluator_command},
        )
        cmd = shlex.split(evaluator_command)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        if proc.returncode != 0:
            logger.warning(
                f"⚠️ Evaluator command returned non-zero exit code: {proc.returncode}",
                extra={"rich_type": "panel", "value": output},
            )
        return output
    except Exception as e:
        error_msg = f"Error executing evaluator command: {str(e)}"
        logger.error(
            "❌ Evaluator command failed",
            extra={"rich_type": "panel", "value": error_msg},
        )
        return error_msg


def run_spec_list_director(spec: "SpecFileListDirector") -> None:
    """
    Execute the director spec by iterating through its tasks.
    For each director task, if evaluator_count and evaluator_command are specified,
    repeatedly execute the task and evaluate its output until it succeeds or the maximum
    number of evaluation attempts is reached. If evaluation is not configured, simply
    run the task once.
    """
    logger.info(f"🚀 Running Director Spec: '{spec.plan_name}'")

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
        use_git=True,
    )

    coder = build_ai_coding_assistant(code_params)

    director_prompts = build_prompt_list_director(spec)

    for prep in director_prompts:
        task = spec.tasks[prep.task_number - 1]
        logger.info(
            f"🚀 Running Task ({prep.task_number}/{len(spec.tasks)})",
            extra={"rich_type": "panel", "value": task.title},
        )
        base_prompt = prep.prompt
        # Check if evaluation is configured for this task
        if task.evaluator_count and task.evaluator_command:
            max_attempts = task.evaluator_count
            success = False
            attempt = 0
            current_prompt = base_prompt
            execution_output = ""
            evaluation = None
            while attempt < max_attempts and not success:
                if attempt > 0 and not success:
                    logger.info(f"🔄 Task '{task.title}' – Attempt {attempt + 1}")

                code_params.prompt = current_prompt

                # Log the complete prompt being sent
                logger.info(
                    "📝 Prompt",
                    extra={
                        "rich_type": "code",
                        "value": current_prompt,
                        "language": "markdown",
                    },
                )

                ai_code(coder, code_params)

                logger.info(f"✅ AI Coding Prompt Completed")

                # Execute the evaluator command and capture its output
                execution_output = execute_evaluator_command(task.evaluator_command)

                # Build the evaluation request
                eval_request = EvaluationRequest(
                    spec=spec,
                    evaluator_command=task.evaluator_command,
                    evaluator_command_result=execution_output,
                    prompt=current_prompt,
                    editable_context=spec.editable_context,
                    readonly_context=spec.readonly_context,
                )

                # Call our evaluation function
                evaluation = evaluate_task(eval_request)

                if evaluation.success:
                    logger.info(
                        f"✅ Task '{task.title}' succeeded on attempt {attempt + 1}"
                    )
                    success = True
                else:
                    logger.warning(
                        f"❌ Task '{task.title}' failed on attempt {attempt + 1}. Feedback: {evaluation.feedback}"
                    )
                    # Generate a new prompt using feedback and previous output
                    current_prompt = (
                        f"""# Generate the next iteration of code based on your original task prompt and the feedback received.
> This is your {attempt + 1}th attempt and you have {max_attempts - attempt - 1} attempt(s) remaining.

## Original Task Prompt
{base_prompt}

## Evaluation Command
{task.evaluator_command}

## Previous Attempt Output
{execution_output}

## Feedback from Evaluation
{evaluation.feedback}"""
                    ).strip()

                    # Log the attempt details
                    logger.info(
                        f"📊 Attempt {attempt + 1} Summary",
                        extra={
                            "rich_type": "json",
                            "value": {
                                "attempt": attempt + 1,
                                "max_attempts": max_attempts,
                                "execution_output": execution_output,
                                "feedback": evaluation.feedback,
                            },
                        },
                    )

                    logger.info(
                        "📝 Updated prompt for next attempt",
                    )

                attempt += 1

            if not success:
                error_msg = f"🚫 Task '{task.title}' did not succeed after {max_attempts} attempts."
                logger.error(
                    error_msg,
                    extra={
                        "rich_type": "panel",
                        "value": (
                            f"{error_msg}\n\n"
                            f"Last execution output:\n{execution_output}\n\n"
                            f"Last feedback:\n{evaluation.feedback if evaluation else 'No feedback available'}"
                        ),
                    },
                )

                if spec.fail_fast:
                    raise RuntimeError(
                        f"{error_msg}\n"
                        f"Last feedback: {evaluation.feedback if evaluation else 'No feedback available'}"
                    )
                else:
                    logger.warning(
                        "⚠️ Continuing to next task since fail_fast=False",
                        extra={
                            "rich_type": "panel",
                            "value": "The spec will continue running but may have incomplete or incorrect implementations.",
                        },
                    )
        else:
            # If evaluation isn't configured, simply run the task once.
            logger.info(
                "📝 Prompt",
                extra={
                    "rich_type": "code",
                    "value": base_prompt.strip(),
                    "language": "markdown",
                },
            )
            code_params.prompt = base_prompt
            ai_code(coder, code_params)
            logger.info(f"Task '{task.title}' executed without evaluation.")
