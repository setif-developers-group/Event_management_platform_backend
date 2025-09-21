from datetime import date, datetime
from zoneinfo import ZoneInfo
from app_models.models import Attendance

EVENT_START_DATE = date(2025, 9, 29)
EVENT_START_REGISTRATION = date(2025, 9, 25)


def get_registration_week_nuber():
    today = datetime.now(tz=ZoneInfo('Africa/Algiers')).date()

    if today < EVENT_START_DATE:
        return 1
    else:
        return ((today - EVENT_START_REGISTRATION).days // 7) + 1
    
def get_time_from_last_registration(attendance: Attendance):
    if attendance is None:
        return 24
    today = datetime.now(tz=ZoneInfo('Africa/Algiers')).date()
    return (today - attendance.attendance_date).hours