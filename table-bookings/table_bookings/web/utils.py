import uuid
import hashlib
from .models import RestaurantTable


def create_email_key(user_id):
    random_key = str(uuid.uuid4())
    sha_data = hashlib.sha256()
    sha_data.update(str(user_id).encode("utf-8"))
    hash_key = sha_data.hexdigest()

    return random_key[::2] + hash_key


def convert_weekday(weekday_value: int) -> str:
    if weekday_value == 0:
        return RestaurantTable.Weekday.MONDAY
    elif weekday_value == 1:
        return RestaurantTable.Weekday.TUESDAY
    elif weekday_value == 2:
        return RestaurantTable.Weekday.WEDNESDAY
    elif weekday_value == 3:
        return RestaurantTable.Weekday.THURDAY
    elif weekday_value == 4:
        return RestaurantTable.Weekday.FRIDAY
    elif weekday_value == 5:
        return RestaurantTable.Weekday.SATURDAY
    elif weekday_value == 6:
        return RestaurantTable.Weekday.SUNDAY
