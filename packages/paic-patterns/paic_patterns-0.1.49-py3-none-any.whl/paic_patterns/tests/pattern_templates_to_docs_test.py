import yaml


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
    assert content["main_model"] == "openai/o3-mini"
    assert content["editor_model"] == "anthropic/claude-3-5-sonnet-20241022"
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
    assert content["main_model"] == "openai/o3-mini"
    assert content["editor_model"] == "anthropic/claude-3-5-sonnet-20241022"
    assert isinstance(content["editable_context"], list)
    assert isinstance(content["readonly_context"], list)


def test_process_all_templates(tmp_path, monkeypatch):
    """Test processing all templates to both output directories."""
    from script_pattern_templates_to_docs import process_all_templates

    # Mock output directories
    mock_relative = tmp_path / "relative"
    mock_local = tmp_path / "local"
    monkeypatch.setattr(
        "pattern_templates_to_docs.RELATIVE_OUTPUT_DIR", str(mock_relative)
    )
    monkeypatch.setattr("pattern_templates_to_docs.LOCAL_OUTPUT_DIR", mock_local)

    # Process templates
    process_all_templates()

    # Verify both directories were created
    assert mock_relative.exists()
    assert mock_local.exists()

    # Verify files in both directories
    for pattern in ["list", "list-reflection"]:
        rel_file = mock_relative / f"{pattern}.yml"
        local_file = mock_local / f"{pattern}.yml"

        assert rel_file.exists()
        assert local_file.exists()

        # Verify content is identical
        assert rel_file.read_text() == local_file.read_text()

        # Verify YAML is valid
        content = yaml.safe_load(rel_file.read_text())
        assert content["pattern"] == pattern
