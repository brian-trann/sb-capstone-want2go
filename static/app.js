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
