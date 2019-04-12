$(document).ready(function() {

    /*
     * This view Model is responsiple for capturing seach queries and
     * redirectig the browser to search resuls page
     *
     */

    function SearchFormViewModel() {
        var self = this;
        self.query = ko.observable("");

        self.beginSearch = function() {
            window.location = '/search?q=' + self.query();
        }

    }

    var searchFormViewModel = new SearchFormViewModel();
    ko.applyBindings(searchFormViewModel, $('#search')[0]);
});
