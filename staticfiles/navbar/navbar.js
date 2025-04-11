
jQuery(document).ready(function($){
    var currentPath = window.location.pathname;

    // Удаляем все классы active
    $('#navbarSupportedContent ul li').removeClass('active');

    // Добавляем active в зависимости от текущего пути
    $('#navbarSupportedContent ul li a').each(function(){
        var $this = $(this);
        var linkPath = $this.attr('href');

        // Поддержка точного совпадения и вложенных путей
        if (linkPath === currentPath || currentPath.startsWith(linkPath)) {
            $this.parent().addClass('active');
        }
    });

    // Обработка кликов по пунктам меню (чтобы менялся active вручную)
    $('#navbarSupportedContent ul li a').on('click', function(){
        $('#navbarSupportedContent ul li').removeClass('active');
        $(this).parent().addClass('active');
    });
});
