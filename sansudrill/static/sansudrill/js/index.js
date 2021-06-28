$(function(){

    function setCode() {
        let code = {'0':'0'
        ,'1':'A'
        ,'2':'B'
        ,'3':'C'
        ,'4':'D'
        ,'5':'E'
        ,'6':'F'
        ,'7':'G'
        ,'8':'H'
        ,'9':'I'
        ,'10':'J'}
        let drill_type = code[$('input[name="drill_type"]:checked').val()];
        let left_minus_select = code[$('#id_left_minus_select').val()];
        let right_minus_select = code[$('#id_right_minus_select').val()];
        let left_input = code[$('#id_left_input').val()];
        let right_input = code[$('#id_right_input').val()];
        let keta_fix_left_select = code[$('#id_keta_fix_left_select').val()];
        let keta_fix_right_select = code[$('#id_keta_fix_right_select').val()];
        let mod_select = 'A';
        if ($('#id_mod_select').is(':visible')) {
            mod_select = code[$('#id_mod_select').val()];
        }
        let answer_minus_select = code[$('#id_answer_minus_select').val()];
        let answer_select = code[$('#id_answer_select').val()];
        let mondai_cnt_select = code[$('#id_mondai_cnt_select').val()];
        let mondai_type_select = code[$('#id_mondai_type_select').val()];

    $('#id_load_drill_type_input').val(
        drill_type
         + left_minus_select
         + right_minus_select
         + left_input
         + right_input
         + keta_fix_left_select
         + keta_fix_right_select
         + mod_select
         + answer_minus_select
         + answer_select
         + mondai_cnt_select
         + mondai_type_select);
    }

    setCode();

    $('select').change(function() {
        setCode();
    });
    $('#id_left_input').change(function() {
        if($(this).val()>10){
            $(this).val(10);
        }
        setCode();
    });
    $('#id_right_input').change(function() {
        if($(this).val()>10){
            $(this).val(10);
        }
        setCode();
    });

    $('input[name="drill_type"]').change(function () {
        setCode();
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_pdf').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#content-type').val($(this).data('content'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_csv_utf8').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#content-type').val($(this).data('content'));
        $('#enc-type').val($(this).data('enc'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_csv_sjis').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#content-type').val($(this).data('content'));
        $('#enc-type').val($(this).data('enc'));
        drillform_submit($(this).data('action'));
    });

    $('#id_create_drill_xls').on('click', function() {
        $('.non-field-errors').hide();
        $('#message-area').hide();
        $('#content-type').val($(this).data('content'));
        drillform_submit($(this).data('action'));
    });

    $('#id_load_drill_type').on('click', function() {
        let code = {'0':'0'
        ,'A':'1'
        ,'B':'2'
        ,'C':'3'
        ,'D':'4'
        ,'E':'5'
        ,'F':'6'
        ,'G':'7'
        ,'H':'8'
        ,'I':'9'
        ,'J':'10'}
        let input_code = $('#id_load_drill_type_input').val();
        if(input_code.length != 12){
            $('#id_copy_drill_alert').html('コードが不正です。');
            $('#id_copy_drill_alert').css({color:'red'});
            $('#id_copy_drill_alert').show().delay(300).fadeOut(600);
            return;
        }
        let drill_type = input_code.slice(0,1);
        let left_minus_select = input_code.slice(1,2);
        let right_minus_select = input_code.slice(2,3);
        let left_input = input_code.slice(3,4);
        let right_input = input_code.slice(4,5);
        let keta_fix_left_select = input_code.slice(5,6);
        let keta_fix_right_select = input_code.slice(6,7);
        let mod_select = input_code.slice(7,8);
        let answer_minus_select = input_code.slice(8,9);
        let answer_select = input_code.slice(9,10);
        let mondai_cnt_select = input_code.slice(10,11);
        let mondai_type_select = input_code.slice(11,12);

        var exists = isCodeExists(code[drill_type], 1, 5)
        && isCodeExists(code[left_minus_select], 1, 3)
        && isCodeExists(code[right_minus_select], 1, 3)
        && isCodeExists(code[left_input], 0, 10)
        && isCodeExists(code[right_input], 0, 10)
        && isCodeExists(code[keta_fix_left_select], 1, 2)
        && isCodeExists(code[keta_fix_right_select], 1, 2)
        && isCodeExists(code[mod_select], 1, 3)
        && isCodeExists(code[answer_minus_select], 1, 3)
        && isCodeExists(code[answer_select], 1, 2)
        && isCodeExists(code[mondai_cnt_select], 1, 5)
        && isCodeExists(code[mondai_type_select], 1, 3);
        if(!exists){
            $('#id_copy_drill_alert').html('コードが不正です。');
            $('#id_copy_drill_alert').css({color:'red'});
            $('#id_copy_drill_alert').show().delay(300).fadeOut(600);
            return;
        }
        $('input[name="drill_type"]:eq('+(code[drill_type] - 1)+')').prop('checked', true);
        $('#id_left_minus_select').val(code[left_minus_select]);
        $('#id_right_minus_select').val(code[right_minus_select]);
        $('#id_left_input').val(code[left_input]);
        $('#id_right_input').val(code[right_input]);
        $('#id_keta_fix_left_select').val(code[keta_fix_left_select]);
        $('#id_keta_fix_right_select').val(code[keta_fix_right_select]);
        $('#id_mod_select').val(code[mod_select]);
        $('#id_answer_minus_select').val(code[answer_minus_select]);
        $('#id_answer_select').val(code[answer_select]);
        $('#id_mondai_cnt_select').val(code[mondai_cnt_select]);
        $('#id_mondai_type_select').val(code[mondai_type_select]);
        drillform_submit($('input[name="drill_type"]:eq('+(code[drill_type] - 1)+')').data('action'));
    });

    $('#id_copy_drill_type').on('click', function() {
        // コピーする文章の取得
        let text = $('#id_load_drill_type_input').val();
        // テキストエリアの作成
        let $textarea = $('<textarea></textarea>');
        // テキストエリアに文章を挿入
        $textarea.text(text);
        //　テキストエリアを挿入
        $(this).append($textarea);
        //　テキストエリアを選択
        $textarea.select();
        // コピー
        document.execCommand('copy');
        // テキストエリアの削除
        $textarea.remove();

        $('#id_copy_drill_alert').html('クリップボードにコピーしました。');
        $('#id_copy_drill_alert').css({color:'blue'});
        $('#id_copy_drill_alert').show().delay(300).fadeOut(600);

    });

    function drillform_submit(data_action){
        $('#drill-form').attr("action", data_action);
        $('#drill-form').submit();
    }
    
    function isCodeExists(code, from, to){
        if(code >= from && code <= to){
            return true;
        }
        return false;
    }
});