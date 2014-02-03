var TweetApp = angular.module("TweetApp", []);

TweetApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.screenName = '';
    $scope.tweets = {};
    
    $scope.getTweets = function (screenName) {
        delete $http.defaults.headers.common['X-Requested-With'];
        $http({
            method: 'GET',
            url: 'http://localhost:5000/get_tweets/' + screenName
        })
        .success(function(data, status, headers, config) {
            $scope.tweets = data['results'];
        })
        .error(function(data, status, headers, config) {
            // something went wrong!!
            alert('Invalid username or protected tweets.');
        });
    }
}]);
