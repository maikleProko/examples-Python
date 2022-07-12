from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
import math


def convert_time_zone_from0_gmt_to_received_tz(datetime1: dict, delta_tz=0) -> Dict[str, Any]:
    try:
        date = datetime(datetime1["year"], datetime1["month"], datetime1["day"], datetime1["hours"], datetime1["minutes"])
        date = date + timedelta(hours=-int(delta_tz))
        datetime1["day"] = date.day
        datetime1["month"] = date.month
        datetime1["year"] = date.year
        datetime1["hours"] = date.hour
        datetime1["minutes"] = date.minute
    except ValueError:
        print('bad session')
    return datetime1


def convert_tz_and_sort_sessions(sessions: List[dict], delta_tz=0) -> List[dict]:
    for i in range(len(sessions)):
        sessions[i]["start_time"] = convert_time_zone_from0_gmt_to_received_tz(sessions[i]["start_time"], delta_tz)
        sessions[i]["end_time"] = convert_time_zone_from0_gmt_to_received_tz(sessions[i]["end_time"], delta_tz)
    return sessions


def compute_dates_difference(datatime2: dict, datatime1: dict, tz2=0, tz1=0) -> Dict[str, Any]:
    dif = {}
    date1 = datetime(int(datatime1['year']), int(datatime1['month']), int(datatime1['day']), int(datatime1['hours']), int(datatime1['minutes']), tzinfo=timezone(timedelta(hours=tz1)))
    date2 = datetime(int(datatime2['year']), int(datatime2['month']), int(datatime2['day']), int(datatime2['hours']), int(datatime2['minutes']), tzinfo=timezone(timedelta(hours=tz2)))
    if date1 > date2:
        diff_time = date1 - date2
        dif['dif'] = -1
    elif date1 < date2:
        diff_time = date2 - date1
        dif['dif'] = 1
    else:
        diff_time = date1 - date2
        dif['dif'] = 0
    diff_minutes = math.floor(diff_time.total_seconds() / 60)  # convert to minutes
    dif['day'] = math.floor(diff_minutes / (60 * 24))
    dif['hours'] = math.floor((diff_minutes - dif['day'] * (60 * 24)) / 60)
    dif['minutes'] = math.floor(diff_minutes - dif['day'] * (60 * 24) - dif['hours'] * 60)
    return dif


def find_min_available_session(sessions) -> List:
    local_session_flag = False  # find or no min session
    # check count of sessions
    if len(sessions) > 0:
        # get utc time to compute difference
        current_client_time = datetime.utcnow()
        current_dict = {"year": current_client_time.year,
                        "month": current_client_time.month, "day": current_client_time.day,
                        "hours": current_client_time.hour, "minutes": current_client_time.minute
                        }
        min_session = {}
        # find any valid session
        for ind in range(len(sessions)):
            try:
                if compute_dates_difference(sessions[ind]['end_time'], current_dict)['dif'] == 1:
                    min_session = sessions[ind]
                    local_session_flag = True
                    break
            except ValueError:
                print("bad session for find min session")
                continue
        if local_session_flag:
            # find the first min session
            for ind in range(len(sessions)):
                try:
                    if compute_dates_difference(current_dict, sessions[ind]['end_time'])['dif'] == -1 and \
                            (compute_dates_difference(sessions[ind]['start_time'], min_session['start_time'])['dif'] == -1 or
                             compute_dates_difference(sessions[ind]['start_time'], min_session['start_time'])['dif'] == 0):
                        min_session = sessions[ind]
                except ValueError:
                    print("bad session for find min session")
                    continue

            return [current_dict, min_session, {"isSessionFound": True}]
        else:
            return [None, None, {"isSessionFound": False}]
    else:
        return [None, None, {"isSessionFound": False}]
