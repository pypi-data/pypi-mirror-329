from paic_patterns.modules.versioning import need_to_upgrade_application


def test_need_to_upgrade_version_mismatch():
    assert need_to_upgrade_application() is False
