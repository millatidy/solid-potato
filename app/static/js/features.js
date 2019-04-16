$(document).ready(function() {

    /**
     * FeaturesViewModel is responsible for fetching a paginated list of
     * Features from the api and handles changes on the
     * Features page
     */
    function FeaturesViewModel() {
        var self = this;
        self.featuresURI = "/api/features";
        self.productAreasURI = "/api/product-areas";
        self.features = ko.observableArray();
        self.productAreas = ko.observableArray();
        self.clients = ko.observableArray();
        self.featureRequests = ko.observableArray();

        self.currentPage = ko.observable();
        self.min = ko.observable();
        self.max = ko.observable();
        self.totalItems = ko.observable();
        self.maxItems = ko.observable();

        self.nextFeaturesURI = ko.observable();
        self.prevFeaturesURI = ko.observable();
        self.currentPageURI = ko.observableArray();

        self.beginAdd = function() {
            addFeatureModel.setProductAreas(self.productAreas)
            $('#add').modal('show');
        }

        /**
         * Posts new Feature to the API and binds it to the
         * features view on success
         * @param {feature} feature - The new Feature
         */
        self.add = function(feature) {
            ApiGateway(self.featuresURI, 'POST', feature).done(function(data) {
                if (self.currentPage() == 1) {
                    self.features.unshift({
                        id: ko.observable(data.id),
                        title: ko.observable(data.title),
                        description: ko.observable(data.description),
                        uri: ko.observable(data.links.self),
                        productArea: ko.observable(data.product_area),
                        productAreaURI: ko.observable(data.links.product_area),
                        requestsURI: ko.observable(data.links.requests),
                        noRequests: ko.observable(data.no_requests),
                        url: ko.observable("/features/" + data.id)
                    });
                    if (self.features().length >= self.maxItems()) {
                        self.features.splice(-1, 1);
                    }
                }
                self.totalItems(self.totalItems() + 1);
            });
        }


        self.beginEdit = function(feature) {
            editFeatureViewModel.setFeature(feature);
            $('#edit').modal('show');
        }

        /**
         * Edits an existing Feature with a call to the API and binds it to the
         * features view on success
         * @param {feature} feature - The existing feature
         * @param {feature} data - The edited Feature
         */
        self.edit = function(feature, data) {
            ApiGateway(feature.uri(), 'PUT', data).done(function(res) {
                self.updateFeature(feature, res);
            })
        }

        self.updateFeature = function(feature, newFeature) {
            var i = self.features.indexOf(feature);
            // self.features()[i].uri
            self.features()[i].title(newFeature.title);
            self.features()[i].description(newFeature.description);
            self.features()[i].productArea(newFeature.product_area);
            self.features()[i].product_area_id(newFeature.product_area_id)
        };

        /**
         * Calls the DELETE method on the API to delete an existing Feature
         * and removes it from view on success
         * @param {feature} feature - The feature to be deleted
         */
        self.remove = function(feature) {
            ApiGateway(feature.uri(), 'DELETE').done(function() {
                self.features.remove(feature);
                self.reload(); // the delete hack in action
            });
        }

        // loads the previous Features Page
        self.loadPrev = function() {
            ApiGateway(self.prevFeaturesURI(), 'GET').done(
                function(data) {
                    self.loadFeaures(data);
                });
        }

        // loads the next Features Page
        self.loadNext = function() {
            ApiGateway(self.nextFeaturesURI(), 'GET').done(
                function(data) {
                    self.loadFeaures(data);
                });
        }

        self.loadFeaures = function(data) {
            self.features([]);
            for (var i = 0; i < data.items.length; i++) {
                self.features.push({
                    id: ko.observable(data.items[i].id),
                    title: ko.observable(data.items[i].title),
                    description: ko.observable(data.items[i].description),
                    uri: ko.observable(data.items[i].links.self),
                    product_area_id: ko.observable(data.items[i].product_area_id),
                    productArea: ko.observable(data.items[i].product_area),
                    productAreaURI: ko.observable(data.items[i].links.product_area),
                    requestsURI: ko.observable(data.items[i].links.requests),
                    noRequests: ko.observable(data.items[i].no_requests),
                    url: ko.observable("/features/" + data.items[i].id)
                });
            }
            var page = data._meta.page;
            var per_page = data._meta.per_page;
            self.totalItems(data._meta.total_items)
            self.maxItems(per_page);
            self.currentPage(page);
            self.currentPageURI(data._links.self); // this is for delete hack

            var paginate = Paginate(data._meta.page, data._meta.per_page, data.items.length);

            self.min(paginate[0]);
            self.max(paginate[1]);

            self.nextFeaturesURI(data._links.next);
            self.prevFeaturesURI(data._links.prev);
        }

        self.getFeatures = function() {
            ApiGateway(self.featuresURI, 'GET').done(
                function(data) {
                    self.loadFeaures(data);
                });
        }

        // reload features after delete
        // not the most efficient but it pulls the trick
        self.reload = function() {
            ApiGateway(self.currentPageURI(), 'GET').done(
                function(data) {
                    self.loadFeaures(data);
                });
        }

        self.getProducts = function() {
            ApiGateway(self.productAreasURI, 'GET').done(
                function(data) {
                    for (var i = 0; i < data.items.length; i++) {
                        self.productAreas.push({
                            id: ko.observable(data.items[i].id),
                            name: ko.observable(data.items[i].name),
                            uri: ko.observable(data.items[i].links.self)
                        });
                    }
                });
        }

        // Get Features
        self.getFeatures();

        // Get Products
        self.getProducts();
    }


    /**
     * AddFeatureViewModel is responsible for binding data entered
     * on the Add New Feature Modal.
     *
     * Also initializes Product Area to the Modal user to select as they entered
     * a new Feature data
     */
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
            self.title(null);
            self.description(null);
            self.productArea(null);
            $("#inputProductArea").val('default');
        }

        self.setProductAreas = function(productAreas) {
            self.productAreas(productAreas());
            $('#add').modal('show');
        }
    }


    /**
     * EditFeatureViewModel initializes the Edit Feature Modal with data of a
     * Feature to be edited and returns the edited data to the
     * FeaturesViewModel
     */
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
