class AreasList {
	constructor(areas) {
		this.areas = areas;
	}
	static async getAreas() {
		const response = await fetch('/api/areas');
		const data = await response.json();
		const areas = data.areas.map((area) => new Area(area));
		const areasList = new AreasList(areas);
		return areasList;
	}
}
class Area {
	constructor(areaObj) {
		this.id = areaObj.id;
		this.city = areaObj.city;
		this.latitude = areaObj.latitude;
		this.longitude = areaObj.longitude;
		this.state = areaObj.state;
		this.zipcode = areaObj.zipcode;
	}
}
class RestaurantsList {
	constructor({ place_ids, next_page_token }) {
		this.placeIds = place_ids;
		this.nextPageToken = next_page_token;
	}
	static async getRestaurants() {
		const response = await fetch('/api/restaurants');
		const data = await response.json();
		const restaurantsList = new RestaurantsList(data);

		return restaurantsList;
	}
	static async getMoreRestaurants(nextPageToken) {
		const dataBody = `{"next_page_token":"${nextPageToken}"}`;
		const response = await fetch('/api/restaurants/nextpage', {
			method  : 'POST',
			headers : {
				'Content-Type' : 'application/json'
			},
			body    : dataBody
		});
		const data = await response.json();

		const restaurantsList = new RestaurantsList(data);

		return restaurantsList;
	}
}

class RestaurantDetail {
	constructor({ name, address, google_place_id, photo_references }) {
		this.name = name;
		this.address = address;
		this.googlePlaceId = google_place_id;
		this.photo_references = photo_references;
	}
	static async getRestaurantDetail(restaurantPlaceId) {
		const dataBody = `{"restaurantPlaceId":"${restaurantPlaceId}"}`;
		const response = await fetch('/api/restaurant/details', {
			method  : 'POST',
			headers : {
				'Content-Type' : 'application/json'
			},
			body    : dataBody
		});
		const data = await response.json();
		const details = data.details;

		// const photos = details.photo_references.map((photo) => new Photo(photo));
		const restaurantDetail = new RestaurantDetail(details);

		return restaurantDetail;
	}
}
