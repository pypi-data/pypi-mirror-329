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

pattern: list

architect: true

main_model: "__main_model__"

# used only if mode is "architect: true"
editor_model: "__editor_model__"

# Code you want your AI Coding Assistant to edit
editable_context: __editable_context__

# Code you want your AI Coding Assistant to read but not edit
readonly_context: __readonly_context__

high_level_objective: "high level objective of the feature you're implementing"

implementation_details: |
    implementation details of the feature you're implementing

# your list of tasks aka prompts that will be executed in order one by one
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

pattern: list-reflection

architect: true

main_model: "__main_model__"

# used only if mode is "architect: true"
editor_model: "__editor_model__" 

# Code you want your AI Coding Assistant to edit
editable_context: __editable_context__

# Code you want your AI Coding Assistant to read but not edit
readonly_context: __readonly_context__

high_level_objective: "high level objective of the feature you're implementing"

implementation_details: |
    implementation details of the feature you're implementing

# your list of tasks aka prompts that will be executed in order one by one
tasks:
  - title: "Task 1: high level description"
    prompt: |
      high to low level coding prompt for task 1
    reflection_count: 1
  
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

pattern: list-director

architect: true

main_model: "__main_model__"

# used only if mode is "architect: true"
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

# your list of tasks aka prompts that will be executed in order one by one
# replace the evaluator_command with the command you want to run to evaluate the task
# evaluator_count is the number of times to run the evaluator_command IF the evaluator_command fails
tasks:
  - title: "Task 1: high level description"
    prompt: |
      high to low level coding prompt for task 1
    evaluator_count: 3
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
