$(async () => {
	const restaurantsList = await RestaurantsList.getRestaurants();

	const likesDislikes = await getUserLikesDislikes();
	let filteredList = restaurantsList.placeIds.filter((restId) => likesDislikes.includes(restId) === false);

	let count = 0;
	let photoCount = 0;

	let restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
	handleRestaurantDetail(restaurantDetail);
	handlePhoto(restaurantDetail, photoCount);
	count += 1;

	$('.restaurant-normal').on('click', async () => {
		photoCount += 1;
		if (photoCount >= restaurantDetail.photo_references.length) {
			photoCount = 0;
		}
		handlePhoto(restaurantDetail, photoCount);
	});

	//Wait for a like/dislike from user
	$('.fas-container').on('click', async (event) => {
		if (count < filteredList.length) {
			if ($(event.target).hasClass('fa-times')) {
				handleDislike(restaurantDetail);
			} else if ($(event.target).hasClass('fa-heart')) {
				handleLike(restaurantDetail);
			}

			photoCount = 0;

			restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
			handleRestaurantDetail(restaurantDetail);
			handlePhoto(restaurantDetail, photoCount);
			count++;
		} else {
			// get an updated liked/disliked user_likes list filter
			count = 0;
			photoCount = 0;
			const newRestaurantsList = await RestaurantsList.getMoreRestaurants(restaurantsList.nextPageToken);
			const newLikesDislikes = await getUserLikesDislikes();
			filteredList = newRestaurantsList.placeIds.filter((restId) => newLikesDislikes.includes(restId) === false);
			restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
			handleRestaurantDetail(restaurantDetail);
			handlePhoto(restaurantDetail, photoCount);
			count += 1;
		}
	});
});
