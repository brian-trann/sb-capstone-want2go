/**
 * processForm: get data from form
 */
function processForm(evt) {
	evt.preventDefault();
	const data = getZipcode();
	console.log(data);
	hideZipcodeSearchForm();
}
const getZipcode = () => {
	const zipcode = $('#zipcode').val();
	return zipcode;
};
const hideZipcodeSearchForm = () => {
	$('#search').hide();
};

const toggleDetailedView = () => {
	// Will toggle if you click anywhere in Card
	$('.restaurant-detailed').toggle();
	$('.restaurant-normal').toggle();
};

$('.area-id').on('click', function() {
	// console.log($(this).data('id'));
	window.location = $(this).data('href');
});

$('.restaurant-normal').on('click', function() {
	// toggleDetailedView();
});
