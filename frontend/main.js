// Fetch the top tracks from the Flask backend
$(document).ready(function () {
    $.ajax({
        url: "/api/top-tracks",
        method: "GET",
        success: function (data) {
            if (data.error) {
                $("#top-tracks").html("<li>" + data.error + "</li>");
                return;
            }
            let trackList = "";
            data.forEach((track, index) => {
                trackList += `<li>${index + 1}. <a href="${track.url}" target="_blank">${track.name}</a> by ${track.artist}</li>`;
            });
            $("#top-tracks").html(trackList);
        },
        error: function (xhr, status, error) {
            console.error("Error fetching tracks:", error);
            $("#top-tracks").html("<li>Failed to load tracks. Please try again later.</li>");
        }
    });
});
