$(function(){
    $('input[name="drill_type"]').change(function () {
        $('#drill-form').attr("action", "");
        $('#drill-form').submit();
    });

    $('#id_create_drill').on('click', function() {
        $('#drill-form').attr("action", $(this).data('action'));
        $('#drill-form').submit();
    });
});