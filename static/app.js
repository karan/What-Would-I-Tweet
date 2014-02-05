var TweetApp = angular.module("TweetApp", []);

TweetApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.screenName = '';
    $scope.tweets = [];
    $scope.copy = '';
    
    $scope.getTweet = function (screenName) {
        if ($scope.tweets.length > 0 && screenName == $scope.copy) {
            console.log('already in list');
            $scope.tweet = $scope.tweets.pop();
        } else {
            $scope.copy = screenName;
            console.log('not in list');
            delete $http.defaults.headers.common['X-Requested-With'];
            $http({
                method: 'GET',
                url: 'http://localhost:5000/get_tweets/' + screenName
            })
            .success(function(data, status, headers, config) {
                $scope.tweets = data['results'];
                $scope.tweet = $scope.tweets.pop();
            })
            .error(function(data, status, headers, config) {
                // something went wrong!!
                alert('Invalid username or protected tweets.');
            });
        }
    }
}]);
