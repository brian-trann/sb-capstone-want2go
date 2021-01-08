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
	$('.carousel').toggle();
	$('.card').toggle();
};

$('.restaurant-normal').on('click', function() {
	console.log('restaurant-normal click');
	// toggleDetailedView()
});
$('.carousel').on('click', function() {
	$('.carousel').carousel('next');
	// $('.carousel-control-prev-35')
});
