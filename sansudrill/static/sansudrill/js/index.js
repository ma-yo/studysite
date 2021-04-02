$(function(){
    $('input[name="drill_type"]').change(function () {
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_pdf').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#output-type').val($(this).data('content'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_csv_utf8').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#output-type').val($(this).data('content'));
        $('#enc-type').val($(this).data('enc'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_csv_sjis').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#output-type').val($(this).data('content'));
        $('#enc-type').val($(this).data('enc'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_xls').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#output-type').val($(this).data('content'));
        drillform_submit($(this).data('action'));
    });

    function drillform_submit(data_action){
        $('#drill-form').attr("action", data_action);
        $('#drill-form').submit();
    }
});