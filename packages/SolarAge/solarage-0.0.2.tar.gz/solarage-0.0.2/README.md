
# SolarAge

`SolarAge` is a Python package designed to provide detailed information about a person's birthday, including zodiac signs, animal years, age calculations, and season of birth. It supports conversions between the Persian (Jalali), Gregorian, and Islamic calendars.

## Features

- **Zodiac Sign**: Get the zodiac sign based on the Gregorian birthdate.
- **Animal Year**: Calculate the Chinese Zodiac animal year.
- **Birthstone**: Get the birthstone based on the Persian month.
- **Age Calculation**: Calculate a person's age in years, months, and days.
- **Season**: Determine the season of birth (Spring, Summer, Autumn, or Winter).
- **Moon Rotation**: Get the approximate number of moon rotations since the birthdate.
- **Date Conversions**: Convert birthdate between Persian, Gregorian, and Islamic calendars.
- **Days Until Next Birthday**: Calculate the number of days until the next birthday.

## Installation

You can install the package using `pip`:

```bash
pip install SolarAge
```

## Usage

Here's an example of how to use the `SolarAge` class:

```python
from SolarAge import BirthdayInfo

# Create an instance of BirthdayInfo with a Persian birthdate (year, month, day)
bd = BirthdayInfo(1386, 2, 3)

# Get detailed birthday information
info = bd.get_info()

# Print the information
print(info)
```

### Output Example:

```python
{
    "birthday": "3 Ordibehesht، 1386",
    "miladi": "2007 ، April 23",
    "ghamari": "1428 7 23",
    "age_years": 17,
    "age_months": 9,
    "age_days": 18,
    "total_days": "6,516",
    "week_day": "Saturday",
    "season": "Spring",
    "zodiac_sign": "Taurus",
    "animal_year": "Pig",
    "days_until_birthday": 52,
    "moon_rotation": 241,
}
```

## Dependencies

- `jdatetime`: For working with the Persian (Jalali) calendar.
- `convertdate`: For converting between Gregorian, Islamic, and Persian calendars.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Explanation:
1. **Features**: Describes the key features of your package.
2. **Installation**: Instructions to install the package via `pip`.
3. **Usage**: A code snippet demonstrating how to use the `SolarAge` class.
4. **Dependencies**: Lists the external libraries required for your package to function.
5. **License**: Optional section if you're including a license for the project.

