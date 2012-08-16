$(function() {
    function setInitialContent(){
        var ids = $('#id_song_ids').attr('value')
        if (ids)
            ids = ids.split(',');
        else
            return;
        for(var i = 0; i < ids.length; i++){
            var node = $('#library-list li[data-id="' + ids[i] + '"]');
            node = node.clone();
            $('#songbook-list').append(node);
            appendToSongbook(node, true);
        }
    }

    function setSongIds(){
        var ids = [];
        $('#songbook-list li').each(function(){
            ids.push($(this).data('id'));
        });
        $('#id_song_ids').attr('value', ids);
    }

    function countInSongbook(id){
        var count = $('#songbook-list [data-id="' + id + '"]').length;
        var zero = 'ui-state-default';
        var nonzero = 'ui-state-active';
        if(!count){
            $('#library-list [data-id="' + id + '"]').addClass(zero).removeClass(nonzero);
        }else{
            $('#library-list [data-id="' + id + '"]').addClass(nonzero).removeClass(zero);
        }
    }

    function addDeleteButtonClick(root){
        root = root || $("#songbook-list");
        root.find(".delete-button").click(function(){
            var id = $(this).parent().data('id')
            $(this).parent().remove();
            countInSongbook(id);
            return false;
        });
    }

    function appendToSongbook(node, skipCounting){
        if (!node.find('.delete-button').length){
            node.find('.song-details-button').remove();
            node.append($('<a href="#" class="ui-icon ui-icon-trash delete-button"></a>'));
            addDeleteButtonClick(node);
            if(!skipCounting)
                countInSongbook(node.data('id'));
            node.addClass('ui-state-default').removeClass('ui-state-active');
        }
    }

    function initListJs(){
        var options = {
            valueNames: ['title']
        };

        var library = new List('library', options);
    }
    setInitialContent();
    $("#songbook-list").sortable({
        stop: function(event, ui){
            appendToSongbook(ui.item);
        }
    });
    $('#songbook-form').submit(setSongIds);
    $("#songbook-list, .sort").disableSelection();
    addDeleteButtonClick();

    $("#library-list li").draggable({
        connectToSortable: '#songbook-list',
        revert: 'invalid',
        helper: 'clone'
    });
    $('#library-list li').each(function(){
        countInSongbook($(this).data('id'));
    });
    $('#library-list li').dblclick(function(){
        var node = $(this).clone();
        $('#songbook-list').append(node);
        appendToSongbook(node);
    });
    $('.button').button();
    initListJs();
});

function addNode(){
    var node = $('<li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>Item ++</li>');
    $('ul').append(node);
}