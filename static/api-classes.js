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
	constructor(restaurants) {
		this.placeIds = restaurants['placeIds'];
		this.nextPageToken = restaurants['nextPageToken'];
	}
	static async getRestaurants() {
		const response = await fetch('/api/restaurants');
		const data = await response.json();
		const restaurantsList = new RestaurantsList(data);
		return restaurantsList;
	}
}
class Restaurant {
	constructor(restaurantObj) {
		this.id = restaurantObj.id;
		this.name = restaurantObj.name;
		this.address = restaurantObj.address;
		this.city = restaurantObj.city;
		this.state = restaurantObj.state;
	}
}
