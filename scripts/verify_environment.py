#!/usr/bin/env python3
"""Verify the Python environment and that required inputs are present."""
from __future__ import annotations
import sys, platform
from _bootstrap import ensure_importable
ensure_importable()

REQUIRED = ["pandas", "numpy", "matplotlib", "scipy", "yaml"]

def main() -> int:
    print("Python:", platform.python_version())
    ok = True
    for mod in REQUIRED:
        try:
            m = __import__(mod)
            print(f"  [ok] {mod} {getattr(m,'__version__','')}")
        except ImportError:
            print(f"  [MISSING] {mod}"); ok = False
    try:
        import responsible_llm_audit as rla
        cfg = rla.load_config()
        print("  [ok] responsible_llm_audit", rla.__version__, "| repo:", cfg.root.name)
        for tag, f in cfg.settings["data"]["response_files"].items():
            p = cfg.responses_dir / f
            print(f"  [{'ok' if p.exists() else 'MISSING'}] data/responses/{f}")
            ok = ok and p.exists()
        for sub, key in [("prompts", "prompts_file"), ("ratings", "ratings_file")]:
            f = cfg.settings["data"][key]
            p = getattr(cfg, f"{sub}_dir") / f
            print(f"  [{'ok' if p.exists() else 'MISSING'}] data/{sub}/{f}")
            ok = ok and p.exists()
        pumf = cfg.raw_dir / cfg.settings["data"]["pumf_filename"]
        print(f"  [note] CCHS PUMF {'present' if pumf.exists() else 'ABSENT (optional; persona verification uses documented counts)'}")
    except Exception as e:
        print("  [ERROR]", e); ok = False
    print("ENVIRONMENT:", "OK" if ok else "INCOMPLETE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
