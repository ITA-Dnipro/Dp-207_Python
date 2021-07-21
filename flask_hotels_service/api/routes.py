from flask import Blueprint, request, jsonify, abort
from parser import ScraperForHotel
from marshmallow import Schema, fields, validate
from utils.api_jwt import check_token


# create schema for hotel responce
class HotelSchema(Schema):
    hotel_name = fields.Str(required=True, validate=validate.Length(max=100))
    city = fields.Str(required=True, validate=validate.Length(max=100))
    adress = fields.Str(required=True)
    photo = fields.Str()
    detail = fields.Str()
    prices = fields.Dict()
    contacts = fields.Str()


hotels_schema = HotelSchema(many=True)
hotel_schema = HotelSchema()

# create blueprint for api
api_blu = Blueprint('api', __name__, url_prefix='/api')


# create endpoint to get all hotels by city
@api_blu.route('/get_all_hotels', methods=['POST'])
def get_all_hotels():
    # check and validate jwt token
    if check_token(request.headers['Authorization']):
        if not request.get_json():
            return abort(400)

        # get data from parser
        data = ScraperForHotel(request.get_json()['city']).parse()
        result = hotels_schema.loads(data)
        return jsonify(result), 200
    else:
        return jsonify({'msg': 'invalid token'}), 400


# @api_blu.route('/get_hotel', methods=['POST'])
# def get_hotel():
#     print(request.get_json())
#     if not request.get_json() or not 'title' in request.get_json():
#         return abort(400)
#     hotels = [
#         {"title": "Kreshatik", "city": "Kiev"},
#         {"title": "Palace", "city": "Dnipro"},
#         {"title": "Owel", "city": "Dnipro"}]
#
#     for data in hotels:
#         if request.get_json()['title'] == data['title']:
#             hotel_result = {"title": data['title'], "city": data['city']}
#             result = hotel_schema.dump(hotel_result)
#             return jsonify({'hotel': result})
