"""Routes for the course resource.
"""

from run import app
from flask import request,  jsonify
from http import HTTPStatus
import data
import json
import datetime

@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE

    ############## This is another method for search index #################
    # try:
    #     index = [ x['id'] for x in data.courses['data'] ].index(id)
    # except ValueError:
    #     return jsonify({'message':'Course ' + str(id) + ' does not exist'}), HTTPStatus.NOT_FOUND

    # res = {}
    # res['data'] = data.courses['data'][index]
    # return jsonify(res), HTTPStatus.OK

    ############## This is getting from binary search ##############
    index = data.search_id(data.courses['data'], id)
    if index > -1:
        res = {}
        res['data'] = data.courses['data'][index]
        return jsonify(res), HTTPStatus.OK
    else:
        return jsonify({'message':'Course ' + str(id) + ' does not exist'}), HTTPStatus.NOT_FOUND


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """

    allData = data.courses['data']
    totalData = data.courses['total']

    titles = request.args.get('title-words')
    if titles is not None:
        title_arr = titles.split(',')
        # x = data.JumpSearch(allData,title_arr)
        # return jsonify(x)
        allData = [x for x in allData if any(y in x['title'] for y in title_arr)]
        totalData = len(allData)

    page = request.args.get('page-number')
    if page is not None:
        try:
            page = int(request.args.get('page-number'))
        except:
            return jsonify({'message': 'Invalid parameter'}), HTTPStatus.BAD_REQUEST
    else:
        page = 1

    page_size = request.args.get('page-size')
    if page_size is not None:
        try:
            page_size = int(request.args.get('page-size'))
        except:
            return jsonify({'message': 'Invalid parameter'}), HTTPStatus.BAD_REQUEST
    else:
        page_size = 20
    
    paginate = data.pagination(page,page_size,totalData)

    if paginate == False:
        return jsonify({'message': 'Invalid page no.'}), HTTPStatus.BAD_REQUEST

    obj = {}
    obj['data'] = allData[paginate['start']:paginate['end']]
    obj['metadata'] = {
        "page_count": paginate['pages'],
        "page_number": page,
        "page_size": page_size,
        "record_count": totalData
    }

    return jsonify(obj), HTTPStatus.OK


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    if request.method == 'POST':
        obj = {}
        check_required = ['discount_price','on_discount','price','title']
        duplicate = ['title']
        minlength = ['title:5']
        maxlength = ['description:255','image_path:100','title:100']

        validation = data.validation(request.json,check_required,minlength,maxlength,duplicate,data.courses['data'],'')
        if validation['statuscode'] != HTTPStatus.OK:
            return jsonify(validation['error']), validation['statuscode']
        obj = request.json
        data.courses['total'] = data.courses['total'] + 1
        obj['id'] = data.courses['total']
        obj['date_created'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        obj['date_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        data.courses['data'].append(obj)
        res = {}
        res['data'] = obj
        return jsonify(res), HTTPStatus.CREATED
    
    return jsonify({'message':'Method Not Allowed'}), HTTPStatus.METHOD_NOT_ALLOWED


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    if request.method == 'PUT':
        try:
            index = [ x['id'] for x in data.courses['data'] ].index(id)
        except ValueError:
            return jsonify({'message':'The id does match the payload'}), HTTPStatus.BAD_REQUEST

        old_obj = data.courses['data'][index]
        obj = request.json
        obj['id'] = id
        check_required = ['discount_price','on_discount','price','title']
        duplicate = ['title']
        minlength = ['title:5']
        maxlength = ['description:255','image_path:100','title:100']
        validation = data.validation(obj, check_required,minlength,maxlength,duplicate,data.courses['data'],id)
        if validation['statuscode'] != HTTPStatus.OK:
            return jsonify(validation['error']), validation['statuscode']
        old_obj = obj
        old_obj['date_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        res = {}
        res['data'] = old_obj
        return jsonify(res), HTTPStatus.OK
    
    return jsonify({'message':'Method Not Allowed'}), HTTPStatus.METHOD_NOT_ALLOWED


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE

    if request.method == 'DELETE':
        try:
            index = [ x['id'] for x in data.courses['data'] ].index(id)
        except ValueError:
            return jsonify({'message':'Course ' + str(id) + ' does not exist'}), HTTPStatus.NOT_FOUND

        data.courses['data'].pop(index)
        return jsonify({'message':'The specified course was deleted'}), HTTPStatus.OK
    return jsonify({'message':'Method Not Allowed'}), HTTPStatus.METHOD_NOT_ALLOWED


