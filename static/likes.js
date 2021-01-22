$(async function() {
	// on document load
	// do stuff
	let photoCount = 0;
	let placeId = null;
	let restaurantDetail = null;
	let userLikes;
	try {
		userLikes = await getUserLikes();
	} catch (e) {
		alert("Unable to get user's from database");
		console.log(e);
	}

	$('#likes-table').append(generateLikesTable());
	populateLikesTable(userLikes);

	$('#likes-table').on('click', '.like-row', async function() {
		placeId = $(this).data('place');
		try {
			restaurantDetail = await RestaurantDetail.getRestaurantDetail(placeId);
			handleRestaurantDetail(restaurantDetail);
			handlePhoto(restaurantDetail, photoCount);
		} catch (e) {
			alert('Unable to fetch restaurant information from Google');
			console.log(e);
		}

		toggleViews();
	});

	$('.unlike').on('click', () => {
		try {
			handleUnlike(placeId);
		} catch (e) {
			alert('Unable to send unlike to database');
			console.log(e);
		}
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
		try {
			handlePhoto(restaurantDetail, photoCount);
		} catch (e) {
			alert('Unable to get photo from Google');
			console.log(e);
		}
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
