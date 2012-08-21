$(function(){
    function initListJs(){
        var options = {
            valueNames: ['title']
        };

        var library = new List('songs', options);
    }
    $(".sort").disableSelection();
    initListJs();
});
