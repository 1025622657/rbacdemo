$('.menu-header').click(function () {

    // $(this).next().toggleClass('rbac-hide');
    $(this).next().removeClass('hide').parent().siblings().find('.menu-body').addClass('hide')

})