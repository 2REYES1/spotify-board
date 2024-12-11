$(document).ready(function () {
    $.ajax({
        url: "http://127.0.0.1:5000/top-tracks", 
        method: "GET",
        success: function (data) {
            data.tracks.forEach((track, index) => {
                const trackId = `#track${index + 1}`;
                const polaroid = $(trackId);

                if (polaroid.length) {
                    polaroid.find('.album-cover').css('background-image', `url(${track.album_image})`);
                    polaroid.find('.song-name').text(track.name);

                    polaroid.click(function () {
                        $('#track-popup').css('display', 'flex').fadeIn();
                        $('#track-popup .album-cover-modal').css('background-image', `url(${track.album_image})`);
                        $('#track-popup .track-number-modal').text(`${index + 1}`);
                        $('#track-popup .song-name-modal').text(track.name);
                        $('#track-popup .artist-name-modal').text(track.artists.join(', '));
                        $('#track-popup .album-name-modal').text(track.album);

                        
                        $.ajax({
                            url: 'http://127.0.0.1:5000/get-rating', 
                            method: 'GET',
                            data: { track_name: track.name }, 
                            success: function (response) {
                                const rating = response.rating || "Unrated"; 
                                $('#track-popup .track-rating-modal').text(rating === "Unrated" ? rating : `${rating} ★`);
                            },
                            error: function (xhr, status, error) {
                                console.error("Failed to fetch rating:", error);
                                $('#track-popup .album-name-modal').text("Unrated");
                            }
                        });
                    });
                }
            });

            
            $('.close').click(function () {
                $('#track-popup').fadeOut();
            });

            $(window).click(function (event) {
                if ($(event.target).is('#track-popup')) {
                    $('#track-popup').fadeOut();
                }
            });
        },
        error: function (xhr, status, error) {
            console.error("Can't get Top Tracks:", error); 
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const polaroids = document.querySelectorAll('.polaroid');

    polaroids.forEach(polaroid => {
        
        const randomRotation = Math.floor(Math.random() * 21) - 10; 
        polaroid.style.transform = `rotate(${randomRotation}deg)`;

        
        polaroid.addEventListener('mouseenter', () => {
            polaroid.style.transform = 'rotate(0deg)';
        });

        
        polaroid.addEventListener('mouseleave', () => {
            polaroid.style.transform = `rotate(${randomRotation}deg)`;
        });
    });
});





$(document).ready(function () {
    
    $('#change-rating-btn').click(function () {
        $('#change-rating-popup').css('display', 'flex').fadeIn();
    });

   
    $('.close-rating').click(function () {
        $('#change-rating-popup').fadeOut();
    });

    
    $('#submit-rating-btn').click(function () {
        const trackName = $('#track-popup .song-name-modal').text(); 
        const rating = $('input[name="rating"]:checked').val(); 

        if (!rating) {
            alert("Please select a rating!");
            return;
        }

        $.ajax({
            url: 'http://127.0.0.1:5000/rate', 
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ track_name: trackName, rating: rating }),
            success: function (response) {
                alert(`${response.message}`);
                $('#change-rating-popup').fadeOut();

                
                const displayRating = `${rating} ★` || "Unrated";
                $('#track-popup .track-rating-modal').text(displayRating);
            },
            error: function (xhr, status, error) {
                console.error("Rating failed:", error);
            }
        });
    });

 
    $(window).click(function (event) {
        if ($(event.target).is('#change-rating-popup')) {
            $('#change-rating-popup').fadeOut();
        }
    });
});


