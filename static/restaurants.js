$(async () => {
	let restaurantsList;
	let likesDislikes;
	let filteredList;
	let restaurantDetail;
	let count = 0;
	let photoCount = 0;

	try {
		restaurantsList = await RestaurantsList.getRestaurants();
		likesDislikes = await getUserLikesDislikes();
		filteredList = restaurantsList.placeIds.filter((restId) => likesDislikes.includes(restId) === false);
		restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
		handleRestaurantDetail(restaurantDetail);
		handlePhoto(restaurantDetail, photoCount);
	} catch (e) {
		alert('Unable to fetch data from Google or connect to Database');
		console.log(e);
	}

	count += 1;

	$('.restaurant-normal').on('click', async () => {
		photoCount += 1;
		if (photoCount >= restaurantDetail.photo_references.length) {
			photoCount = 0;
		}
		try {
			handlePhoto(restaurantDetail, photoCount);
		} catch (e) {
			alert('Unable to get photo from google.');
			console.log(e);
		}
	});

	//Wait for a like/dislike from user
	$('.fas-container').on('click', async (event) => {
		if (count < filteredList.length) {
			if ($(event.target).hasClass('fa-times')) {
				try {
					handleDislike(restaurantDetail);
				} catch (e) {
					console.log('Unable to send dislike to database');
				}
			} else if ($(event.target).hasClass('fa-heart')) {
				try {
					handleLike(restaurantDetail);
				} catch (e) {
					console.log('Unable to send like to database');
					console.log(e);
				}
			}

			photoCount = 0;
			try {
				restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
				handleRestaurantDetail(restaurantDetail);
				handlePhoto(restaurantDetail, photoCount);
			} catch (e) {
				alert('Unable to get next restaurant from Google');
				console.log(e);
			}
			count++;
		} else {
			// get an updated liked/disliked user_likes list filter
			count = 0;
			photoCount = 0;
			let newRestaurantsList;
			let newLikesDislikes;
			try {
				newRestaurantsList = await RestaurantsList.getMoreRestaurants(restaurantsList.nextPageToken);
				newLikesDislikes = await getUserLikesDislikes();
				filteredList = newRestaurantsList.placeIds.filter(
					(restId) => newLikesDislikes.includes(restId) === false
				);
				restaurantDetail = await RestaurantDetail.getRestaurantDetail(filteredList[count]);
				handleRestaurantDetail(restaurantDetail);
				handlePhoto(restaurantDetail, photoCount);
			} catch (e) {
				alert('Unable to get new page from google');
				console.log(e);
			}
			count += 1;
		}
	});
});
