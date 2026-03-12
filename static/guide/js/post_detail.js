$(document).ready(function() {
    // Get CSRF token from the hidden input rendered by {% csrf_token %}
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

    $('#ajax-like-btn').click(function(e) {
        e.preventDefault();
        var btn = $(this);
        var url = btn.data('url');

        $.ajax({
            url: url,
            type: 'POST',
            data: { csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function(data) {
                if (data.is_liked) {
                    btn.removeClass('btn-outline-primary').addClass('btn-primary shadow-sm');
                    btn.text('Liked');
                    btn.attr('aria-label', 'Liked');
                } else {
                    btn.removeClass('btn-primary shadow-sm').addClass('btn-outline-primary');
                    btn.text('Like');
                    btn.attr('aria-label', 'Like this post');
                }
            },
            error: function(xhr, status, error) {
                console.log('Like error:', status, error);
            }
        });
    });

    $('#ajax-save-btn').click(function(e) {
        e.preventDefault();
        var btn = $(this);
        var url = btn.data('url');

        $.ajax({
            url: url,
            type: 'POST',
            data: { csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function(data) {
                if (data.is_saved) {
                    btn.removeClass('btn-outline-secondary').addClass('btn-secondary shadow-sm');
                    btn.text('Saved');
                    btn.attr('aria-label', 'Saved');
                } else {
                    btn.removeClass('btn-secondary shadow-sm').addClass('btn-outline-secondary');
                    btn.text('Save');
                    btn.attr('aria-label', 'Save this post');
                }
            },
            error: function(xhr, status, error) {
                console.log('Save error:', status, error);
            }
        });
    });
});
