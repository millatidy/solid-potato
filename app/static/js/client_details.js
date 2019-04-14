$(document).ready(function() {

  /**
   * ClientDetailsViewModel is responsible for fetching a Clients details
   * from the api and a list of paginated Feature Requests of that client, and
   * handles changes on the Client Details page
   */
    function ClientDetailsViewModel() {
        var self = this;
        self.id = ko.observable(location.pathname.split("/")[2]);
        self.name = ko.observable();
        self.requests = ko.observableArray();

        self.clientURI = "/api/clients/" + self.id();
        self.featureRequestsURI = "/api/feature-requests" + "?client_id=" + self.id();

        // Dummy function for editing a Feature Request
        self.beginEdit = function() {
            alert('we can edit from here');
        }

        // Dummy function for deleting a Feature Request
        self.remove = function() {
            alert('We can delete from here');
        }

        self.getClientDetails = function() {
            ApiGateway(self.clientURI, 'GET').done(function(data) {
                self.name(data.name);
            });
        }

        self.getRequests = function() {
            ApiGateway(self.featureRequestsURI, 'GET').done(function(data) {
                for (var i = 0; i < data.items.length; i++) {
                    self.requests.push({
                        featureID: ko.observable(data.items[i].feature_id),
                        clientID: ko.observable(data.items[i].client_id),
                        featureTitle: ko.observable(data.items[i].feature_title),
                        priority: ko.observable(data.items[i].priority),
                        targetDate: ko.observable(data.items[i].target_date),
                        uri: ko.observable(data.items[i].links.self)
                    });
                }
            });
        }

        self.getClientDetails();
        self.getRequests();
    }

    var clientDetailsViewModel = new ClientDetailsViewModel();
    ko.applyBindings(clientDetailsViewModel, $('#client-detail')[0]);
});
