import datetime


def parse_birth_date(pinfl: str | None) -> str | None:
    """https://lex.uz/ru/docs/5955669"""
    if pinfl:
        century_index = int(pinfl[0])
        day = int(pinfl[1:3])
        month = int(pinfl[3:5])
        year_offset = int(pinfl[5:7])

        if century_index in [1, 2]:
            year = 1800 + year_offset
        elif century_index in [3, 4]:
            year = 1900 + year_offset
        elif century_index in [5, 6]:
            year = 2000 + year_offset
        else:
            raise ValueError("Некорректный индекс века в ПИНФЛ")

        try:
            birthdate = datetime.date(year, month, day)
        except ValueError:
            raise ValueError("Некорректная дата рождения в ПИНФЛ")

        return birthdate.strftime("%Y-%m-%d")
