A minimal grading utility for DSLabs, use local machine to do grading.
Switch to other solution if there are so many submissions that distributed grading becomes a must.

The grading script extracts submission into a temporary directory, then override the directory content with a *handout overlay*.
The overlay contains files for compiling and running the submission, and also resets the test sources.
Then the submission is tested. 
The standard output is dumped into a log file, and move into submission directory after testing is done.
The testing will be killed after certain time limit, and the log file will be truncated into the last part if it is too long.
The grading script also skips all submissions that already have a dumped log file, so the script can be interrupted and resumed arbitrarily.

Step 1, prepare the handout overlay
```
$ ./prepare_overlay.sh
```

Step 2, edit constants in the head of `run_submissions.py` to match your need, then
```
$ python3 run_submissions.py
```

You may want to run the command in a detached tmux session.

Step 3, edit constants in the head of `report.py` to match your need, then
```
$ python3 report.py | sort
```

to parse all dumped log file and report submission scores.
If the score shows `N/A`, then the submission may have some problems getting compiled or tested, or its log file is missed.
You may manually check for this case.
