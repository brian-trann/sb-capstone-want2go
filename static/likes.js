$(async function() {
	// on document load
	// do stuff
	let photoCount = 0;
	let placeId = null;
	let restaurantDetail = null;
	const userLikes = await getUserLikes();

	$('#likes-table').append(generateLikesTable());
	populateLikesTable(userLikes);

	$('#likes-table').on('click', '.like-row', async function() {
		placeId = $(this).data('place');
		restaurantDetail = await RestaurantDetail.getRestaurantDetail(placeId);
		handleRestaurantDetail(restaurantDetail);
		handlePhoto(restaurantDetail, photoCount);

		toggleViews();
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

const generateLikesTable = () => {
	const likesTableMarkup = $(`
	<table class="table table-hover">
	<thead>
	  <tr>
		<th scope="col"><span id="name" class="fas fa-sort-down"></span> Name</th>
		<th scope="col"><span id="area_city" class="fas fa-sort-down"></span> City</th>
		<th scope="col"><span id="area_state" class="fas fa-sort-down"></span> State</th>
		<th scope="col"></th>
	  </tr>
	</thead>
	<tbody class="likes">
	</tbody>
  	</table>
  	`);
	return likesTableMarkup;
};
const populateLikesTable = ({ restaurant_likes }) => {
	for (let res of restaurant_likes) {
		const likeMarkup = $(`
        <tr class="like-row" id="${res.name}" data-place="${res.google_place_id}" >
        <td>${res.name}</td>
        <td>${res.area_city}</td>
        <td>${res.area_state}</td>
        <td><a class="btn btn-sm btn-danger" href="#">X</a></td>
        </tr>
    `);
		$('tbody').append(likeMarkup);
	}
};
const getUserLikes = async () => {
	const res = await fetch('/api/likes');
	return res.json();
};
const toggleViews = () => {
	$('#likes-table').toggle();
	$('.card-view').toggle();
	$('.go-back').toggle();
};

const changeImgToLoad = () => {
	$('.restaurant-photo').attr('src', '/static/loading-200px.gif');
};

const sortBy = (arr, idSortBy, direction) => {
	return arr.sort((a, b) => {
		if (a[idSortBy] > b[idSortBy]) {
			return direction === 'up' ? 1 : -1;
		} else if (b[idSortBy] > a[idSortBy]) {
			return direction === 'up' ? -1 : 1;
		}
		return 0;
	});
};
