document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-1').forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this quote?')) {
                event.preventDefault();
            }
        });
    });
});