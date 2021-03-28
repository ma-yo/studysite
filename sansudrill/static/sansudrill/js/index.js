$(function(){
    $('input[name="drill_type"]').change(function () {
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill').on('click', function() {
        drillform_submit($(this).data('action'));
    });

    function drillform_submit(data_action){
        $('#drill-form').attr("action", data_action);
        $('#drill-form').submit();
    }
});