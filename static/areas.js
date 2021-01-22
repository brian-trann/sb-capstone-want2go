/**
 * On Document load:
 */
$(async function() {
	if ($('#areas-table').length === 1) {
		let areasList;
		try {
			areasList = await AreasList.getAreas();
		} catch (e) {
			alert("Unable to get user's list from database");
			console.log(e);
		}
		$('#areas-table').append(generateAreasTable());
		populateAreasTable(areasList);
	}

	$('#areas-table').on('click', '.area-row', function() {
		window.location = $(this).data('href');
	});
});
