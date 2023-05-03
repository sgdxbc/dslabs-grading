import subprocess
import tempfile
import pathlib

SUBMISSIONS_DIR = "lab4-all"
OUT_DIR = "out_2"
HANDOUT_OVERLAY = "dslabs/handout-overlay.tar.gz"
RUN_TESTS_ARGS = "--lab 4"
# TIMEOUT = 800  # my lab 4 takes 635.71s
TIMEOUT = 1000


def run_submission(submission_path):
    # open log file early, so every submission will always has a corresponding
    # log file, make collection easier
    with tempfile.TemporaryDirectory() as work_dir, open(
        f"{OUT_DIR}/{submission_path.name}.log", "wb"
    ) as log_file:
        print(f"RUN {submission_path} IN {work_dir}")

        setup_command = f"tar -xf {submission_path} --directory={work_dir} && tar -xf {HANDOUT_OVERLAY} --directory={work_dir}"
        try:
            subprocess.run(
                setup_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print("SETUP FAILED")
            with open(
                f"{OUT_DIR}/{submission_path.name}_setup-error.log", "wb"
            ) as log_file:
                log_file.write(e.stdout)
            return

        run_command = f"timeout --signal=KILL {TIMEOUT} ./run-tests.py {RUN_TESTS_ARGS} | tail -n 1000"
        subprocess.run(
            run_command,
            shell=True,
            cwd=work_dir,
            stdout=log_file,
            stderr=subprocess.DEVNULL,
            # timeout=TIMEOUT,
        )


pathlib.Path(OUT_DIR).mkdir(exist_ok=True)
for submission_path in pathlib.Path(SUBMISSIONS_DIR).glob("*.tar.gz"):
    if pathlib.Path(f"{OUT_DIR}/{submission_path.name}.log").exists():
        print(f"SKIP {submission_path.name}")
        continue
    run_submission(submission_path)