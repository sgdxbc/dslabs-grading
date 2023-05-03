import re
import pathlib

OUT_DIRS = ["out_1", "out_2"]

scores = {}
for out_dir in OUT_DIRS:
    for log_path in pathlib.Path(out_dir).glob("*.tar.gz.log"):
        name = log_path.name.split("_")[0]  # TODO customizable?
        if name not in scores:
            scores[name] = {}

        log = log_path.read_text()
        # TODO: defense against manually construction
        m = re.search(r"Points:\ (\d+)", log)
        if not m:
            scores[name][out_dir] = None
        else:
            scores[name][out_dir] = int(m[1])

for name, run_scores in scores.items():
    print(f"{name:30}", end="")
    for out_dir in OUT_DIRS:
        score = run_scores.get(out_dir)
        if not score:
            score = "N/A"
        print(f"{score:<10}", end="")
    print()
