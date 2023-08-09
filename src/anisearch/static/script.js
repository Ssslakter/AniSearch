$(document).ready(function () {
    $('.search-btn').click(sendRequest);

    $('.search-input').keydown(function (event) {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault(); // Prevent the default Enter key behavior

            // Call the function to send the request
            sendRequest();
        }
    });

    $('#toggle-nickname').change(function () {
        var isNicknameEnabled = $(this).is(':checked');
        $('#nickname').prop('disabled', !isNicknameEnabled);
    });

    function renderSearchResults(data) {
        var resultsContainer = $('#results-container');
        resultsContainer.empty();

        if (data.length === 0) {
            resultsContainer.html('<p>No results found.</p>');
        } else {
            var row = $('<div>').addClass('row');
            data.forEach(function (item) {
                var card = $('<div>').addClass('card col-md-3');
                var imgWrapper = $('<div>').addClass('img-wrapper');
                var img = $('<img>').addClass('card-img-top img-fluid').attr('src', item.metadata.img_url);
                var cardBody = $('<div>').addClass('card-body');
                var title = $('<h5>').addClass('card-title').text(item.metadata.title);
                var description = $('<p>').addClass('card-text').text(item.metadata.synopsis);

                var infoList = $('<ul>').addClass('list-group list-group-flush');
                var aired = $('<li>').addClass('list-group-item').text('Aired: ' + item.metadata.aired);
                var episodes = $('<li>').addClass('list-group-item').text('Episodes: ' + item.metadata.episodes);
                var genres = $('<li>').addClass('list-group-item').text('Genres: ' + item.metadata.genres.join(', '));
                var popularity = $('<li>').addClass('list-group-item').text('Popularity: ' + item.metadata.popularity);
                var score = $('<li>').addClass('list-group-item').text('Score: ' + item.metadata.score);

                infoList.append(aired, episodes, genres, popularity, score);

                imgWrapper.append(img);
                cardBody.append(title, description, infoList);
                card.append(imgWrapper, cardBody);
                row.append(card);
            });
            resultsContainer.append(row);
        }
    }

    function sendRequest() {
        var searchText = $('.search-input').val();
        var nickname = $('#nickname').val();

        if ($('#toggle-nickname').prop('checked')) {
            if (searchText.trim() !== '' && nickname.trim() !== '') {
                $.ajax({
                    type: 'POST',
                    url: '/api/v1/content/recommend',
                    data: JSON.stringify({ text: searchText, nickname: nickname }),
                    contentType: 'application/json',
                    success: function (response) {
                        renderSearchResults(response);
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            }
            else if (nickname.trim() !== '') {
                $.ajax({
                    type: 'GET',
                    url: `/api/v1/content/recommend/${nickname}`,
                    contentType: 'application/json',
                    success: function (response) {
                        renderSearchResults(response);
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            }
        } else {
            if (searchText.trim() !== '') {
                let url = ""; if ($('#toggle-fulltext').prop('checked')) url = "text_search";

                $.ajax({
                    type: 'POST',
                    url: `/api/v1/content/${url}`,
                    data: JSON.stringify({ text: searchText }),
                    contentType: 'application/json',
                    success: function (response) {
                        renderSearchResults(response);
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            }
        }
    }

});

