"""Abre los registros de MLflow y actualiza sus rutas al directorio actual."""
from pathlib import Path
import sqlite3
import subprocess
import sys

root = Path(__file__).resolve().parent
db = root / "mlflow.db"
if db.exists():
    with sqlite3.connect(db) as con:
        for eid, in con.execute("SELECT experiment_id FROM experiments").fetchall():
            con.execute("UPDATE experiments SET artifact_location=? WHERE experiment_id=?",
                        ((root / "mlruns" / str(eid)).as_uri(), eid))
        for run_id, eid in con.execute("SELECT run_uuid, experiment_id FROM runs").fetchall():
            con.execute("UPDATE runs SET artifact_uri=? WHERE run_uuid=?",
                        ((root / "mlruns" / str(eid) / run_id / "artifacts").as_uri(), run_id))
subprocess.run([sys.executable, "-m", "mlflow", "ui", "--backend-store-uri",
                "sqlite:///" + db.as_posix()], cwd=root, check=True)
