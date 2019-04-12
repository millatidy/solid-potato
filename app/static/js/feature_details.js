$(document).ready(function() {

    function FeatureDetailsViewModel() {
        var self = this;
        self.api = "http://localhost:5000/api"
        self.clientsURI = self.api + "/clients";

        self.id = ko.observable(location.pathname.split("/")[2]);
        self.requestURI = self.api + "/features/" + self.id();
        self.featureRequestsURI = self.api + "/feature-requests" + "?feature_id=" + self.id();

        self.title = ko.observable();
        self.description = ko.observable();
        self.product_area_id = ko.observable();
        self.uri = ko.observable();
        self.productAreaURI = ko.observable();
        self.requestsURI = ko.observable();
        self.requests = ko.observableArray();
        self.clients = ko.observableArray();

        self.prodcuts = ko.observableArray();

        self.beginAdd = function() {
            addFeatureRequestViewModel.initialize(self.id, self.clients);
            $('#addRequest').modal('show');
        }

        self.add = function(featureRequest) {
            var i = self.requests().findIndex(
                request => request.clientID() === featureRequest.client_id
            );
            if(i === -1) {
                ApiGateway(self.requestsURI(), 'POST', featureRequest).done(function(data) {
                self.requests.push({
                    featureID: ko.observable(data.feature_id),
                    clientID: ko.observable(data.client_id),
                    priority: ko.observable(data.priority),
                    targetDate: ko.observable(data.target_date),
                    clientName: ko.observable(data.client_name)
                });
            });
            } else {
                self.edit(self.requests()[i], featureRequest);
            }
            
        }

        self.beginEdit = function(featureRequest) {
            editFeatureRequestViewModel.initialize(self.id, self.clients);
            editFeatureRequestViewModel.setFeatureRequest(featureRequest);
            $('#editRequest').modal('show');
        }

        self.edit = function(featureRequest, data) {
            ApiGateway(featureRequest.uri(), 'PUT', data).done(function(res) {
                self.updateRequest(featureRequest, res);
            });
        }
        self.updateRequest = function(featureRequest, newRequest) {
            var i = self.requests.indexOf(featureRequest);
            self.requests()[i].priority(newRequest.priority);
            self.requests()[i].targetDate(newRequest.target_date)
        };

        self.remove = function(featureRequest) {
            ApiGateway(featureRequest.uri(), 'DELETE').done(function() {
                self.requests.remove(featureRequest);
            });
        }

        self.getRequest = function() {
            ApiGateway(self.requestURI, 'GET').done(
                function(data) {
                    self.id(data.id);
                    self.title(data.title);
                    self.description(data.description);
                    self.uri(data.links.self);
                    self.requestsURI(data.links.requests);
                });
        }

        self.getClients = function() {
            ApiGateway(self.clientsURI, 'GET').done(
                function(data) {
                    for (var i = 0; i < data.items.length; i++) {
                        self.clients.push({
                            id: ko.observable(data.items[i].id),
                            name: ko.observable(data.items[i].name),
                            uri: ko.observable(data.items[i].links.self),
                            requstsURI: ko.observable(data.items[i].links.requests)
                        });
                    }
                });
        }

        self.getRequests = function() {
            ApiGateway(self.featureRequestsURI, 'GET').done(
                function(data) {
                    for (var i = 0; i < data.items.length; i++) {
                        self.requests.push({
                            featureID: ko.observable(data.items[i].feature_id),
                            clientID: ko.observable(data.items[i].client_id),
                            priority: ko.observable(data.items[i].priority),
                            targetDate: ko.observable(data.items[i].target_date),
                            uri: ko.observable(data.items[i].links.self),
                            clientName: ko.observable(data.items[i].client_name)
                        });
                    }

                });
        }

        // Get Feature Detials
        self.getRequest();

        // Load Clients
        self.getClients();

        // Load requests
        self.getRequests();

    }

    function AddFeatureRequestViewModel() {
        var self = this;
        self.featureID = ko.observable();
        self.clientID = ko.observable();
        self.priority = ko.observable();
        self.targetDate = ko.observable();
        self.clients = ko.observableArray();

        self.initialize = function(featureID, clients) {
            self.featureID(featureID());
            self.clients(clients());
        }

        self.addRequest = function() {
            $('#addRequest').modal('hide');
            featureDetailsViewModel.add({
                feature_id: self.featureID(),
                client_id: self.clientID(),
                priority: self.priority(),
                target_date: self.targetDate()
            });
            self.featureID(null);
            self.clientID(null);
            self.priority(null);
            self.targetDate(null);

            $('#inputClient').val('default');
            $('#inputPriority').val('default');
        }
    }

    function EditFeatureRequestViewModel() {
        var self = this;
        self.featureID = ko.observable();
        self.clientID = ko.observable();
        self.priority = ko.observable();
        self.targetDate = ko.observable();
        self.clients = ko.observableArray();

        self.initialize = function(featureID, clients) {
            self.featureID(featureID());
            self.clients(clients());
        }

        self.setFeatureRequest = function(featureRequest) {
            self.featureRequest = featureRequest;
            self.featureID(featureRequest.featureID());
            self.clientID(featureRequest.clientID());
            self.priority(featureRequest.priority());
            self.targetDate(featureRequest.targetDate());
        }

        self.editRequest = function() {
            $("#editRequest").modal("hide");
            featureDetailsViewModel.edit(self.featureRequest, {
                feature_id: self.featureID(),
                client_id: self.clientID(),
                priority: self.priority(),
                target_date: self.targetDate()
            });
        }
    }


    var featureDetailsViewModel = new FeatureDetailsViewModel();
    var addFeatureRequestViewModel = new AddFeatureRequestViewModel();
    var editFeatureRequestViewModel = new EditFeatureRequestViewModel();
    ko.applyBindings(featureDetailsViewModel, $('#feature-detail')[0]);
    ko.applyBindings(addFeatureRequestViewModel, $('#addRequest')[0]);
    ko.applyBindings(editFeatureRequestViewModel, $('#editRequest')[0]);

});
