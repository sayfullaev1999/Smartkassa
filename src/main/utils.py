def extract_birthdate_and_gender(pinfl):
    if len(pinfl) != 14 or not pinfl.isdigit():
        return None, None

    day = int(pinfl[1:3])
    month = int(pinfl[3:5])
    year_suffix = int(pinfl[5:7])

    year = 1900 + year_suffix if year_suffix > 30 else 2000 + year_suffix
    birthdate = f"{year}-{month:02d}-{day:02d}"
    gender = "Мужской" if int(pinfl[-1]) % 2 else "Женский"

    return birthdate, gender
