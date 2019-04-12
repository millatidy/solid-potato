$(document).ready(function() {
    /*
     * This view Model is responsible for fetching search queries and
     * displaying seach results
     *
     * It captures the seach query from the browser url
     *
     * NB: This app only searchs Feature titles and description for demonstration
     *     purposes only
     */

    function SearchResultsViewModel() {
        var self = this;
        self.searchURI = 'http://localhost:6000/api/search?q=';
        self.results = ko.observableArray();
        self.query = ko.observable(location.href.split('=')[1])

        self.getResults = function() {
            var queryURI = self.searchURI + self.query();
            ApiGateway(queryURI, 'GET').done(function(data) {
                for (var i = 0; i < data.items.length; i++) {
                    self.results.push({
                        id: ko.observable(data.items[i].id),
                        title: ko.observable(data.items[i].title),
                        description: ko.observable(data.items[i].description),
                        productArea: ko.observable(data.items[i].product_area),
                        uri: ko.observable(data.items[i].links.self),
                        url: ko.observable("/feature/" + data.items[i].id)
                    });
                }
            });
        }

        self.getResults();

    }

    var searchResultsViewModel = new SearchResultsViewModel();
    ko.applyBindings(searchResultsViewModel, $('#search-results')[0]);
});
