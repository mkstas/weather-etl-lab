# Weather ETL Lab

Скрипт для получения, агрегации и экспорта прогноза погоды по текущему местоположению.

## Описание проекта

Программа автоматически определяет город по IP-адресу через [ipinfo.io](https://ipinfo.io/), запрашивает прогноз погоды с [OpenWeatherMap Forecast API 2.5](https://openweathermap.org/forecast5), агрегирует почасовые данные по дням, сохраняет их в локальную базу данных SQLite и формирует Markdown-отчёт с прогнозом за **последние 4 дня**.

## Технологии и API

| Инструмент                                                                  | Назначение                       |
| --------------------------------------------------------------------------- | -------------------------------- |
| **[Python](https://www.python.org/)**                                       | Основной язык разработки         |
| **[SQLite](https://www.sqlite.org/)**                                       | Локальная база данных            |
| **[SQLAlchemy](https://www.sqlalchemy.org/)**                               | ORM для работы с базой данных    |
| **[requests](https://pypi.org/project/requests/)**                          | Выполнение HTTP-запросов         |
| **[python-dotenv](https://pypi.org/project/python-dotenv/)**                | Работа с переменными окружения   |
| **[ipinfo.io](https://ipinfo.io/)**                                         | Определение местоположения по IP |
| **[OpenWeatherMap Forecast API 2.5](https://openweathermap.org/forecast5)** | Получение прогноза погоды        |

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/mkstas/weather-etl-lab.git
cd weather-etl-lab
```

### 2. Создание и активация виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## Настройка

### 1. Создание файла `.env`

Скопируйте шаблон `.env.example` в `.env`:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

### 2. Получение API-ключа OpenWeatherMap

1. Зарегистрируйтесь на [openweathermap.org](https://openweathermap.org/).
2. Перейдите в раздел `API keys` в личном кабинете.
3. Сгенерируйте бесплатный ключ для **Forecast API 2.5**.

### 3. Заполнение конфигурации

Откройте файл `.env` и укажите значения:

```env
GEO_API_FALLBACK_CITY=Moscow
WEATHER_FORECAST_API_KEY=your_api_key
```

> При первом запуске автоматически создастся файл `weather_lab.db` со структурой таблицы `weather_forecast`.

## Запуск

```bash
python main.py
```

После выполнения программы в корне проекта появится файл `weather_report.md` с актуальным прогнозом.

## Структура проекта

| Файл                | Описание                                                                          |
| ------------------- | --------------------------------------------------------------------------------- |
| `main.py`           | Точка входа. Координирует весь процесс.                                           |
| `geo_locator.py`    | Определение города по IP-адресу с помощью [ipinfo.io](https://ipinfo.io/).        |
| `weather_client.py` | Взаимодействие с OpenWeatherMap API.                                              |
| `db_models.py`      | Описание ORM-моделей SQLAlchemy.                                                  |
| `exporter.py`       | Формирование и выгрузкатаблицы прогноза за последние 4 дня в `weather_report.md`. |
| `.env.example`      | Шаблон для файла конфигурации `.env`.                                             |
| `requirements.txt`  | Список зависимостей проекта.                                                      |

## Пример ожидаемого вывода

### Консольный вывод

```text
[2026-10-26 17:21:31] [INFO]: Current location - Kirov
[2026-10-26 17:21:33] [INFO]: Weather forecast for Kirov saved
[2026-10-26 17:21:33] [INFO]: Weather forecast exported in weather_report.md
```

### Файл `weather_report.md`

```markdown
# Прогноз погоды

Автоматически определённая локация: Kirov

Период: 2026-10-26 - 2026-10-29

| Дата       | Мин. темп. (°C) | Макс. темп. (°C) | Описание        | Влажность (%) | Ветер (м/с) |
| ---------- | --------------- | ---------------- | --------------- | ------------- | ----------- |
| 2026-10-26 | 2.0             | 3.5              | Ясно            | 76            | 3.1         |
| 2026-10-27 | 1.8             | 4.2              | Облачно         | 72            | 2.8         |
| 2026-10-28 | 0.5             | 3.7              | Небольшой дождь | 81            | 4.0         |
| 2026-10-29 | -1.2            | 2.4              | Пасмурно        | 78            | 3.4         |
```
