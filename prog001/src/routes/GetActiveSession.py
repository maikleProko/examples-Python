from flask import request
from flask_restful import Resource
from typing import Dict, Any
from db.session_utils import compute_dates_difference, find_min_available_session
from db.api import get_sessions_from_name


class GetActiveSession(Resource):
    # return {day, hours, minutes, isSessionFound} #isSessionFound - flag found or no any valid session
    def get(self) -> Dict[str, Any]:
        name: str = request.args.get("name")
        return findDiffTimeForTimer(name)


def findDiffTimeForTimer(userName) -> Dict[str, Any]:
    # find all sessions
    sessions = get_sessions_from_name(userName)
    current_dict, min_session, flag = find_min_available_session(sessions)
    if not flag['isSessionFound']:
        return flag
    diff_between_cur_time_and_start_min_session = compute_dates_difference(current_dict, min_session['start_time'])
    diff_between_cur_time_and_end_min_session = compute_dates_difference(current_dict, min_session['end_time'])
    # if session is active return time to END session
    if diff_between_cur_time_and_start_min_session['dif'] == 1:
        return_difference = diff_between_cur_time_and_end_min_session
        return_difference['session_is_active'] = True
    else:  # otherwise, return time to START session
        return_difference = diff_between_cur_time_and_start_min_session
        return_difference['session_is_active'] = False
    return_difference['isSessionFound'] = True
    return_difference['hostname'] = min_session['hostname']
    return_difference['id'] = min_session['id']
    return return_difference
