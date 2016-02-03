var initialize = function(navigator, user, token, urls) {
    $('#id_login').on('click', function() {
        navigator.id.request();
        return false;
    })
    $('#id_logout').on('click', function() {
        navigator.id.logout();
        return false;
    })
    
    navigator.id.watch({
        loggedInUser: user,
        onlogin: function (assertion) {
            $.post(urls.login, {assertion: assertion, csrfmiddlewaretoken: token})
            .done(function () { window.location.reload(); })
            .fail(function () { navigator.id.logout(); })
        },
        onlogout: function () {
            document.location.href = urls.logout;
            //.always(function () { window.location.reload(); })
        },
    });
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
