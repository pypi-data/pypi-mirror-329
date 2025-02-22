from datetime import datetime
from convertdate import persian




########################################################################################################################
########################################################################################################################

def remaining_days(shamsi_date: str) -> int:
    """
    Calculate the number of days remaining from the given Persian (Shamsi) date to the current Gregorian date.

    This function performs the following steps:
    1. Removes the weekday name from the Persian date string.
    2. Converts Persian digits to English digits.
    3. Splits the Persian date into day, month, and year components.
    4. Converts the Persian date to the Gregorian (Miladi) date.
    5. Calculates and returns the absolute number of days remaining between the given date and today's date.

    Args:
        shamsi_date (str): A Persian date in the format 'Weekday day month year' (e.g., "سه شنبه ۲۴ تیر ۱۴۰۴").

    Returns:
        int: The absolute number of days remaining until the provided date. If the provided date is in the future,
             the number will be positive; if it is in the past, it will also be positive due to the use of absolute value.

    Example:
        >>> remaining_days("سه شنبه ۲۴ تیر ۱۴۰۴")
        700  # This will return the number of days from the given Persian date to today's date.

    Notes:
        - The function assumes the Persian date is in the 'Weekday day month year' format.
        - The weekday is removed for accurate date conversion.
        - If the date is in the future, the function will return a positive number of days.
    """
    # 1. حذف روز هفته از تاریخ شمسی
    def remove_weekday(shamsi_date: str) -> str:
        weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        for day in weekdays:
            if shamsi_date.startswith(day):
                return shamsi_date.replace(day, '', 1).strip()
        return shamsi_date
    
    # 2. تبدیل اعداد فارسی به انگلیسی
    def persian_to_english_number(persian_num: str) -> str:
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        translation_table = str.maketrans(persian_digits, english_digits)
        return persian_num.translate(translation_table)
    
    # 3. تقسیم تاریخ به سال، ماه و روز
    def split_date_parts(cleaned_date: str):
        persian_months = {
            "فروردین": 1, "اردیبهشت": 2, "خرداد": 3,
            "تیر": 4, "مرداد": 5, "شهریور": 6,
            "مهر": 7, "آبان": 8, "آذر": 9,
            "دی": 10, "بهمن": 11, "اسفند": 12
        }
        parts = cleaned_date.split()
        day = persian_to_english_number(parts[0])          # روز
        month = persian_months[parts[1]]                   # ماه
        year = persian_to_english_number(parts[2])          # سال
        return int(year), int(month), int(day)
    
    # 4. تبدیل تاریخ شمسی به میلادی
    def shamsi_to_miladi(year: int, month: int, day: int) -> str:
        g_year, g_month, g_day = persian.to_gregorian(year, month, day)
        miladi_date = datetime(g_year, g_month, g_day).strftime("%Y-%m-%d")
        return miladi_date
    
    # 5. محاسبه فاصله روزانه تا تاریخ میلادی
    def calculate_days_difference(miladi_date: str) -> int:
        current_date = datetime.now()
        target_date = datetime.strptime(miladi_date, "%Y-%m-%d")
        delta = current_date - target_date
        return abs(delta.days)  # استفاده از مقدار مطلق برای مثبت بودن خروجی
    
    # مراحل انجام کار
    cleaned_date = remove_weekday(shamsi_date)  # حذف روز هفته
    year, month, day = split_date_parts(cleaned_date)  # تقسیم تاریخ به اجزاء
    miladi_date = shamsi_to_miladi(year, month, day)  # تبدیل به میلادی
    return calculate_days_difference(miladi_date)  # محاسبه فاصله روزانه

