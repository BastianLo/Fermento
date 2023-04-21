
$(function () {
    $('button[name="complete"]').click(function () {   
        let container = $(this).parent()
        $.ajax({
            url: "/batches/executions/complete/" + $(this).attr('btnvalue') + "/",
            method: "POST",
            data: {
                "csrfmiddlewaretoken":csrftoken
            },
            success: function (data) {
                container.remove();
            }
        });
    });
});