from flask import Blueprint, render_template, jsonify, request,g,session
from helpers import place_search_request
from secrets import PRIVATE_API_KEY
from models import db, User,Likes, Dislikes, Restaurant, Area, UserAreas
api = Blueprint("api", __name__, static_folder="static",template_folder="templates")

# prefix = /api

@api.route('/areas', methods=["GET"])
def get_user_areas():
    user = User.query.get_or_404(g.user.id)
    serialized = [area.serialize() for area in user.areas]
    return jsonify(areas=serialized)

@api.route('/restaurants')
def get_restaurants_in_area():
    
    area = Area.query.get_or_404(session['curr_area'])
    response = place_search_request(latitude=area.latitude,longitude=area.longitude,key=PRIVATE_API_KEY)
    return jsonify(response)