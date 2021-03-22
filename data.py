"""Routines associated with the application data.
"""
import os
from flask import Flask, json
from http import HTTPStatus
import math

courses = {}

def load_data():
    """Load the data from the json file.
    """
    root_path = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(root_path, "json", "course.json")
    data = json.load(open(json_url))
    courses['total'] = len(data)
    courses['data'] = data
    pass


def pagination(page,size,total):
    pages = math.ceil(total/size)

    if page < 1 or page > pages:
        return False

    start = (page - 1) * size
    end = page * size

    obj = {
        'pages' : pages,
        'start' : start,
        'end' : end
    }

    return obj


def validation(payload, req_feilds, minlength, maxlength, duplicate, data, id):
    res = {}
    errors = []
    for key, value in payload.items():
        if key in req_feilds:
            req_feilds.remove(key)
            if value == '' or value is None:
                res = {}
                res['error_message'] = key + " is invalid."
                res['feild_name'] = key
                errors.append(res)
        if key in duplicate:
            index = -1
            try:
                index = [ x[key] for x in data ].index(value)
            except ValueError:
                pass
            if index > -1:
                res = {}
                res['error_message'] = key + " is already present."
                res['feild_name'] = key
                errors.append(res)

        minindex = -1
        try:
            minindex = [ x.split(':')[0] for x in minlength ].index(key)
        except ValueError:
            pass
        if minindex > -1:
            if not int(len(value)) > int(minlength[minindex].split(':')[1]):
                res = {}
                res['error_message'] = key + " minimum length is "+ minlength[minindex].split(':')[1] +"."
                res['feild_name'] = key
                errors.append(res)

        maxindex = -1
        try:
            maxindex = [ x.split(':')[0] for x in maxlength ].index(key)
        except ValueError:
            pass
        if maxindex > -1:
            if not int(len(value)) < int(maxlength[maxindex].split(':')[1]):
                res = {}
                res['error_message'] = key + " maximum length is "+ maxlength[maxindex].split(':')[1] +"."
                res['feild_name'] = key
                errors.append(res)

    if len(req_feilds) > 0:
        for x in req_feilds:
            res = {}
            res['error_message'] = x + " is invalid."
            res['feild_name'] = x
            errors.append(res)

    if len(errors) > 0:
        res = {}
        res['statuscode'] = HTTPStatus.BAD_REQUEST
        res['error'] = errors
        return res
    res['statuscode'] = HTTPStatus.OK
    return res

def search_id(data,id):
    b_index = 0
    e_index = len(data) - 1

    while b_index <= e_index:
        mid = b_index + (e_index - b_index) // 2
        mid_val = data[mid]['id']
        if mid_val == id:
            return mid
        
        elif id < mid_val:
            e_index = mid - 1

        else:
            b_index = mid + 1

    return -1

