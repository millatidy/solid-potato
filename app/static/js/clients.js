$(document).ready(function() {
    /**
     * ClientsViewModel is responsible for fetching a paginated list of
     * Clients from the api and handles changes on the
     * Client Details page
     */
    function ClientsViewModel() {
        var self = this;
        self.clientsURI = "/api/clients";
        self.clients = ko.observableArray();

        self.getClients = function() {
            ApiGateway(self.clientsURI, 'GET').done(function(data) {
                for (var i = 0; i < data.items.length; i++) {
                    self.clients.push({
                        id: data.items[i].id,
                        name: data.items[i].name,
                        noRequests: data.items[i].no_requests,
                        uri: data.items[i].links.self,
                        url: ko.observable("/clients/" + data.items[i].id)

                    });
                }
            });
        }

        self.getClients();
    }

    var clientsViewModel = new ClientsViewModel();
    ko.applyBindings(clientsViewModel, $('#clients')[0]);

});
