"""Build SHA-256 file baselines and report added, removed, and modified files without changing the monitored directory."""
import argparse
import hashlib
import json
from pathlib import Path

def snapshot(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('root must be a directory')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            continue
        if path.is_file():
            # Never follow a parent symlink outside the chosen root.
            if any((root / part).is_symlink() for part in path.relative_to(root).parents if part != Path('.')):
                continue
            path.resolve().relative_to(root)
            digest = hashlib.sha256()
            with path.open('rb') as handle:
                for block in iter(lambda: handle.read(65536), b''):
                    digest.update(block)
            result[path.relative_to(root).as_posix()] = digest.hexdigest()
    return result

def compare(before, after):
    return dict(added=sorted(after.keys()-before.keys()),
                removed=sorted(before.keys()-after.keys()),
                modified=sorted(key for key in before.keys() & after.keys() if before[key] != after[key]))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['baseline', 'check'])
    parser.add_argument('root', type=Path)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        manifest = args.manifest.resolve()
        if manifest.is_relative_to(root):
            raise ValueError('store the manifest outside the monitored directory')
        current = snapshot(root)
        if args.mode == 'baseline':
            # Exclusive creation prevents silently replacing a trusted baseline.
            with manifest.open('x', encoding='utf-8') as handle:
                json.dump(current, handle, indent=2)
            print(json.dumps({'files':len(current)}))
        else:
            old = json.loads(manifest.read_text(encoding='utf-8'))
            if not isinstance(old, dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in old.items()):
                raise ValueError('manifest must map paths to digests')
            report = compare(old, current)
            print(json.dumps(report, indent=2))
            return int(any(report.values()))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f'error: {exc}\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
