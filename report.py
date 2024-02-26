import re
import pathlib
import pandas as pd

OUT_DIRS = ["lab1-out.0", "lab1-out.1", "lab1-out.2"]
COL = "Lab 1 (96793)"
CSV_FILE = "2024-02-26T1417_Grades-CS5223.csv"

data = pd.read_csv(CSV_FILE)
# print(data)

scores = {}
for out_dir in OUT_DIRS:
    for log_path in pathlib.Path(out_dir).glob("*.tar.gz.log"):
        # TODO customizable?
        splitted = log_path.name.split("_")
        name, id = splitted[0], int(splitted[-3])
        if (name, id) not in scores:
            scores[name, id] = {}

        log = log_path.read_text()
        # TODO: defense against manually construction
        m = re.search(r"Points:\ (\d+)", log)
        if not m:
            scores[name, id][out_dir] = None
        else:
            scores[name, id][out_dir] = int(m[1])


for (name, id), run_scores in scores.items():
    print(f"{name:30} {id:8}    ", end="")
    final_score = -1
    for out_dir in OUT_DIRS:
        score = run_scores.get(out_dir)
        if not score:
            score = "N/A"
        else:
            final_score = max(final_score, score)
        print(f"{score:<6}", end="")

    row = data["ID"] == id
    # print(row)
    if data[row].empty:
        print("!MISSING", end='')
    else:
        data.loc[row, COL] = final_score if final_score >= 0 else 'FAIL'
        print(f'=> {data.loc[row, "Student"].values[0]}', end='')

    print()

data.to_csv(CSV_FILE.replace('.csv', '.out.csv'))
