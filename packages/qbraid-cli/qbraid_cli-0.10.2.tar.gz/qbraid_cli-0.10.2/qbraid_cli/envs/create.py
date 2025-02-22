# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module supporting 'qbraid envs create' command.

"""


def create_venv(*args, **kwargs) -> None:
    """Create a python virtual environment for the qBraid environment."""
    from qbraid_core.services.environments import create_local_venv

    return create_local_venv(*args, **kwargs)


def update_state_json(*ags, **kwargs) -> None:
    """Update the state.json file for the qBraid environment."""
    from qbraid_core.services.environments.state import update_state_json as update_state

    return update_state(*ags, **kwargs)


def create_qbraid_env_assets(slug: str, alias: str, kernel_name: str, slug_path: str) -> None:
    """Create a qBraid environment including python venv, PS1 configs,
    kernel resource files, and qBraid state.json."""
    from qbraid_core.services.environments.create import create_qbraid_env_assets as create_assets

    return create_assets(slug, alias, kernel_name, slug_path)
