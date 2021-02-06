const getGooglePhoto = async (photoRef) => {
	const dataBody = `{"photo_reference":"${photoRef}"}`;
	const response = await fetch('/api/restaurant/details/photo', {
		method  : 'POST',
		headers : {
			'Content-Type' : 'application/json'
		},
		body    : dataBody
	});
	const data = response.json();

	return data;
};
const getUserLikesDislikes = async () => {
	const res = await fetch('/api/user/likes_dislikes');
	const data = await res.json();
	const likesDislikes = [ ...data.likes, ...data.dislikes ];
	return likesDislikes;
};

const handleRestaurantDetail = ({ name, address }) => {
	$('.res-name').empty().append(name);
	$('.res-address').empty().append(address);
};
const handlePhoto = async (restaurantDetail, photoCount) => {
	const res = await getGooglePhoto(restaurantDetail.photo_references[photoCount]);
	const photoUrl = res.url;

	$('.restaurant-photo').attr('src', photoUrl);
};

const handleLike = ({ name, address, googlePlaceId }) => {
	const dataBody = `{"googlePlaceId":"${googlePlaceId}","name":"${name}","address":"${address}"}`;
	fetch('/api/restaurant/like', {
		method  : 'POST',
		headers : {
			'Content-Type' : 'application/json'
		},
		body    : dataBody
	});
};
const handleUnlike = (placeId) => {
	const dataBody = `{"googlePlaceId":"${placeId}"}`;
	fetch('/api/restaurant/unlike', {
		method  : 'POST',
		headers : {
			'Content-Type' : 'application/json'
		},
		body    : dataBody
	});
};
const handleDislike = ({ name, address, googlePlaceId }) => {
	const dataBody = `{"googlePlaceId":"${googlePlaceId}","name":"${name}","address":"${address}"}`;
	fetch('/api/restaurant/dislike', {
		method  : 'POST',
		headers : {
			'Content-Type' : 'application/json'
		},
		body    : dataBody
	});
};
const toggleDetailedView = () => {
	// Will toggle if you click anywhere in Card
	$('.restaurant-detailed').toggle();
	$('.restaurant-normal').toggle();
};

const handlerTest = () => {
	console.log('handlertest');
};
const generateAreasTable = () => {
	const areasTableMarkup = $(`
	<table class="table table-hover">
	<thead>
	  <tr>
		<th scope="col">City</th>
		<th scope="col">State</th>
		<th scope="col">Delete</th>
	  </tr>
	</thead>
	<tbody class="areas">
	</tbody>
  	</table>
  	`);
	return areasTableMarkup;
};
const populateAreasTable = ({ areas }) => {
	for (let area of areas) {
		const areaMarkup = $(`
			<tr class="area-row" data-href="/discover/restaurants/${area.id}" >
			<td>${area.city}</td>
			<td>${area.state}</td>
			<td><a class="btn btn-sm btn-danger" href="/areas/${area.id}/delete">X</a></td>
			</tr>
		`);
		$('tbody').append(areaMarkup);
	}
};

const changeImgToLoad = () => {
	$('.restaurant-photo').attr('src', '/static/loading-200px.gif');
};

const generateLikesTable = () => {
	const likesTableMarkup = $(`
	<table class="table table-hover">
	<thead>
	  <tr>
		<th scope="col"><span id="name" class="fas fa-sort-down"></span> Name</th>
		<th scope="col"><span id="area_city" class="fas fa-sort-down"></span> City</th>
		<th scope="col"><span id="area_state" class="fas fa-sort-down"></span> State</th>
		
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
