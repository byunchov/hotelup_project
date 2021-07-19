(function ($) {
    "use strict";

    // Add active state to sidbar nav links
    const path = window.location.href.split('?')[0]; // because the 'href' property of the DOM element is the absolute path
    $("#navbarTogglerDemo01 a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    const user_menu_sel = $("div.dropdown-menu.user-dropdown-menu a.dropdown-item");

    user_menu_sel.each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    if(user_menu_sel.hasClass('active')){
        user_menu_sel.parent().parent().children().first().addClass('active')
    }

})(jQuery);