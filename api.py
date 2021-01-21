from flask import Blueprint, render_template, jsonify, request,g,session
from helpers import place_search_request , google_details_request, google_photo_request, google_next_page
from models import db, User,Likes, Dislikes, Restaurant, Area, UserAreas
api = Blueprint("api", __name__, static_folder="static",template_folder="templates")

# prefix = /api
#maybe implement a @api.before_request for authenticated users only! to make more DRY

@api.route('/areas', methods=["GET"])
def get_user_areas():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    user = User.query.get_or_404(g.user.id)
    serialized = [area.serialize() for area in user.areas]
    return jsonify(areas=serialized)

@api.route('/restaurants')
def get_restaurants_in_area():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    area = Area.query.get_or_404(session['curr_area'])
    response = place_search_request(latitude=area.latitude,longitude=area.longitude)
    
    return jsonify(response)

@api.route('/restaurants/nextpage', methods=['POST'])
def get_nextpage():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    page_token= request.json['next_page_token']

    response = google_next_page(pagetoken=page_token)
    return jsonify(response)
    # return jsonify({"test":"test"})


@api.route('/restaurant/details', methods=['POST'])
def get_restaurant_details():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401    
    place_id = request.json['restaurantPlaceId']
    response = google_details_request(place_id=place_id)
    return jsonify(response)

@api.route('/restaurant/details/photo', methods=['POST'])
def get_photo():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    photo_reference = request.json['photo_reference']
    response = google_photo_request(photo_reference=photo_reference)
    return jsonify(response)

@api.route('/restaurant/like', methods=["POST"])
def like_restaurant():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    google_place_id = request.json['googlePlaceId']
    name = request.json['name']
    address = request.json['address']
    
    # will need parse out seen restaurants.
    area_id = session['curr_area']
    matched=None
    if matched: 
        like = Likes.query.get(matched.id)
        db.session.delete(like)
    else:
        restaurant = Restaurant(name=name,address=address,google_place_id=google_place_id,user_id=g.user.id,area_id=area_id)
        db.session.add(restaurant)
        db.session.commit()
        like = Likes(user_id=g.user.id, restaurant_id=restaurant.id)
        db.session.add(like)
    db.session.commit()

    return jsonify({"restaurant":"liked"})

@api.route('/restaurant/dislike',methods=['POST'])
def dislike_restaurant():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    google_place_id = request.json['googlePlaceId']
    name = request.json['name']
    address = request.json['address']
    area_id = session['curr_area']
    #what am i doing with matched again? also fix it for like_restauerant
    matched=None
    if matched: 
        like = Likes.query.get(matched.id)
        db.session.delete(like)
    else:
        restaurant = Restaurant(name=name,address=address,google_place_id=google_place_id,user_id=g.user.id,area_id=area_id)
        db.session.add(restaurant)
        db.session.commit()
        dislike = Dislikes(user_id=g.user.id, restaurant_id=restaurant.id)
        db.session.add(dislike)
    db.session.commit()
    return jsonify({"restaurant":"disliked"})
    
@api.route('/user/likes', methods=['POST'])
def get_user_likes():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    # query DB to get list of all user likes.
    user = User.query.get_or_404(g.user.id)
    user_likes = [restaurant.google_place_id for restaurant in user.likes]
    user_dislikes = [restaurant.google_place_id for restaurant in user.dislikes]
    
    return jsonify({"likes":user_likes,"dislikes":user_dislikes})

@api.route('/likes')
def get_user_likes_test():
    if not g.user:
        return jsonify({"message":"Unauthorized"}),401
    user = User.query.get_or_404(g.user.id)
    serialized = [restaurant.serialize() for restaurant in user.likes]

    return jsonify(restaurant_likes=serialized)