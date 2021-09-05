import json
from collections import defaultdict


def create_task(subscriptons):
    tasks = defaultdict(list)
    for sub in subscriptons:
        key = json.dumps({"name": sub.user.username, "email": sub.user.email})
        sub_info = {}
        sub_info["service"] = sub.service
        sub_info["target_city"] = sub.target_city
        sub_info["city_of_departure"] = sub.city_of_departure
        tasks[key].append(sub_info)
    return tasks
