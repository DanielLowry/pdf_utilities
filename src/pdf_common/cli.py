from pathlib import Path


def prompt_path(prompt: str, default: str | None = None, must_exist: bool = False) -> Path:
    """
    Ask the user for a path with an optional default, retrying until a value is provided.
    """
    while True:
        suffix = f" [{default}]" if default else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default:
            raw = default
        if not raw:
            print("Please enter a path.")
            continue
        # Accept pasted paths with quotes (common when paths contain spaces)
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        path = Path(raw).expanduser()
        if must_exist and not path.exists():
            print(f"{path} does not exist. Try again.")
            continue
        return path


def confirm(prompt: str) -> bool:
    resp = input(f"{prompt} [y/N]: ").strip().lower()
    return resp in ("y", "yes")
