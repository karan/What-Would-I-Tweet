angular.module("TweetApp", [])
        .config(["$routeProvider", function($routeProvider) {
            $routeProvider
                .when("/", {
                    templateUrl: 'index.html',
                    controller: 'TweetController'
                })
                .otherwise({redirectTo: "/"});
        }])
        .factory("windowAlert", [
            "$window",
            function($window) {
                return $window.alert;
            }
        ])
        .controller("TweetController", [
            "$scope","$http", "$windowAlert",
            function($scope, $http, $windowAlert) {
                $scope.state = {};
                $scope.state.tweets = [];

                $scope.getTweets = function() {
                    if (!$scope.state.screenName) {
                        windowAlert('Nopes');
                    } else {
                        $http
                            .get('http://localhost:5000/get_tweets/' + $scope.state.screenName)
                            .success(function(data, status, headers, config) {
                                $scope.state.tweets = data.tweets;
                            })
                            .error(function(data, status, headers, config) {
                                windowAlert("Error");
                            });
                    };
                }
            }
        ])
