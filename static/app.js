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
			<td><a class="btn btn-sm btn-danger" href="/areas/{{area.id}}/delete">X</a></td>
			</tr>
		`);
		$('tbody').append(areaMarkup);
	}
};
/**
 * On Document load:
 */
$(async function() {
	if ($('#areas-table').length === 1) {
		const areasList = await AreasList.getAreas();
		$('#areas-table').append(generateAreasTable());
		populateAreasTable(areasList);
	}

	$('.restaurant-normal').on('click', function() {
		// toggleDetailedView();
	});

	$('#areas-table').on('click', '.area-row', function() {
		window.location = $(this).data('href');
	});
});
