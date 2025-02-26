import logging
from openai import OpenAI
import os
from paic_patterns.modules.data_types import EvaluationRequest, EvaluationResult

logger = logging.getLogger(name="paic_patterns")

# OpenAI client will be instantiated when needed to prevent early API key errors
client = None

def get_openai_client():
    global client
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required but not found in environment")
        client = OpenAI(api_key=api_key)
    return client


def evaluate_task(evaluation_request: EvaluationRequest) -> EvaluationResult:
    """
    Evaluate the result of a director task execution.

    This function creates a structured prompt based on the evaluation_request input,
    calls the OpenAI LLM, and returns an EvaluationResult containing:
       - success: bool
       - feedback: Optional[str]

    The output from the LLM is expected to be valid JSON without any extra formatting.

    Args:
        evaluation_request: The evaluation request containing spec, prompt and results

    Returns:
        EvaluationResult with success status and optional feedback

    Raises:
        Exception: If API call fails or returns invalid response
    """
    try:
        # Helper: loads file content with header "### <filename>"
        def load_files(file_list: list[str], editable: bool) -> str:
            result = ""
            for fpath in file_list:
                try:
                    with open(fpath, "r", encoding="utf-8") as file:
                        content = file.read().strip()
                    prefix_text = "Editable" if editable else "Read-Only"
                    result += f"\n### {prefix_text} File: {fpath}\n{content}\n"
                except Exception as e:
                    logger.warning(
                        f"Error reading file: {fpath}",
                        extra={"rich_type": "panel", "value": f"Error: {str(e)}"},
                    )
                    continue
            return result

        editable_files_content = load_files(
            evaluation_request.editable_context, editable=True
        )
        readonly_files_content = load_files(
            evaluation_request.readonly_context, editable=False
        )

        # Build a structured prompt using the fields in the evaluation_request.
        prompt = f"""Evaluate the following task execution result and determine if it met the specified objectives.

## Instructions
- You are an expert software engineer.
- You're reviewing the execution of a task by your engineering co-worker.
- You'll be given the task prompt, the editable files, the read-only files, the evaluation command, and the evaluation command result.
- You'll need to evaluate the task execution result and determine if it met the specified objectives.
- If the task was executed successfully, return {{success: true, feedback: null}}
- If the task was not executed successfully, return {{success: false, feedback: detailed feedback explaining what failed and how to fix it. Make it super clear and concise. Be kind, and helpful but direct.}}

## Task Prompt (Current Task) (Desired Result)
{evaluation_request.prompt}

## Editable Files
{editable_files_content}

## Read-Only Files
{readonly_files_content}

## Evaluation Command
{evaluation_request.evaluator_command}

## Evaluation Command Result
{evaluation_request.evaluator_command_result}

## Response Format
Return a valid JSON object with the following structure:
{{
    "success": bool,    // true if the task execution was successful, false otherwise
    "feedback": string | null  // detailed feedback (if any), or null if successful
}}

Ensure that your output is valid JSON without any additional text.
"""

        logger.info(
            "🔍 Evaluation prompt",
            extra={"rich_type": "code", "value": prompt, "language": "markdown"},
        )

        # Call the OpenAI Chat API using the evaluator_model specified in the spec.
        completion = get_openai_client().beta.chat.completions.parse(
            model=evaluation_request.spec.evaluator_model,
            messages=[{"role": "user", "content": prompt}],
            response_format=EvaluationResult,
        )

        eval_result = completion.choices[0].message.parsed

        logger.debug(
            "🤖 Raw Evaluator response",
            extra={"rich_type": "code", "value": eval_result, "language": "json"},
        )

        logger.info(
            "📊 Evaluation result",
            extra={"rich_type": "json", "value": eval_result.model_dump()},
        )

        return eval_result

    except Exception as e:
        logger.error(
            "Evaluation failed",
            extra={"rich_type": "panel", "value": f"Error evaluating task: {str(e)}"},
        )
        return EvaluationResult(
            success=False, feedback=f"Error evaluating task: {str(e)}"
        )
