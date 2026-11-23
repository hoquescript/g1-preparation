# g1-preparation

Ontario G1 knowledge test practice quiz: 203 multiple-choice questions, practice and exam modes, 80% to pass.

## Use

```
python3 server.py        # then open http://127.0.0.1:8000/
```

Every answer is saved to `g1_history.db` (SQLite, table `attempts`: question, picked, answer,
is_correct, mode, answered_at). "Focus on questions I've got wrong before" reads from it.
See your most-missed questions with:

```
sqlite3 g1_history.db "SELECT question, COUNT(*) FROM attempts WHERE NOT is_correct GROUP BY question ORDER BY 2 DESC"
```

## How the question bank is built

1. `capture.py` screenshots the study material into `screenshots/`.
2. `ocr.py` extracts questions and answers into `questions.csv` (macOS Vision).
3. `options.py` holds the correct answer wording and three wrong options per question.
4. `python3 build_bank.py` merges them into `question_bank.js`, which `quiz.html` loads.
