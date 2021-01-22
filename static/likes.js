$(async () => {
	// on document load
	// do stuff
	let photoCount = 0;
	let placeId = null;
	let restaurantDetail = null;
	const userLikes = await getUserLikes();

	$('#likes-table').append(generateLikesTable());
	populateLikesTable(userLikes);

	$('#likes-table').on('click', '.like-row', async () => {
		placeId = $(this).data('place');
		restaurantDetail = await RestaurantDetail.getRestaurantDetail(placeId);
		handleRestaurantDetail(restaurantDetail);
		handlePhoto(restaurantDetail, photoCount);

		toggleViews();
	});

	$('.unlike').on('click', () => {
		handleUnlike(placeId);
		location.reload();
	});
	$('.go-back').on('click', () => {
		photoCount = 0;
		toggleViews();
		changeImgToLoad();
	});

	$('.restaurant-normal').on('click', () => {
		photoCount += 1;
		if (photoCount >= restaurantDetail.photo_references.length) {
			photoCount = 0;
		}
		handlePhoto(restaurantDetail, photoCount);
	});
	$('.fas').on('click', (event) => {
		const direction = $(event.target).hasClass('fa-sort-down') ? 'down' : 'up';
		const idSortBy = $(event.target).attr('id');
		const sortedLikes = sortBy(userLikes['restaurant_likes'], idSortBy, direction);
		const sortedRestaurants = { restaurant_likes: sortedLikes };

		$('.likes').empty();

		populateLikesTable(sortedRestaurants);
		$(event.target).toggleClass('fa-sort-down');
		$(event.target).toggleClass('fa-sort-up');
	});
});
