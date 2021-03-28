$(function(){
    $('input[name="drill_type"]').change(function () {
        drillform_submit();
    });

    $('#id_create_drill').on('click', function() {
        drillform_submit();
    });

    function drillform_submit(){
        $('#drill-form').attr("action", $(this).data('action'));
        $('#drill-form').submit();
    }
});