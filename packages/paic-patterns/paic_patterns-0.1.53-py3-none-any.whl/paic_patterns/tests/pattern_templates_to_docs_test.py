import pytest
import yaml
import os
from pathlib import Path
from paic_patterns.modules.aider_llm_models import (
    DEFAULT_EDITOR_MODEL,
    DEFAULT_MAIN_MODEL,
    DEFAULT_EVALUATOR_MODEL,
)


def test_render_template(tmp_path):
    """Test rendering a template to a temporary directory."""
    from script_pattern_templates_to_docs import render_template

    # Test rendering list pattern
    render_template("list", tmp_path)
    list_file = tmp_path / "list.yml"
    assert list_file.exists()

    # Verify YAML content
    content = yaml.safe_load(list_file.read_text())
    assert content["pattern"] == "list"
    assert content["plan_name"] == "template-list"
    assert content["main_model"] == f"{DEFAULT_MAIN_MODEL}"
    assert content["editor_model"] == f"{DEFAULT_EDITOR_MODEL}"
    assert isinstance(content["editable_context"], list)
    assert isinstance(content["readonly_context"], list)

    # Test rendering list-reflection pattern
    render_template("list-reflection", tmp_path)
    reflection_file = tmp_path / "list-reflection.yml"
    assert reflection_file.exists()

    # Verify YAML content
    content = yaml.safe_load(reflection_file.read_text())
    assert content["pattern"] == "list-reflection"
    assert content["plan_name"] == "template-list-reflection"
    assert content["main_model"] == f"{DEFAULT_MAIN_MODEL}"
    assert content["editor_model"] == f"{DEFAULT_EDITOR_MODEL}"
    assert isinstance(content["editable_context"], list)
    assert isinstance(content["readonly_context"], list)
