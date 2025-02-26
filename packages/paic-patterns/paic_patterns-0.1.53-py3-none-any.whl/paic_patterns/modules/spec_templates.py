template_spec_file_markdown = """# __plan_name__
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- [High level goal goes here - what do you want to build?]

## Mid-Level Objective

- [List of mid-level objectives - what are the steps to achieve the high-level objective?]
- [Each objective should be concrete and measurable]
- [But not too detailed - save details for implementation notes]

## Implementation Notes

- [Important technical details - what are the important technical details?]
- [Dependencies and requirements - what are the dependencies and requirements?]
- [Coding standards to follow - what are the coding standards to follow?]
- [Other technical guidance - what are other technical guidance?]

## Context

### Editable context
__editable_context__

### Readonly context
__readonly_context__

## Low-Level Tasks
> Ordered from start to finish

1. [First task - what is the first task?]
```
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```
2. [Second task - what is the second task?]
```
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```
3. [Third task - what is the third task?]
```
What prompt would you run to complete this task?
What file do you want to CREATE or UPDATE?
What function do you want to CREATE or UPDATE?
What are details you want to add to drive the code changes?
```"""

template_spec_file_list = """plan_name: "__plan_name__"

# Use the list pattern to run a series of tasks in order one by one
pattern: list

# (Recommended) Run every task in architect mode where your main_model reasons then drafts the code and your editor_model writes the code
architect: true

main_model: "__main_model__"

# Used only if mode is "architect: true"
editor_model: "__editor_model__"

# Code you want your AI Coding Assistant to edit
editable_context: __editable_context__

# Code you want your AI Coding Assistant to read but not edit
readonly_context: __readonly_context__

high_level_objective: "high level objective of the feature you're implementing"

implementation_details: |
  implementation details of the feature you're implementing

# Your list of tasks aka prompts that will be executed in order one by one
tasks:
  - title: "Task 1: high level description"
    prompt: |
      high to low level coding prompt for task 1
  
  - title: "Task 2: high level description"
    prompt: |
      high to low level coding prompt for task 2
  
  - title: "Task 3: high level description"
    prompt: |
      high to low level coding prompt for task 3
"""

template_spec_file_list_reflection = """plan_name: "__plan_name__"

# Use the list-reflection pattern to run a series of tasks in order one by one with reflection(s) to double check the code is correct
pattern: list-reflection

# (Recommended) Run every task (including reflection loops) in architect mode where your main_model reasons then drafts the code and your editor_model writes the code
architect: true

main_model: "__main_model__"

# Used only if mode is "architect: true"
editor_model: "__editor_model__" 

# Code you want your AI Coding Assistant to edit
editable_context: __editable_context__

# Code you want your AI Coding Assistant to read but not edit
readonly_context: __readonly_context__

high_level_objective: "high level objective of the feature you're implementing"

implementation_details: |
  implementation details of the feature you're implementing

# Your list of tasks aka prompts that will be executed in order one by one
# (Optional) Add reflection_count to any task to set the number of times to run the reflection prompt after the initial coding prompt
# (Optional) Add reflection_prompt_prefix to any task to set the prompt prefix that will guide the reflection ai coding prompt
tasks:
  - title: "Task 1: high level description"
    prompt: |
      high to low level coding prompt for task 1

    # (Optional) Number of times to run the reflection prompt after the initial coding prompt
    reflection_count: 1

    # (Optional) Set the prompt prefix that will guide the reflection ai coding prompt
    # reflection_prompt_prefix: __reflection_prompt_prefix__

  - title: "Task 2: high level description"
    prompt: |
      high to low level coding prompt for task 2
    reflection_count: 1
  
  - title: "Task 3: high level description"
    prompt: |
      high to low level coding prompt for task 3
    reflection_count: 1
"""

template_spec_file_list_director = """plan_name: "__plan_name__"

# Use the list-director pattern to run a series of tasks in order one by one. Run a command and pass it's output into the evaluator model to evaluate the code is correct.
pattern: list-director

# (Recommended) Run every task (including evaluator loops) in architect mode where your main_model reasons then drafts the code and your editor_model writes the code
architect: true

main_model: "__main_model__"

# Used only if mode is "architect: true"
editor_model: "__editor_model__"

# evaluator model (currently only o3-mini is supported)
evaluator_model: "__evaluator_model__"

# Code you want your AI Coding Assistant to edit
editable_context: __editable_context__

# Code you want your AI Coding Assistant to read but not edit
readonly_context: __readonly_context__

high_level_objective: "high level objective of the feature you're implementing"

implementation_details: |
  implementation details of the feature you're implementing

# Your list of tasks aka prompts that will be executed in order one by one
# (Optional) Add evaluator_count to any task to set the number of times to run the evaluator_command IF the evaluator_command fails
# (Optional) Add evaluator_command to any task with the command you want to run to evaluate the task
tasks:
  - title: "Task 1: high level description"
    prompt: |
      high to low level coding prompt for task 1

    # (Optional) Number of times to run the evaluator_command IF the evaluator_command fails
    evaluator_count: 3

    # (Optional) The command to run to evaluate the task.
    evaluator_command: "uv run pytest"
  
  - title: "Task 2: high level description"
    prompt: |
      high to low level coding prompt for task 2
    evaluator_count: 3
    evaluator_command: "uv run pytest"

  - title: "Task 3: high level description"
    prompt: |
      high to low level coding prompt for task 3
    evaluator_count: 3
    evaluator_command: "uv run pytest"
"""
