document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-1').forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this quote?')) {
                event.preventDefault();
            }
        });
    });
});


window.onload = function() {
    setTimeout(function() {
        var flashMessage = document.getElementById('flash-message');
        if (flashMessage) {
            flashMessage.style.display = 'none';
        }
    }, 3000); // 5000 milliseconds = 5 seconds
};

// script.js
var swiper = new Swiper('.mySwiper', {
    spaceBetween: 30,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
});


document.addEventListener('DOMContentLoaded', function() {
    var swiper = new Swiper('.mySwiper', {
        spaceBetween: 30,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        loop: false, // Disable loop mode
    });

    // Custom navigation buttons
    document.getElementById('prevButton').addEventListener('click', function() {
        swiper.slidePrev();
    });

    document.getElementById('nextButton').addEventListener('click', function() {
        swiper.slideNext();
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper
    var swiper = new Swiper('.mySwiper', {
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        loop: false, // Disable loop mode
    });

    // Custom navigation buttons
    var prevButton = document.getElementById('prevButton');
    var nextButton = document.getElementById('nextButton');

    prevButton.addEventListener('click', function() {
        swiper.slidePrev();
        checkButtonState();
    });

    nextButton.addEventListener('click', function() {
        swiper.slideNext();
        checkButtonState();
    });

    // Check the state of buttons to disable/enable based on slide position
    function checkButtonState() {
        let index = swiper.activeIndex;
        let totalSlides = swiper.slides.length - 2; // Adjust for duplicate slides in loop mode

        if (index === 0) {
            prevButton.disabled = true;
        } else {
            prevButton.disabled = false;
        }

        if (index-1 == totalSlides) {
            nextButton.disabled = true;
        } else {
            nextButton.disabled = false;
        }
    }

    // Initial check for the button states
    checkButtonState();
});
