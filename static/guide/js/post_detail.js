$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({ headers: { 'X-CSRFToken': csrftoken } });

    $('#ajax-like-btn').click(function(e) {
        e.preventDefault();
        var url = $(this).data('url');
        $.post(url, function(data) {
            if (data.is_liked) {
                $('#ajax-like-btn').removeClass('btn-outline-primary').addClass('btn-primary shadow-sm');
                $('#like-icon').removeClass('bi-hand-thumbs-up').addClass('bi-hand-thumbs-up-fill');
                $('#like-text').text('Unlike');
            } else {
                $('#ajax-like-btn').removeClass('btn-primary shadow-sm').addClass('btn-outline-primary');
                $('#like-icon').removeClass('bi-hand-thumbs-up-fill').addClass('bi-hand-thumbs-up');
                $('#like-text').text('Like');
            }
        });
    });

    $('#ajax-save-btn').click(function(e) {
        e.preventDefault();
        var url = $(this).data('url');
        $.post(url, function(data) {
            if (data.is_saved) {
                $('#ajax-save-btn').removeClass('btn-outline-secondary').addClass('btn-secondary shadow-sm');
                $('#save-icon').removeClass('bi-bookmark').addClass('bi-bookmark-fill');
                $('#save-text').text('Unsave');
            } else {
                $('#ajax-save-btn').removeClass('btn-secondary shadow-sm').addClass('btn-outline-secondary');
                $('#save-icon').removeClass('bi-bookmark-fill').addClass('bi-bookmark');
                $('#save-text').text('Save');
            }
        });
    });
});