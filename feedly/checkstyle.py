from pathlib import Path

import subprocess
import sys
import os
import urllib.request


def run():
    jar = _download_checkstyle_if_missing()
    code = _run_checkstyle(jar)
    sys.exit(code)


def _download_checkstyle_if_missing() -> Path:
    path: Path = Path.home() / ".checkstyle"
    path.mkdir(exist_ok=True)

    path = path / "checkstyle-8.31-all.jar" ""
    if not path.exists():
        print(f"downloading jar to {path}")
        urllib.request.urlretrieve(
            "https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.31/checkstyle-8.31-all.jar",
            path,
        )

    return path


def _run_checkstyle(jar):
    cmd = f"java -cp {jar} com.puppycrawl.tools.checkstyle.Main -d -c {os.getcwd()}/.checkstyle"
    cmd = cmd.split() + sys.argv[1:]

    cpl = subprocess.run(args=cmd, capture_output=True)
    if cpl.returncode != 0:
        print(cpl.stdout.decode("utf-8"))
    return cpl.returncode
    # run subprocess and then sys.exit(exit code)
