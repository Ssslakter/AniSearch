let page = 1;

$(document).ready(function () {
    $('#next-b').click(() => {page += 1; updateInfo()});
    $('#prev-b').click(() => {page -= 1; if (page === 0) page = 1; updateInfo()});

    updateInfo()

    function updateInfo() {
        $.ajax({
        type: 'GET',
        url: `/api/v1/user/all/${page}`,
        contentType: 'application/json',
        success: function (response) {
            renderSearchResults(response);
        },
        error: function (error) {
            console.error(error);
        }
    });
    }

    function renderSearchResults(data) {
        var resultsContainer = $('#results-container');
        resultsContainer.empty();

        if (data.length === 0) {
            resultsContainer.html('<p>No results found.</p>');
            return;
        }

        for (let obj in data) {
            let item = $('<div>').text(data[obj]);
            resultsContainer.append(item)
        }
    }

});
