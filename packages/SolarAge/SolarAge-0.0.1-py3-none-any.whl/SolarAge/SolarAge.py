import jdatetime
import convertdate.islamic

class BirthdayInfo:
    ZODIAC_SIGNS = [
        (1, 19, "جدی"), (2, 18, "دلو"), (3, 20, "حوت"), (4, 19, "حمل"),
        (5, 20, "ثور"), (6, 20, "جوزا"), (7, 22, "سرطان"), (8, 22, "اسد"),
        (9, 22, "سنبله"), (10, 22, "میزان"), (11, 21, "عقرب"), (12, 21, "قوس")
    ]
    ANIMAL_YEARS = ["موش", "گاو", "ببر", "خرگوش", "اژدها", "مار", "اسب", "گوسفند", "میمون", "خروس", "سگ", "خوک"]
    BIRTHSTONES = {"آبان": "سیترین و یاقوت قرمز", "آذر": "فیروزه", "دی": "گارنت"}

    def __init__(self, year, month, day):
        self.sh_date = jdatetime.date(year, month, day)
        self.today = jdatetime.date.today()
        self.gregorian_date = self.sh_date.togregorian()
        self.ghamari_date = convertdate.islamic.from_gregorian(self.gregorian_date.year, self.gregorian_date.month, self.gregorian_date.day)
        
    def get_zodiac_sign(self):
        month, day = self.gregorian_date.month, self.gregorian_date.day
        for m, d, sign in self.ZODIAC_SIGNS:
            if (month == m and day <= d) or (month == m - 1 and day > d):
                return sign
        return ""  
    
    def get_animal_year(self):
        return self.ANIMAL_YEARS[(self.gregorian_date.year + 8) % 12]

    
    def calculate_age(self):
        delta = self.today - self.sh_date
        age_years = delta.days // 365
        age_months = (delta.days % 365) // 30
        age_days = (delta.days % 365) % 30
        return age_years, age_months, age_days, delta.days

    def days_until_next_birthday(self):
        next_birthday = jdatetime.date(self.today.year, self.sh_date.month, self.sh_date.day)
        if next_birthday < self.today:
            next_birthday = jdatetime.date(self.today.year + 1, self.sh_date.month, self.sh_date.day)
        return (next_birthday - self.today).days

    def get_season(self):
        if 1 <= self.sh_date.month <= 3:
            return "بهار"
        elif 4 <= self.sh_date.month <= 6:
            return "تابستان"
        elif 7 <= self.sh_date.month <= 9:
            return "پاییز"
        else:
            return "زمستان"
    
    def get_info(self):
        age_years, age_months, age_days, total_days = self.calculate_age()
        return {
            "birthday": f"{self.sh_date.day} {self.sh_date.strftime('%B')}، {self.sh_date.year}",
            "miladi": f"{self.gregorian_date.year} ، {self.gregorian_date.strftime('%B')}  {self.gregorian_date.day}",
            "ghamari": f"{self.ghamari_date[0]} {self.ghamari_date[1]} {self.ghamari_date[2]}",
            "age_years": age_years,
            "age_months": age_months,
            "age_days": age_days,
            "total_days": f"{total_days:,}",
            "week_day": self.sh_date.strftime('%A'),
            "season": self.get_season(), 
            "zodiac_sign": self.get_zodiac_sign(),
            "animal_year": self.get_animal_year(),
            "days_until_birthday": self.days_until_next_birthday(),
            "moon_rotation": total_days // 27,
        }
