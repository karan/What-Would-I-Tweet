var TweetApp = angular.module("TweetApp", []);

TweetApp.controller('MainCtrl', ['$scope', '$http', '$sce', function($scope, $http, $sce) {
    $scope.screenName = '';
    $scope.tweets = [];
    $scope.copy = '';
    $scope.tsrc = '';
    $scope.loading = false;

    var domain = 'tweeny.herokuapp.com/';
    var base_url = 'https://platform.twitter.com/widgets/tweet_button.html?count=none&size=large&text=';
    
    $scope.getTweet = function (screenName) {
        if ($scope.tweets.length > 0 && screenName == $scope.copy) {
            console.log('already in list');
            $scope.tweet = $scope.tweets.pop();
            $scope.tsrc = $sce.trustAsResourceUrl(base_url + '@' + $scope.screenName + ' would say ' + '"' + $scope.tweet.tweet + '"');
        } else {
            $scope.copy = screenName;
            $scope.loading = true;
            console.log('not in list');
            $http({
                method: 'GET',
                url: '/get_tweets/' + screenName
            })
            .success(function(data, status, headers, config) {
                $scope.tweets = data['results'];
                $scope.tweet = $scope.tweets.pop();
                $scope.loading = false;
                $scope.tsrc = $sce.trustAsResourceUrl(base_url + '@' + $scope.screenName + ' would say ' + '"' + $scope.tweet.tweet + '"');
            })
            .error(function(data, status, headers, config) {
                // something went wrong!!
                $scope.loading = false;
                alert('Invalid username or protected tweets.');
            });
        }
    }
}]);
