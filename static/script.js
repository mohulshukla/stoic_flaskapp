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

