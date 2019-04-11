$(document).ready(function () {
	
	function ClientDetailsViewModel() {
		var self = this;
		self.id = ko.observable(location.pathname.split("/")[2]);
		self.name = ko.observable();
		self.requests = ko.observableArray();

		self.api = "http://localhost:5000/api";
		self.clientURI = self.api + "/clients/" + self.id();
		self.featureRequestsURI = self.api + "/feature-requests" + "?client_id=" + self.id();

		self.beginEdit = function() {
			alert('we can edit from here');
		}

		self.remove = function() {
			alert('We can delete from here');
		}

		self.getClientDetails = function() {
			ApiGateway(self.clientURI, 'GET').done(function(data){
				self.name(data.name);
			});
		}

		self.getRequests = function() {
			ApiGateway(self.featureRequestsURI, 'GET').done(function(data){
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