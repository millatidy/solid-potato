$(document).ready(function() {

	function FeaturesViewModel() {
			var self = this;
			self.api = "http://localhost:5000/api"
			self.featuresURI = self.api + "/features";
			self.features = ko.observableArray();
			self.productAreas = ko.observableArray();
			self.clients = ko.observableArray();
			self.featureRequests = ko.observableArray();

			self.beginAdd = function() {
				addFeatureModel.setProductAreas(self.productAreas)
					$('#add').modal('show');
			}

			self.add = function(feature) {
					ApiGateway(self.featuresURI, 'POST', feature).done(function(data) {
							self.features.push({
									title: ko.observable(data.title),
									description: ko.observable(data.description),
									product_area_id: ko.observable(data.product_area_id)
							});
					});
			}

			self.beginEdit = function(feature) {
					editFeatureViewModel.setFeature(feature);
					$('#edit').modal('show');
			}

			self.edit = function(feature, data) {
					self.ajax(feature.uri(), 'PUT', data).done(function(res) {
							self.updateFeature(feature, res);
					})
			}

			self.updateFeature = function(feature, newFeature) {
					var i = self.features.indexOf(feature);
					// self.features()[i].uri
					self.features()[i].title(newFeature.title);
					self.features()[i].description(newFeature.description);
					self.features()[i].product_area_id(newFeature.product_area_id)
			};

			self.remove = function(feature) {
					self.ajax(feature.uri(), 'DELETE').done(function() {
							self.features.remove(feature);
					});
			}

			self.markInProgress = function(feature) {
					feature.done(false);
			}

			self.markDone = function(feature) {
					feature.done(true);
			}

			self.getFeatures = function() {
				ApiGateway(self.featuresURI, 'GET').done(
					function(data) {
					for (var i = 0; i < data.items.length; i++) {
							self.features.push({
								id: ko.observable(data.items[i].id),
									title: ko.observable(data.items[i].title),
									description: ko.observable(data.items[i].description),
									uri: ko.observable(data.items[i].links.self),
									product_area_id: ko.observable(data.items[i].product_area_id),
									productAreaURI: ko.observable(data.items[i].links.product_area),
									requestsURI: ko.observable(data.items[i].links.requests),
									noRequests: ko.observable(data.items[i].no_requests),
									url: ko.observable("/feature/" + data.items[i].id)
							});
					}
			});
			}


			self.getFeatures();
	}

	function AddFeatureViewModel() {
			var self = this;
			self.title = ko.observable();
			self.description = ko.observable();
			self.productArea = ko.observable();
			self.productAreas = ko.observableArray();

			self.addFeature = function() {
					$('#add').modal('hide');
					featuresViewModel.add({
							title: self.title(),
							description: self.description(),
							product_area_id: self.productArea()
					});
					self.title("");
					self.description("");
					self.productArea("")
			}

			self.setProductAreas = function(productAreas) {
				self.productAreas(productAreas());
				$('#add').modal('show');
			}
	}

	function EditFeatureViewModel() {
			var self = this;
			self.title = ko.observable();
			self.description = ko.observable();
			self.product_area_id = ko.observable();

			self.setFeature = function(feature) {
					self.feature = feature;
					self.title(feature.title());
					self.description(feature.description());
					self.product_area_id(feature.product_area_id());
					$('#edit').modal('show');
			}

			self.editFeature = function() {
				console.log("SAFDD");
					$('#editRequest').modal('hide');
					featuresViewModel.edit(self.feature, {
							title: self.title(),
							description: self.description(),
							product_area_id: self.product_area_id()
					});
			}

	}


	var featuresViewModel = new FeaturesViewModel();
	var addFeatureModel = new AddFeatureViewModel();
	var editFeatureViewModel = new EditFeatureViewModel();
	ko.applyBindings(featuresViewModel, $('#main')[0]);
	ko.applyBindings(addFeatureModel, $('#add')[0]);
	ko.applyBindings(editFeatureViewModel, $('#edit')[0]);

});