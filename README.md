# g1-preparation

Ontario G1 knowledge test practice quiz: 203 multiple-choice questions, practice and exam modes, 80% to pass.

## Use

Open `quiz.html` in a browser.

## How the question bank is built

1. `capture.py` screenshots the study material into `screenshots/`.
2. `ocr.py` extracts questions and answers into `questions.csv` (macOS Vision).
3. `options.py` holds the correct answer wording and three wrong options per question.
4. `python3 build_bank.py` merges them into `question_bank.js`, which `quiz.html` loads.
