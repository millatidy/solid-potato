/**
 * ApiGateway is a generic function to make Api calls to the server on
 * behalf of View Models
 * @param {string} uri - The api endpoint for a resource
 * @param {string} method - The api method to be called on resource
 * @param {object} data - The data to be sent to the server
 */
function ApiGateway(uri, method, data) {
    // const host = 'https://workshift.co.zw/britecore';
    const host = "http://localhost:5000";
    var request = {
        url: host + uri,
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

    var itemsRangeMin = (page - 1) * perPage + 1;
    var itemsRangeMax = (page - 1) * perPage + itemsLength;

    return [itemsRangeMin, itemsRangeMax];
}

function dateConverter(date) {
  var dateString = date;
  var dateObj = new Date(dateString);
  var momentObj = moment(dateObj);
  var momentString = momentObj.format('YYYY-MM-DD');
  return momentString;
}
