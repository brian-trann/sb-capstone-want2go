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
	const res = await fetch('/api/user/likes', {
		method : 'POST'
	});
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
		<th scope="col">Zipcode</th>
		<th scope="col"></th>
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
			<tr class="area-row" id="${area.zipcode}" data-href="/discover/restaurants/${area.id}" data-lat="${area.latitude}" data-long="${area.longitude}">
			<td>${area.city}</td>
			<td>${area.state}</td>
			<td>${area.zipcode}</td>
			<td><a class="btn btn-sm btn-danger" href="/areas/${area.id}/delete">X</a></td>
			</tr>
		`);
		$('tbody').append(areaMarkup);
	}
};
