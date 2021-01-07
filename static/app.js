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
