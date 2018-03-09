// dropdown menus
var monthDropdown = $(".filter-month-dropdown");
var dowDropdown = $(".filter-dow-dropdown");

// when filter type changes
$(".filter-type").change(function() {
	var filterTypeVal = $(".filter-type").val();
	if (filterTypeVal == 'day') {
		monthDropdown.hide();
		dowDropdown.show();
	} else if (filterTypeVal == 'month') {
		dowDropdown.hide();
		monthDropdown.show();
	} else if (filterTypeVal == 'none') {
		dowDropdown.hide();
		monthDropdown.hide();	
	}
})