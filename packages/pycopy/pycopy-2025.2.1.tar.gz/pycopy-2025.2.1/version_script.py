import datetime
import re
import sys
from pathlib import Path

python_version_file = Path(".") / "pycopy" / "version.py"
pyproject_toml_regex = re.compile("\"(?P<VERSION>[0-9]+\\.[0-9]+\\.[0-9]+)\"\\s*#\\s?version")

def get_version(increment):
    date = datetime.date.today()
    return f"{date.year}.{date.month}.{increment}"

def is_current_month(year, month):
    date = datetime.date.today()
    if date.year != year:
        return False
    if date.month != month:
        return False
    return True

def write_version_file(version):
    python_version_file.touch(exist_ok=True)

    with open(python_version_file, "w") as file:
        file.write(f"""program_version = \"{version}\"""")

def get_current_version():
    path = Path(".") / "pyproject.toml"

    string = path.read_text()
    match = pyproject_toml_regex.search(string)

    return match.groupdict()["VERSION"]

def update_pyproject_toml(version):
    path = Path(".") / "pyproject.toml"

    string = path.read_text()
    match = pyproject_toml_regex.search(string)

    print(f"The old version is {match.groupdict()["VERSION"]}")

    path.write_text(pyproject_toml_regex.sub(f"\"{version}\" # version", string))


def update(version):
    print(f"Updating version to {version}")

    write_version_file(version)

    update_pyproject_toml(version)


def main(args=tuple(sys.argv)):
    if len(args) <= 1:
        current_version = get_current_version().split(".")
        new_increment = int(current_version[-1]) + 1

        if not is_current_month(int(current_version[0]), int(current_version[1])):
            new_increment = 1

        print(f"New version ist {new_increment}")
        main((args[0],new_increment,"update"))
        return

    version = get_version(int(args[1]))
    print(f"The current version is {version}")

    if len(args) <= 2 or args[2] != "update":
        return

    update(version)


main()
