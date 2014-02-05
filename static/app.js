var TweetApp = angular.module("TweetApp", []);

TweetApp.controller('MainCtrl', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
    $scope.screenName = '';
    $scope.tweets = [];
    $scope.copy = '';
    $scope.tsrc = '';

    var domain = 'x.goel.im';
    var base_url = 'https://platform.twitter.com/widgets/tweet_button.html?count=none&size=large&via=' + domain + '&text=';
    
    $scope.getTweet = function (screenName) {
        if ($scope.tweets.length > 0 && screenName == $scope.copy) {
            console.log('already in list');
            $scope.tweet = $scope.tweets.pop();
            $scope.tsrc = $sce.trustAsResourceUrl(base_url + '"' + $scope.tweet.tweet +'"');
        } else {
            $scope.copy = screenName;
            console.log('not in list');
            $http({
                method: 'GET',
                url: 'http://localhost:5000/get_tweets/' + screenName
            })
            .success(function(data, status, headers, config) {
                $scope.tweets = data['results'];
                $scope.tweet = $scope.tweets.pop();
                $scope.tsrc = $sce.trustAsResourceUrl(base_url + '"' + $scope.tweet.tweet +'"');
            })
            .error(function(data, status, headers, config) {
                // something went wrong!!
                alert('Invalid username or protected tweets.');
            });
        }
    }
}]);
