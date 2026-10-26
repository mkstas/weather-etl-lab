import logging

from sqlalchemy.orm import Session

from db_models import WeatherForecast


HEADERS = [
    "Дата",
    "Мин. темп. (°C)",
    "Макс. темп. (°C)",
    "Описание",
    "Влажность (%)",
    "Ветер (м/с)",
]


def _fmt_number(number):
    rounded = round(float(number), 1)
    return f"{rounded:.1f}"


def _fmt_row(cells, widths):
    padded = [str(cell).ljust(widths[i]) for i, cell in enumerate(cells)]
    return "| " + " | ".join(padded) + " |"


def _build_table(rows):
    data = [
        [
            row.forecast_date.isoformat(),
            _fmt_number(row.temp_min),
            _fmt_number(row.temp_max),
            row.description.replace("|", "\\|").capitalize(),
            row.humidity,
            _fmt_number(row.wind_speed),
        ]
        for row in rows
    ]

    widths = [len(header) for header in HEADERS]

    for cells in data:
        for i, cell in enumerate(cells):
            widths[i] = max(widths[i], len(str(cell)))

    separator = "|" + "|".join("-" * (width + 2) for width in widths) + "|"
    lines = [_fmt_row(HEADERS, widths), separator]
    lines += [_fmt_row(cells, widths) for cells in data]
    return "\n".join(lines)


def export_to_markdown(engine, city):
    with Session(engine) as session:
        weather_rows = session.query(WeatherForecast).all()

    rows = sorted(
        (row for row in weather_rows if row.city == city),
        key=lambda row: row.forecast_date
    )
    rows = rows[-4:]

    if not rows:
        logging.warning(f"No forecast data for {city} to export")
        return

    period = f"{rows[0].forecast_date.isoformat()} - {rows[-1].forecast_date.isoformat()}"

    content = (
        "# Прогноз погоды\n\n"
        f"Автоматически определённая локация: {city}\n\n"
        f"Период: {period}\n\n"
        f"{_build_table(rows)}\n"
    )

    with open("weather_report.md", "w", encoding="utf-8") as file:
        file.write(content)

    logging.info("Weather forecast exported in weather_report.md")
