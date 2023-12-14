# Формализация текста

## Хакатон: задача от Mandarin 

## Группа 4

Состав группы:

- Dmitrii-Krasnov: Дмитрий Краснов
- svwk: Светлана Савоськина
- GLOBB1000: Артем Солодухин
- AFK0: Витченко Сергей

## Описание проекта

Оценка возможности одобрения кредита банками заданному клиенту

В решении используется модель дерева решений библиотеки XGBoost XGBClassifier https://xgboost.readthedocs.io/en/stable/

XGBoost (eXtreme gradient boosting) - известный и мощный инструмент машинного обучения, 
обычно используемый для задач контролируемого обучения, таких как классификация, регрессия и ранжирование.
Он построен на архитектуре gradient boosting и приобрел популярность благодаря своей высокой точности и масштабируемости.

## Использованные технологии

- pandas>=2.1.3
- scikit-learn>=1.3.0
- pyyaml>=6.0.0
- python-dateutil>=2.8.2
- numpy>=1.26.0
- joblib~=1.3.2
- xgboost~=2.0.2
- dvc>=3.30.3
- fastapi>=0.95.1
- uvicorn>=0.21.1
- pydantic>=2.5.0

## Установка

- Для установки зависимостей для сервера, выполните команду:

  `pip install -r requirements.txt`

## Использование

- Для запуска выполните:

`uvicorn api.api:app --reload`

- Для работы с приложением перейдите по ссылке:
  http://127.0.0.1:8000/docs

- Откроется окно swagger, в котором есть два роута (метода):
    - Роут "/" покажет описание проекта.
    - Роут "/predict" предсказывает одобрения банками заявки клиента.