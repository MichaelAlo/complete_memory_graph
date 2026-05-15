import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "graphify-out"
OUT.mkdir(exist_ok=True)

status = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "source": str(SRC.relative_to(ROOT)) if SRC.exists() else "src",
    "graphify_available": shutil.which("graphify") is not None,
}

if status["graphify_available"] and SRC.exists():
    cmd = ["graphify", str(SRC), "--update", "--no-viz"]
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        status["command"] = " ".join(cmd)
        status["returncode"] = result.returncode
        status["stdout_tail"] = result.stdout[-2000:]
        status["stderr_tail"] = result.stderr[-2000:]
    except Exception as e:
        status["returncode"] = -1
        status["error"] = str(e)
else:
    files = []
    if SRC.exists():
        for p in SRC.rglob("*"):
            if p.is_file():
                files.append(str(p.relative_to(ROOT)))
    status["fallback"] = True
    status["files_indexed"] = files

(OUT / "refresh-status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
(OUT / "GRAPH_REPORT.md").write_text(
    "# Graph Refresh Report\n\n"
    f"- Timestamp: {status['timestamp']}\n"
    f"- Source root: `{status['source']}`\n"
    f"- Graphify available: `{status['graphify_available']}`\n"
    f"- Fallback mode: `{status.get('fallback', False)}`\n",
    encoding="utf-8",
)
