from pathlib import Path

from sismic.interpreter import Interpreter
from sismic.clock import UtcClock
from sismic.io import import_from_yaml

try:
    from importlib import resources as importlib_resources
except Exception:
    # backport for python 3.6
    import importlib_resources


def get_yaml_file(machine_name):
    if not machine_name.endswith(".yaml"):
        machine_name += ".yaml"

    try:
        full_path = (
            importlib_resources.files("hcam_devices") / "machines" / machine_name
        )
        if not full_path.exists():
            # yaml file not installed with package, see if it is specified directly
            full_path = Path(machine_name)
    except AttributeError:
        # hack for Python <3.9
        from pkg_resources import resource_filename, resource_exists

        full_path = resource_filename("hcam_devices", f"machines/{machine_name}")
        if not resource_exists("hcam_devices", f"machines/{machine_name}"):
            # yaml file not installed with package, see if it is specified directly
            full_path = Path(machine_name)

    return str(full_path)


def create_machine(name, **kwargs):
    full_path = get_yaml_file(name)
    return Interpreter(import_from_yaml(filepath=full_path), clock=UtcClock(), **kwargs)
