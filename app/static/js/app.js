
function ApiGateway(uri, method, data) {
				var request = {
						url: uri,
						type: method,
						contentType: "application/json",
						accepts: "application/json",
						cache: false,
						dataType: 'json',
						data: JSON.stringify(data),
						beforeSend: function(xhr) {
								xhr.setRequestHeader("Access-Control-Allow-Origin", "http://localhost:8000")
						},
						error: function(jqXHR) {
								console.log("ajax error " + jqXHR.status);
						}
				};
				return $.ajax(request);
}

function Paginate(page, perPage, itemsLength) {

	var itemsRangeMin = (page-1)*perPage + 1;
	var itemsRangeMax = (page-1)*perPage + itemsLength;

	return [itemsRangeMin, itemsRangeMax];
}