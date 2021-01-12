$(async function() {
	console.log('inside restaurant');
	const restaurantsList = await RestaurantsList.getRestaurants();
	console.log(restaurantsList);
});
