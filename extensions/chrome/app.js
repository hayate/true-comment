(function($) {

    var app = $.sammy(function() {
        this.use(Sammy.Template, 'html');

        this.get('#/', function(ctx) {
            $.ajax({
                url: 'http://api.biv.dev/comment/list',
                success: function(data) {
                    console.log(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.status != 200)
                    {
                        ctx.redirect('#/signin');
                    }
                    // else show the comments
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('Accept', 'application/json');
                },
                type: 'GET'
            });
        });

        this.get('#/signin', function(ctx) {
            this.partial('templates/signin.html');
        });
    });

    $(function() {
        app.run('#/');
    });

})(jQuery);
