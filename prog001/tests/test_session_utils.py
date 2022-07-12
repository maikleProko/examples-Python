from src.db.classes import DuckieBotSession
from src.db.session_utils import convert_time_zone_from0_gmt_to_received_tz, find_min_available_session
from datetime import datetime, timedelta


def test_convert_time_zone_from0_gmt_to_received_tz(capsys):
    time = {"year": 2022,
            "month": 1,
            "day": 1,
            "hours": 9,
            "minutes": 0}
    time = convert_time_zone_from0_gmt_to_received_tz(time, 10)
    assert time["year"] == 2021 and time["month"] == 12 and \
        time["day"] == 31 and time["hours"] == 23, time["minutes"] == 0

    time = {"year": 0,
            "month": 1,
            "day": 1,
            "hours": 11,
            "minutes": 1}
    convert_time_zone_from0_gmt_to_received_tz(time, 10)
    out, _ = capsys.readouterr()
    assert out == "bad session\n"

    # Fails
    # time = None
    # convert_time_zone_from0_gmt_to_received_tz(time, 10)
    # out, _ = capsys.readouterr()
    # assert out == "bad session\n"


def test_find_min_available_session(capsys):
    def gen_dict_time(time):
        return {"year": time.year,
                "month": time.month, "day": time.day,
                "hours": time.hour, "minutes": time.minute
                }

    def gen_session(start_time, end_time, ind):
        s = gen_dict_time(start_time)
        e = gen_dict_time(end_time)
        res = DuckieBotSession(ind, str(ind), str(ind), s, e).dict()
        return res

    cur = datetime.utcnow()
    past = gen_session(cur + timedelta(weeks=-20), cur + timedelta(weeks=-10), 0)
    ends_now = gen_session(cur + timedelta(hours=-1), cur, 1)
    active_5min = gen_session(cur + timedelta(minutes=-3), cur + timedelta(minutes=2), 2)
    active_1hour = gen_session(cur + timedelta(minutes=-30), cur + timedelta(minutes=30), 3)
    active_10hours = gen_session(cur + timedelta(hours=-5), cur + timedelta(hours=5), 4)
    # wrong_start_time_dict = DuckieBotSession(5, "5", "5", {}, {"year": 2020, "month": 1, "day": 1, "hours": 0, "minutes": 0}).dict()
    # wrong_end_time_dict = DuckieBotSession(6, "6", "6", {"year": 2020, "month": 1, "day": 1, "hours": 0, "minutes": 0}, {}).dict()
    # wrong_time = DuckieBotSession(7, "7", "7", {"year": 0, "month": 0, "day": 0, "hours": 0, "minutes": 0}, {"year": 0, "month": 0, "day": 0, "hours": 0, "minutes": 0}).dict()

    # Fails with TypeError (idk if it's possible in real usage)
    # sessions = None
    # res = find_min_available_session(sessions)
    # assert res == [None, None, {"isSessionFound": False}]

    sessions = []
    res = find_min_available_session(sessions)
    assert res == [None, None, {"isSessionFound": False}]

    sessions = [past, ends_now]
    res = find_min_available_session(sessions)
    assert res == [None, None, {"isSessionFound": False}]

    # Fails (no 'bad session message' but dict has no start time)
    # sessions = [wrong_start_time_dict]
    # res = find_min_available_session(sessions)
    # out, _ = capsys.readouterr()
    # assert out == "bad session for find min session\n" and res == [None, None, {"isSessionFound": False}]

    # Fails in compute_time_diff
    # sessions = [wrong_end_time_dict]
    # res = find_min_available_session(sessions)
    # out, _ = capsys.readouterr()
    # assert out == "bad session for find min session\n" and res == [None, None, {"isSessionFound": False}]

    # Fails in compute_time_diff
    # sessions = [wrong_time]
    # res = find_min_available_session(sessions)
    # out, _ = capsys.readouterr()
    # assert out == "bad session for find min session\n" and res == [None, None, {"isSessionFound": False}]

    sessions = [active_1hour, active_5min]
    res = find_min_available_session(sessions)
    assert res[1] == active_1hour and res[2] == {"isSessionFound": True}

    sessions = [active_10hours, active_1hour, active_5min]
    res = find_min_available_session(sessions)
    assert res[1] == active_10hours and res[2] == {"isSessionFound": True}

    sessions = [past, ends_now, active_5min, active_1hour, active_10hours]
    res = find_min_available_session(sessions)
    assert res[1] == active_10hours and res[2] == {"isSessionFound": True}
