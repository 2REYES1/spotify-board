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

