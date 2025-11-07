# config.py
import os
import glob
import yaml
import copy

def _deep_merge(a, b):
    """
    Merge dict b into dict a (in place) and return a.
    - dict + dict: deep merge
    - list + list: concatenate
    - scalar/other: b overwrites a
    """
    for k, v in b.items():
        if k in a:
            if isinstance(a[k], dict) and isinstance(v, dict):
                _deep_merge(a[k], v)
            elif isinstance(a[k], list) and isinstance(v, list):
                a[k].extend(v)
            else:
                a[k] = copy.deepcopy(v)
        else:
            a[k] = copy.deepcopy(v)
    return a

def load_config(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or {}

def load_config_dir(dir_path: str):
    """
    Load and merge all *.yml|*.yaml files in lexicographic order.
    Ignores temp/backup files and unreadable entries.
    """
    if not os.path.isdir(dir_path):
        return {}

    patterns = [os.path.join(dir_path, "*.yml"), os.path.join(dir_path, "*.yaml")]
    files = sorted({p for pat in patterns for p in glob.glob(pat)})

    merged = {}
    for p in files:
        # Skip common junk files
        name = os.path.basename(p)
        if name.endswith((".rpmnew", ".rpmsave", ".bak", "~")) or name.startswith("."):
            continue
        try:
            with open(p, "r") as f:
                data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                raise ValueError(f"{p} must contain a mapping at the top level")
            _deep_merge(merged, data)
        except Exception as e:
            raise RuntimeError(f"Failed to load config snippet {p}: {e}") from e
    return merged

def load_config_any(file_path: str, dir_path: str):
    """
    Prefer directory if it exists and contains at least one file,
    otherwise fall back to the single file.
    """
    try:
        dir_has_files = os.path.isdir(dir_path) and any(
            glob.glob(os.path.join(dir_path, "*.yml")) +
            glob.glob(os.path.join(dir_path, "*.yaml"))
        )
    except Exception:
        dir_has_files = False

    if dir_has_files:
        return load_config_dir(dir_path)
    else:
        return load_config(file_path)
