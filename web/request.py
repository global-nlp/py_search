# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/30 19:30
# Description: 提供RESTFUL风格接口
# -----------------------------------------------------------------------#

from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

from handle.search import Search
from utils.constant import SUCCESS, NOT_EXIST, EXIST

# 创建一个flask应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)


class SearchView(Resource):
    def get(self):
        """
            /query/_search 查询最新的10条
            /query/_search?limit=5 查询最新的5条
            /query/_search?key=相信 根据关键词查询
        Returns:

        """
        req_parses = reqparse.RequestParser()
        req_parses.add_argument('key', type=str)
        req_parses.add_argument('limit', type=int, help='type of limit is int')
        args = req_parses.parse_args()
        search = Search()
        if args['key'] is None:
            if args['limit']:
                query_records = search.search(args['limit'])
            else:
                query_records = search.search()
        else:
            query_records = search.search_by_key(args['key'])
        result = {"code": SUCCESS, "data": query_records}
        return jsonify(result)


class QueryView(Resource):
    """
        /query/<data_id> 接口 GET、PUT、POST、DELETE、PUT
    """
    def get(self, data_id):
        search = Search()
        query_records = search.search_by_id(data_id)
        result = {"code": SUCCESS, "data": query_records}
        return jsonify(result)

    def post(self, data_id):
        args = self.get_args_from_request()
        search = Search()
        head = search.head(data_id)
        if NOT_EXIST == head:
            data_id = search.add(data_id, args['query'], args['answer'])
            result = {"code": SUCCESS, "msg": "insert successfully", "data": {"data_id": data_id}}
        else:
            result = {"code": EXIST, "msg": "This id already exist"}
        return jsonify(result)

    def put(self, data_id):
        args = self.get_args_from_request()
        search = Search()
        data_id = search.add(data_id, args['query'], args['answer'])
        result = {"code": SUCCESS, "msg": "insert successfully", "data": {"data_id": data_id}}
        return jsonify(result)

    def get_args_from_request(self):
        req_parses = reqparse.RequestParser()
        req_parses.add_argument('query', required=True, nullable=False, type=str, help='missing a param.')
        req_parses.add_argument('answer', required=True, nullable=False, type=str, help='missing a param.')
        args = req_parses.parse_args()
        return args

    def delete(self, data_id):
        search = Search()
        result = search.delete(data_id)
        if SUCCESS.__eq__(result):
            result = {"code": SUCCESS, "msg": "delete successfully"}
        else:
            result = {"code": NOT_EXIST, "msg": "This id not exist."}
        return jsonify(result)

    def head(self, data_id):
        """
            判断指定id是否存在
        Args:
            data_id:

        Returns:

        """
        search = Search()
        exist = search.head(data_id)
        if NOT_EXIST == exist:
            result = {"code": NOT_EXIST, "msg": "This id not exist."}
            response = make_response(jsonify(result), 404)
            return response
        result = {"code": SUCCESS, "msg": "This id exist."}
        response = make_response(jsonify(result))
        return response


# endpoint 表示api路径
api.add_resource(SearchView, '/query/_search', endpoint='search')
api.add_resource(QueryView, '/query/<data_id>', endpoint='query')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug='false')
