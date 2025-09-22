# Тестовое задание на стажировку АВИТО

HF Model Link: [mbart-large-50-spaces](https://huggingface.co/Dropdead072/mbart-large-50-spaces)

### Computational Power

CUDA: 12.6

GPU: NVIDIA GeForce RTX 3060 Laptop GPU

## Structure



├── data/

│   └── dataset\_1937770\_3.txt      # тестовый датасет из Stepik

├── mbart-space-fix/               # локальные чекпоинты обученной модели (не загружаются в GitHub)

├── train\_model\_data/

│   └── wiki\_dataset.csv           # собранный датасет (Wiki + синтетика)

├── .gitignore

├── README.md

├── basic\_functions.ipynb          # эксперименты с функциями предобработки

├── data\_collection.py             # функции для формирования датасета `wiki_dataset.csv`

├── model\_test.ipynb               # тестирование обученной модели (загрузка из локальной папки)

├── model\_train.ipynb              # обучение модели для задачи расстановки пробелов

├── processing.py                   # базовые функции обработки (эвристика, индексы пробелов, чтение .txt)

└── scorer.py                      # локальная функция подсчёта F1




