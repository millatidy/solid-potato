// $(document).ready(function() {

function fn1 () {
    alert("sdafsdkj");
}

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


// });