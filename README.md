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

Questions come in categories, one per section of the study app:

| Category | Questions | Options | Paraphrases | Numbers |
|---|---|---|---|---|
| Road Rules | `questions.csv` | `options.py` | `paraphrases.py` | 1–203 |
| Fines, Limits & Points | `questions_fines.csv` | `options_fines.py` | `paraphrases_fines.py` | 1001–1094 |

The number is the global question number used by the answer history and `duplicates.py`; the quiz shows
the number within the category (e.g. "Fines, Limits & Points #12").

1. `capture.py --count N --out screenshots/<category>` screenshots a section of the study app.
2. `ocr.py --src screenshots/<category> --out questions_<category>.csv` extracts questions and answers (macOS Vision).
3. The options file holds the correct answer wording and three wrong options per question.
4. The paraphrases file holds three rewordings per question; each test shows the original or one of them at
   random, so you learn the rule rather than the wording. "Which is NOT..." questions also get positive
   versions with their own answers. New questions without paraphrases use the original only.
5. `duplicates.py` groups near-duplicate questions across categories; a test includes at most one from each group.
6. `python3 build_bank.py` merges everything into `question_bank.js`, which `quiz.html` loads.

To add a category, capture and OCR it as above, add its options and paraphrases files, and add a line to
`CATEGORIES` in `build_bank.py` with the next free block of numbers (e.g. 2000).
