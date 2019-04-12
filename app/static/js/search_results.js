$('document').ready.(function () {
	/*
	 * This view Model is responsiple for making seach queries and
	 * displaying seach results
     *
	 * NB: This app only searchs Feature titles and description for demonstration
	 *     purposes only
	*/

	function SearchResultsViewModel() {
		self = this;
		self.searchURI = 'http://localhost:5000/api/search';
		self.results = ko.obsevableArray();

		self.getResults = function() {
			ApiGateway(self.searchURI, 'GET').done(function(data) {

			});
		}

	}

	var searchResultsViewModel = SearchResultsViewModel();
	ko.applyBindings(searchResultsViewModel, $('#search-results')[0]);
});