$(document).ready(function() {
    
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

});
