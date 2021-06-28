import logging
import random
import reportlab
import math
import os
import csv
import xlsxwriter
from io import BytesIO

from sansudrill.models import NgPattern
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.conf import settings
from . import forms

from datetime import datetime as dt

from reportlab.pdfgen import canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

from decimal import Decimal, getcontext, Overflow, DivisionByZero, InvalidOperation

#コンテキスト
context = {'title':'『無料』計算問題自動作成 | 小学生向け', 'message_type':'alert-info', 'message':'', 'timestamp':dt.now().strftime('%Y%m%d%H%M%S')}

# PDFフォント
FONT_NAMEPDF = 'ipa-gothic-fonts'

# 足し算
PLUS_CODE = 1
# 引き算
MINUS_CODE = 2
# 掛け算
MULTIPLCODE = 3
# 割り算
DIVIDE_CODE = 4
# ランダム
RANDOM_CODE = 5

# マイナス無し
MINUS_INPUT_OFF = 1
# マイナス有り
MINUS_INPUT_ON = 2
# マイナスのみ
MINUS_INPUT_ONLY = 3

KETA_INPUT_0 = 0
KETA_INPUT_1 = 1
KETA_INPUT_2 = 2
KETA_INPUT_3 = 3
KETA_INPUT_4 = 4
KETA_INPUT_5 = 5
KETA_INPUT_6 = 6
KETA_INPUT_7 = 7
KETA_INPUT_8 = 8
KETA_INPUT_9 = 9
KETA_INPUT_10 = 10

# 桁固定しない
KETA_FIX_OFF = 1
# 桁固定する
KETA_FIX_ON = 2

# 答えマイナス無し
ANSWER_MINUS_OFF = 1
# 答えマイナス有り
ANSWER_MINUS_ON = 2
# 答えマイナスのみ
ANSWER_MINUS_ONLY = 3

# 余りなし
MOD_OFF = 1
# 余り有り
MOD_ON = 2
# 小数点
MOD_DECIMAL = 3

# 通常の計算式
MONDAI_TYPE_NORMAL = 1
# 逆算
MONDAI_TYPE_REVERSE = 2
# ひっ算
MONDAI_TYPE_HISSAN = 3

# 最大ループ回数
MAX_LOOP_COUNT = 5000

# コンテキストを初期化する
def init_context():
    context['message'] = ""
    context['timestamp'] = dt.now().strftime('%Y%m%d%H%M%S')

# 素因数分解
def prime_factorize(n):
    arr = []
    n = int(n)
    temp = n
    for i in range(2, int(-(-n**0.5//1))+1):
        if temp%i==0:
            cnt=0
            while temp%i==0:
                cnt+=1
                temp //= i
            arr.append([i, cnt])

    if temp!=1:
        arr.append([temp, 1])

    if arr==[]:
        arr.append([n, 1])
    return arr

# ランダムな整数を取得する
def create_randint(value, keta_fix):
    num = 0

    if keta_fix == False:
        if value == 0:
            return 0
        randValue = random.randint(1, value)
        result = ""
        for num in range(randValue):
            if num == 0:
                result += str(random.randint(1, 9))
            else:
                result += str(random.randint(0, 9))
        return str(result)
    else:
        if value == 0:
            return 0
        result = ""
        for num in range(value):
            if num == 0:
                result += str(random.randint(1, 9))
            else:
                result += str(random.randint(0, 9))

        return str(result)

# ドリルタイトルを描画する
def draw_title(p, width, height, drill_name, write_answer, mondai_name, mondai_cnt):

    name_title = "なまえ:"
    inner_title = '計算ドリル[' + str(mondai_cnt) + '問 ' + drill_name +' ' + mondai_name +']'
    if write_answer:
        inner_title += "(答え)"
    font_size = 18
    str_width = pdfmetrics.stringWidth(inner_title, FONT_NAMEPDF, font_size)
    str_height = pdfmetrics.getAscent(FONT_NAMEPDF, font_size) + pdfmetrics.getDescent(FONT_NAMEPDF, font_size)
    x = width  - str_width - 15
    y = height - 25 - str_height
    p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定
    p.drawString(x, y, inner_title)

    if write_answer == False:
        x = 0
        p.drawString(x + 15, y, name_title)

        p.setLineWidth(1)
        p.line(x + 15, y - 3, x + 275, y - 3)


# スライド判定問題数を取得する
def get_slide_range(mondai_cnt):
    range_cnt = 0
    if mondai_cnt == 50:
        range_cnt = 25
    elif mondai_cnt == 40:
        range_cnt = 20
    elif mondai_cnt == 30:
        range_cnt = 15
    elif mondai_cnt == 20:
        range_cnt = 10
    else:
        range_cnt = 5
    return range_cnt
# 計算問題をPDFに描画する
def draw_keisan(p, font_size, x, y, start, drill_type, drill_list, answer_output, mondai_cnt, mondai_type):

    slide_cnt = get_slide_range(mondai_cnt)

    add_x_default = 27
    max_y = 750 / slide_cnt
    for num in range(slide_cnt):

        tmp_font_size = font_size
        p.drawString(x, y, str(drill_list[num + start][0]) + ")")

        kigo = ""
        if drill_list[num + start][1] == PLUS_CODE:
            kigo = "＋"
        elif drill_list[num + start][1] == MINUS_CODE:
            kigo = "－"
        elif drill_list[num + start][1] == MULTIPLCODE:
            kigo = "×"
            tmp_font_size *= 1.4
        elif drill_list[num + start][1] == DIVIDE_CODE:
            kigo = "÷"
            tmp_font_size *= 1.4

        # 通常の計算の場合
        if answer_output == True or mondai_type == MONDAI_TYPE_NORMAL:
            # 左辺
            sahen = str(drill_list[num + start][3])
            sahen_width = pdfmetrics.stringWidth(sahen, FONT_NAMEPDF, font_size)
            add_x1 = add_x_default
            p.drawString(x + add_x1, y, sahen)

            #　記号

            p.setFont(FONT_NAMEPDF, tmp_font_size)  # フォントを設定
            kigo_width = pdfmetrics.stringWidth(kigo, FONT_NAMEPDF, tmp_font_size)
            p.drawString(x + add_x1 + sahen_width + 2, y, kigo)
            p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定

            # 右辺
            uhen = str(drill_list[num + start][4])
            if drill_list[num + start][4] < 0:
                uhen = "(" + uhen + ")"
            uhen_width = pdfmetrics.stringWidth(uhen, FONT_NAMEPDF, font_size)
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2, y, uhen)

            # イコール記号
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5, y, "=")

            equals_width = pdfmetrics.stringWidth("=", FONT_NAMEPDF, font_size)

            # 答え
            if answer_output:
                if drill_list[num + start][1] == DIVIDE_CODE and drill_list[num + start][2] == 3 and str(drill_list[num + start][5]).__contains__("."):
                    ans_shosu = str(drill_list[num + start][5]).split('.')[1]
                    if len(ans_shosu) > 5:
                        ans_num = drill_list[num + start][5].quantize(Decimal("0.00001"))
                    else:
                        ans_num = drill_list[num + start][5]
                    ans = str(ans_num)
                else:
                    ans_num = drill_list[num + start][5]
                    ans = str(ans_num)
                p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5, y, ans)

                if drill_list[num + start][2] == 2 and drill_list[num + start][6] != 0:
                    ans_width = pdfmetrics.stringWidth(ans, FONT_NAMEPDF, font_size)
                    p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5 + ans_width, y, "余り" + str(drill_list[num + start][6]))
            y -= max_y

        elif mondai_type == MONDAI_TYPE_REVERSE:
            #逆算計算タイプの場合
            # 左辺
            sahen = str(drill_list[num + start][3])
            sahen_width = pdfmetrics.stringWidth(sahen, FONT_NAMEPDF, font_size)
            add_x1 = add_x_default
            p.drawString(x + add_x1, y, sahen)

            #　記号
            kigo_width = pdfmetrics.stringWidth(kigo, FONT_NAMEPDF, font_size)
            p.drawString(x + add_x1 + sahen_width + 2, y, kigo)

            # 右辺 逆算なので描画しない
            uhen = str(drill_list[num + start][4])
            if drill_list[num + start][4] < 0:
                uhen = "(" + uhen + ")"
            uhen_width = pdfmetrics.stringWidth(uhen, FONT_NAMEPDF, font_size)

            # イコール記号
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5, y, "=")

            equals_width = pdfmetrics.stringWidth("=", FONT_NAMEPDF, font_size)

            # 答え 逆算なので描画する
            if drill_list[num + start][1] == DIVIDE_CODE and drill_list[num + start][2] == 3 and str(drill_list[num + start][5]).__contains__("."):
                ans_num = drill_list[num + start][5].quantize(Decimal("0.00001"))
                ans = str(ans_num)
            else:
                ans_num = drill_list[num + start][5]
                ans = str(ans_num)
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5, y, ans)

            if drill_list[num + start][2] == 2 and drill_list[num + start][6] != 0:
                ans_width = pdfmetrics.stringWidth(ans, FONT_NAMEPDF, font_size)
                p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5 + ans_width, y, "余り" + str(drill_list[num + start][6]))
            y -= max_y
        else:

            add_height = 12
            add_x1 = 0
            add_x_default = 50
            add_margin = 3
            #　記号
            kigo_width = pdfmetrics.stringWidth(kigo, FONT_NAMEPDF, font_size)

            # 右辺
            uhen = str(drill_list[num + start][4])
            uhen_width = pdfmetrics.stringWidth(uhen, FONT_NAMEPDF, font_size)

            # 左辺
            sahen = str(drill_list[num + start][3])
            sahen_width = pdfmetrics.stringWidth(sahen, FONT_NAMEPDF, font_size)

            if uhen_width > add_x1:
                add_x1 = uhen_width
            if sahen_width > add_x1:
                add_x1 = sahen_width
            add_x1 += kigo_width
            add_x1 += add_x_default
            # 右辺描画
            p.drawRightString(x + add_x1, y - add_height, uhen)
            # 左辺
            p.drawRightString(x + add_x1, y, sahen)

            # 記号
            p.drawString(x + add_x_default - add_margin, y - add_height, kigo)

            p.setLineWidth(1)
            p.line(x + add_x_default, y - add_height - add_margin, x + add_x1, y - add_height - add_margin)

            y -= max_y

#素因数分解し、割れる数を取得する
def get_divide_list(value):
    factorized_tapple = prime_factorize(value)
    if len(factorized_tapple) == 0:
        return []

    factorized_list = []
    for p in factorized_tapple:
        for p1 in range(p[1]):
            factorized_list.append(p[0])

    result_list = []
    for p in range(len(factorized_list)):
        num = factorized_list[p]
        if result_list.__contains__(num) == False and num != int(value):
            result_list.append(num)
        for p1 in range(len(factorized_list)):
            if p == p1:
                continue
            num *= factorized_list[p1]
            if result_list.__contains__(num) == False and num != int(value):
                result_list.append(num)
    result_list.sort()
    return result_list

#計算ドリルリストを作成する
def create_drill_list(request, drill_type, left_input, right_input
, answer_select, keta_fix_left_flg, keta_fix_right_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select, mondai_cnt):

    # 作成した計算式を格納
    drill_list = []
    loop_cnt = 0
    tmp_drill_type = drill_type
    while True:
        loop_cnt+=1
        if loop_cnt > MAX_LOOP_COUNT:
            return []

        if drill_type == RANDOM_CODE:
            #計算式をランダムで選択する
            tmp_drill_type = random.randint(1, 4)

        # 桁固定の場合
        if keta_fix_left_flg == KETA_FIX_ON:
            left_number_str = create_randint(left_input, True)
        else:
            left_number_str = create_randint(left_input, False)
        if keta_fix_right_flg == KETA_FIX_ON:
            right_number_str = create_randint(right_input, True)
        else:
            right_number_str = create_randint(right_input, False)

        left_value_dec = Decimal(left_number_str)

        # ﾏｲﾅｽ有無
        if left_minus_flg == 2: # ﾏｲﾅｽ含む
            minus_div = random.randint(0,1)
            if minus_div == 1:
                left_value_dec *= Decimal(-1)
        if left_minus_flg == 3: # ﾏｲﾅｽ固定
            left_value_dec *= Decimal(-1)

        # 小数点とつなげる
        right_value_dec = Decimal(right_number_str)

        # ﾏｲﾅｽ有無
        if right_minus_flg == 2: # ﾏｲﾅｽ含む
            minus_div = random.randint(0,1)
            if minus_div == 1:
                right_value_dec *= Decimal(-1)
        if right_minus_flg == 3: # ﾏｲﾅｽ固定
            right_value_dec *= Decimal(-1)

        answer_dec = Decimal(0)
        answer_mod_dec = Decimal(0)

        if tmp_drill_type == DIVIDE_CODE: # 割り算

            # どちらかが0はやり直す
            if left_value_dec == 0 or right_value_dec == 0:
                continue
            # 同数値もループ
            if left_value_dec == right_value_dec:
                continue

            if mod_select == MOD_OFF: #余り無し
                if abs(left_value_dec) < abs(right_value_dec):
                    continue
                # 余り無しは結果が余り無しになるのをLoopし続けると時間がかかりすぎるため、
                # 素因数分解した割り切れる値からランダムに選択する仕様とする
                divide_arg = Decimal(0)
                minus_flg = left_value_dec < 0 or right_value_dec < 0
                divide_arg = Decimal(str(abs(left_value_dec)))
                divide_list = get_divide_list(divide_arg)

                # 割り切れない場合は再試行
                if len(divide_list) == 0:
                    continue
                #ﾏｲﾅｽの場合はﾏｲﾅｽも候補に追加する
                if minus_flg == True:
                    divide_list_copy = divide_list.copy()
                    for d in divide_list_copy:
                        divide_list.append(-d)
                # 桁数固定の場合右辺が一致する解を取得しその中からランダムで右辺を決定する

                fix_divide_list = []
                for p in divide_list:
                    if keta_fix_right_flg == KETA_FIX_ON:
                        if len(str(abs(p))) == right_input:
                            if right_value_dec < 0:
                                if  p < 0:
                                    fix_divide_list.append(p)
                            else:
                                if  p >= 0:
                                    fix_divide_list.append(p)
                    else:
                        if len(str(abs(p))) <= right_input:
                            if right_value_dec < 0:
                                if  p < 0:
                                    fix_divide_list.append(p)
                            else:
                                if  p >= 0:
                                    fix_divide_list.append(p)
                if len(fix_divide_list) == 0:
                    continue

                divide_idx = random.randint(0, len(fix_divide_list) - 1)
                right_value_dec = Decimal(fix_divide_list[divide_idx])

            elif mod_select == MOD_ON:
                if abs(left_value_dec) < abs(right_value_dec):
                    continue

            answer_dec = 0
            answer_mod_dec = 0
            try:
                answer_dec = left_value_dec / right_value_dec
                answer_mod_dec = left_value_dec % right_value_dec
                if mod_select == MOD_ON and answer_mod_dec != 0:
                    if answer_dec < 0:
                        answer_dec = Decimal(math.ceil(answer_dec))
                    else:
                        answer_dec = Decimal(math.floor(answer_dec))
            except ZeroDivisionError:
                # 結果が0除算はやり直す
                continue

            # 余りあり指定で余りが0のものはやり直す
            if mod_select == MOD_ON and answer_mod_dec == 0:
                continue

        elif tmp_drill_type == PLUS_CODE: #足し算
            answer_dec = int(left_value_dec) + int(right_value_dec)
        elif tmp_drill_type == MINUS_CODE: #引き算
            answer_dec = int(left_value_dec) - int(right_value_dec)
        elif tmp_drill_type == MULTIPLCODE: #掛け算
            answer_dec = int(left_value_dec) * int(right_value_dec)

        # ﾏｲﾅｽ無し 結果がﾏｲﾅｽの場合やり直す
        if answer_minus_flg == ANSWER_MINUS_OFF:
            if answer_dec < 0:
                continue

        # ﾏｲﾅｽ固定 結果がﾏｲﾅｽでない場合やり直す
        if answer_minus_flg == ANSWER_MINUS_ONLY:
            if answer_dec >= 0:
                continue

        drill_data = [0, tmp_drill_type, mod_select, int(left_value_dec), int(right_value_dec), answer_dec, int(answer_mod_dec)]

        if right_input != 1 and left_input != 1:
            if drill_list.__contains__(drill_data) == False:
                drill_list.append(drill_data)
                loop_cnt = 0
        else:
                drill_list.append(drill_data)
                loop_cnt = 0

        # 問題数上限となったら終了
        if len(drill_list) == mondai_cnt:
            break

    # 問題番号をつける
    drill_no = 1
    for siki in drill_list:
        siki[0] = drill_no
        drill_no += 1

    return drill_list

# 問題タイプを名を取得する
def get_mondai_name(mondai_type):
    mondai_name="ひっ算"
    if mondai_type == MONDAI_TYPE_NORMAL:
        mondai_name="通常"
    elif mondai_type == MONDAI_TYPE_REVERSE:
        mondai_name = "逆算"
    return mondai_name

# ドリル名を取得する
def get_drill_name(drill_type):

    drill_name=""
    if drill_type == DIVIDE_CODE:
         drill_name = "割り算"
    elif drill_type == PLUS_CODE: #足し算
        drill_name = "足し算"
    elif drill_type == MINUS_CODE: #引き算
        drill_name = "引き算"
    elif drill_type == MULTIPLCODE: #掛け算
        drill_name = "かけ算"
    elif drill_type == RANDOM_CODE: #ランダム
        drill_name = "ランダム"
    return drill_name

# NgPatternモデルを新規で取得する
def get_ng_pattern_model(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select):
    new_ng_ptn = NgPattern(drill_type=str(drill_type), left_input=str(left_input)
    ,right_input=str(right_input), answer_select=str(answer_select)
    ,keta_fix_left_flg=str(keta_fix_left_flg),keta_fix_right_flg=str(keta_fix_right_flg), left_minus_flg=str(left_minus_flg)
    ,right_minus_flg=str(right_minus_flg), answer_minus_flg=str(answer_minus_flg)
    ,mod_select=str(mod_select))
    new_ng_ptn.hash_key = new_ng_ptn.get_hash()
    return new_ng_ptn

# NGパターンをDBより取得する
def get_ng_pattern(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select):

    new_ng_ptn = get_ng_pattern_model(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select)
    return NgPattern.objects.all().filter(hash_key=new_ng_ptn.hash_key)

# NGパターンがDBに存在しなければ作成する
def create_ng_pattern(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select):

    flag = exists_ng_pattern(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select)
    if flag == False:
        get_ng_pattern_model(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select).save()

# NGパターンがDBに存在するかの確認
def exists_ng_pattern(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select):
        ng_ptn = get_ng_pattern(drill_type, left_input, right_input, answer_select
        , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
        , right_minus_flg, answer_minus_flg, mod_select)
        return len(ng_ptn) > 0

# 計算ドリル作成処理
def create_drill_exec(request):

    #POSTパラメーターを取得する
    content_type = request.POST.get("content-type")
    enc_type = request.POST.get("enc-type")
    drill_type = int(request.POST.get("drill_type"))
    left_input = int(request.POST.get("left_input"))
    right_input = int(request.POST.get("right_input"))
    answer_select = int(request.POST.get("answer_select"))
    keta_fix_left_flg = int(request.POST.get("keta_fix_left_select"))
    keta_fix_right_flg = int(request.POST.get("keta_fix_right_select"))
    left_minus_flg = int(request.POST.get("left_minus_select"))
    right_minus_flg = int(request.POST.get("right_minus_select"))
    answer_minus_flg = int(request.POST.get("answer_minus_select"))
    mondai_cnt = int(request.POST.get("mondai_cnt_select")) * 10
    mondai_type = int(request.POST.get("mondai_type_select"))

    mod_select = 0
    if drill_type == DIVIDE_CODE or drill_type == RANDOM_CODE:
        mod_select = int(request.POST.get("mod_select"))

    simulation = False

    if simulation == True:

        # 解答可否判定情報を作成するための機能のため、コメントは削除してはいけない！！
        drill_type_list = [PLUS_CODE,MINUS_CODE,MULTIPLCODE,DIVIDE_CODE,RANDOM_CODE]
        left_minus_input_list = [MINUS_INPUT_OFF,MINUS_INPUT_ON,MINUS_INPUT_ONLY]
        right_minus_input_list = [MINUS_INPUT_OFF,MINUS_INPUT_ON,MINUS_INPUT_ONLY]

        left_keta_input_list = [KETA_INPUT_0,KETA_INPUT_1,KETA_INPUT_2,KETA_INPUT_3,KETA_INPUT_4,KETA_INPUT_5,KETA_INPUT_6,KETA_INPUT_7,KETA_INPUT_8,KETA_INPUT_9,KETA_INPUT_10]
        right_keta_input_list = [KETA_INPUT_0,KETA_INPUT_1,KETA_INPUT_2,KETA_INPUT_3,KETA_INPUT_4,KETA_INPUT_5,KETA_INPUT_6,KETA_INPUT_7,KETA_INPUT_8,KETA_INPUT_9,KETA_INPUT_10]
        keta_fix_left_list = [KETA_FIX_OFF,KETA_FIX_ON]
        keta_fix_right_list = [KETA_FIX_OFF,KETA_FIX_ON]

        answer_minus_list = [ANSWER_MINUS_OFF,ANSWER_MINUS_ON,ANSWER_MINUS_ONLY]
        mod_list = [MOD_OFF,MOD_ON,MOD_DECIMAL]

        max = len(drill_type_list) * len(left_minus_input_list) * len(right_minus_input_list) \
        * len(left_keta_input_list) * len(right_keta_input_list) * len(keta_fix_left_list)  * len(keta_fix_right_list) \
        * len(answer_minus_list) * len(mod_list)
        logging.debug("max : " + str(max))
        cnt = 0
        for v0 in drill_type_list:
            drill_type = v0
            for v1 in left_keta_input_list:
                left_input = v1
                for v2 in right_keta_input_list:
                    right_input = v2
                    for v3 in left_minus_input_list:
                        left_minus_flg = v3
                        for v4 in right_minus_input_list:
                            right_minus_flg = v4
                            for v5 in keta_fix_left_list:
                                keta_fix_left_flg = v5
                                for v6 in keta_fix_right_list:
                                    keta_fix_right_flg = v6
                                    for v7 in answer_minus_list:
                                        answer_minus_flg = v7
                                        for v8 in mod_list:
                                            mod_select = v8

                                            cnt += 1
                                            if cnt % 100 == 0:
                                                logging.debug(str(cnt) + "/" + str(max))
                                            # 計算ドリルを作成する
                                            drill_list = create_drill_list(request, drill_type, left_input
                                            , right_input, answer_select, keta_fix_left_flg, keta_fix_right_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select, mondai_cnt)
                                            if len(drill_list) == 0:
                                                log = "計算ﾀｲﾌﾟ:" + str(drill_type)
                                                log += " 左辺:" + str(left_input)
                                                log += " 右辺:" + str(right_input)
                                                log += " 左辺ﾏｲﾅｽ:" + str(left_minus_flg)
                                                log += " 右辺ﾏｲﾅｽ:" + str(right_minus_flg)
                                                log += " 余り有無:" + str(mod_select)
                                                log += " 左辺指定桁固定:" + str(keta_fix_left_flg)
                                                log += " 右辺指定桁固定:" + str(keta_fix_right_flg)
                                                log += " 答えﾏｲﾅｽ:" + str(answer_minus_flg)
                                                create_ng_pattern(drill_type = drill_type
                                                , left_input = left_input
                                                , right_input = right_input
                                                , answer_select = answer_select
                                                , keta_fix_left_flg = keta_fix_left_flg
                                                , keta_fix_right_flg = keta_fix_right_flg
                                                , left_minus_flg = left_minus_flg
                                                , right_minus_flg = right_minus_flg
                                                , answer_minus_flg = answer_minus_flg
                                                , mod_select = mod_select)
                                                logging.debug(log)

        drill_list = []

    if exists_ng_pattern(drill_type, left_input, right_input, answer_select
    , keta_fix_left_flg, keta_fix_right_flg, left_minus_flg
    , right_minus_flg, answer_minus_flg, mod_select) == True:
        context['message'] = '問題作成の出来ない組み合わせの可能性があります。設定を見直してください。'
        context['message_type'] = "alert-warning"
        form = forms.DrillTypeForm(request.POST)
        c = {'context': context, 'form': form}
        c.update(csrf(request))
        return render(request,
                'sansudrill/index.html',
                c)

    # Decimalを初期化する
    getcontext().Emin = -999999999999999
    getcontext().Emax = 999999999999999
    getcontext().prec = 15

    # 計算ドリルを作成する
    drill_list = create_drill_list(request, drill_type, left_input
    , right_input, answer_select, keta_fix_left_flg, keta_fix_right_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select, mondai_cnt)

    # 処理が基底ループ回数で終わらなかった場合は終了する
    if len(drill_list) == 0:

        context['message'] = '問題作成の出来ない組み合わせの可能性があります。設定を見直してください。'
        context['message_type'] = "alert-warning"
        form = forms.DrillTypeForm(request.POST)
        c = {'context': context, 'form': form}
        c.update(csrf(request))
        return render(request,
                'sansudrill/index.html',
                c)

    if content_type == "pdf":
        return exec_pdf_output(drill_type, left_input, right_input, answer_select, drill_list, mondai_cnt, mondai_type)

    if content_type == "csv":
        return exec_csv_output(drill_type, answer_select, drill_list, enc_type)

    if content_type == "xls":
        return exec_xls_output(drill_type, answer_select, drill_list)

# excelを出力
def exec_xls_output(drill_type, answer_select, drill_list):

    filename = 'drill_' + dt.now().strftime('%Y%m%d%H%M%S') + '.xlsx'  # 出力ファイル名
    output = BytesIO()
    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet('Sheet1')
    format = wb.add_format({'align': 'center'})

    row = 0
    for drill in drill_list:

        kigo = ""
        if drill[1] == PLUS_CODE:
            kigo = "＋"
        elif drill[1] == MINUS_CODE:
            kigo = "－"
        elif drill[1] == MULTIPLCODE:
            kigo = "×"
        elif drill[1] == DIVIDE_CODE:
            kigo = "÷"
        ans = 0
        amari = 0

        if answer_select == 2:
            if drill[1] == DIVIDE_CODE and drill[2] == 3 and str(drill[5]).__contains__("."):
                ans_num = drill[5].quantize(Decimal("0.00001"))
                ans = str(ans_num)
            else:
                ans_num = drill[5]
                ans = str(ans_num)

            if drill[2] == 2 and drill[6] != 0:
                amari = drill[6]
        ws.write(row, 0, drill[3], format)
        ws.write(row, 1, kigo, format)
        ws.write(row, 2, drill[4], format)
        ws.write(row, 3, "＝", format)
        ws.write(row, 4, ans, format)
        if amari != 0:
            ws.write(row, 5, amari, format)
        row+=1

    wb.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + filename
    return response

# csvを出力
def exec_csv_output(drill_type, answer_select, drill_list, enc_type):
    filename = 'drill_' + dt.now().strftime('%Y%m%d%H%M%S') + '.csv'  # 出力ファイル名

    if enc_type == "sjis":
        response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    else:
        response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename=' + filename



    writer = csv.writer(response)
    for drill in drill_list:

        kigo = ""
        if drill[1] == PLUS_CODE:
            kigo = "+"
        elif drill[1] == MINUS_CODE:
            kigo = "-"
        elif drill[1] == MULTIPLCODE:
            kigo = "×"
        elif drill[1] == DIVIDE_CODE:
            kigo = "÷"
        ans = ""
        amari = ""
        if answer_select == 2:
            if drill[1] == DIVIDE_CODE and drill[2] == 3 and str(drill[5]).__contains__("."):
                ans_num = drill[5].quantize(Decimal("0.00001"))
                ans = str(ans_num)
            else:
                ans_num = drill[5]
                ans = str(ans_num)

            if drill[2] == 2 and drill[6] != 0:
                amari = drill[6]
        writer.writerow([drill[3], kigo , drill[4], "=", ans, amari ])

    return response

# pdfを出力
def exec_pdf_output(drill_type, left_input, right_input, answer_select, drill_list, mondai_cnt, mondai_type):

    slide_cnt = get_slide_range(mondai_cnt)
    drill_name = get_drill_name(drill_type)
    mondai_name = get_mondai_name(mondai_type)
    filename = 'drill_' + dt.now().strftime('%Y%m%d%H%M%S') + '.pdf'  # 出力ファイル名
    title = '算数ドリル'
    footer = "keisan-drill.com"
    width, height = A4

    # A4縦書きのpdfを作る
    page_size = portrait(A4)

    # PDF出力
    response = HttpResponse(status=200, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    # pdfを描く場所を作成：位置を決める原点は左上にする(bottomup)
    # デフォルトの原点は左下
    p = canvas.Canvas(response, pagesize=page_size, bottomup=True)
    #pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    pdfmetrics.registerFont(TTFont(FONT_NAMEPDF, os.path.dirname(settings.BASE_DIR) + '/fonts/ipaexg.ttf'))
    font_size = 12
    p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定
    # pdfのタイトルを設定
    p.setTitle(title)

    footer_width = pdfmetrics.stringWidth(footer, FONT_NAMEPDF, font_size)

    # 桁数合計を取得
    input_sum = left_input + right_input
    #12桁以内は1ページに出力
    if input_sum <= 12:

        draw_title(p, width, height, drill_name, False, mondai_name, mondai_cnt)

        font_size = 12
        p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定

        for col in range(2):
            y = height - 60
            if col == 0:
                x = 15
                start = 0
            else:
                x = width / 2 + 7
                start = slide_cnt

            draw_keisan(p, font_size, x, y, start, drill_type, drill_list, False, mondai_cnt, mondai_type)

        p.setFillColorRGB(0.5,0.5,0.5)
        p.drawString((width - footer_width) / 2 , 15, footer)
        p.setFillColorRGB(1, 1, 1)

        p.showPage()
    else:
        for col in range(2):

            draw_title(p, width, height, drill_name, False, mondai_name, mondai_cnt)

            # p.drawString(width - 50, height - 35, str(col + 1) + "/2")

            font_size = 12
            p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定

            x = 25
            y = height - 60
            if col == 0:
                start = 0
            else:
                start = slide_cnt

            draw_keisan(p, font_size, x, y, start, drill_type, drill_list, False, mondai_cnt, mondai_type)

            p.setFillColorRGB(0.5,0.5,0.5)
            p.drawString((width - footer_width) / 2 , 15, footer)
            p.setFillColorRGB(1, 1, 1)

            p.showPage()

    if answer_select == 2:

        #16以内は1ページに出力
        if input_sum <= 12:

            draw_title(p, width, height, drill_name, True, mondai_name, mondai_cnt)

            font_size = 12
            p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定

            for col in range(2):
                y = height - 60
                if col == 0:
                    x = 15
                    start = 0
                else:
                    x = width / 2 + 7
                    start = slide_cnt

                draw_keisan(p, font_size, x, y, start, drill_type, drill_list, True, mondai_cnt, mondai_type)

            p.setFillColorRGB(0.5,0.5,0.5)
            p.drawString((width - footer_width) / 2 , 15, footer)
            p.setFillColorRGB(1, 1, 1)
            p.showPage()
        else:
            for col in range(2):

                draw_title(p, width, height, drill_name, True, mondai_name, mondai_cnt)

                # p.drawString(width - 50, height - 35, str(col + 1) + "/2")

                font_size = 12
                p.setFont(FONT_NAMEPDF, font_size)  # フォントを設定

                x = 25
                y = height - 60
                if col == 0:
                    start = 0
                else:
                    start = slide_cnt

                draw_keisan(p, font_size, x, y, start, drill_type, drill_list, True, mondai_cnt, mondai_type)

                p.setFillColorRGB(0.5,0.5,0.5)
                p.drawString((width - footer_width) / 2 , 15, footer)
                p.setFillColorRGB(1, 1, 1)
                p.showPage()

    p.save()

    return response

# 計算ドリルを作成する
def create_drill(request):
    init_context()
    if request.method == 'GET':

        form = forms.DrillTypeForm()
        c = {'context': context, 'form': form}
        c.update(csrf(request))
        return render(request,
                'sansudrill/index.html',
                c)

    if request.method == 'POST':
        form = forms.DrillTypeForm(request.POST)

        if form.is_valid():
            return create_drill_exec(request)

        else:
            c = {'context': context, 'form': form}
            c.update(csrf(request))
            return render(request,
                        'sansudrill/index.html',
                        c)

# 初期ページ
def index(request):
    init_context()
    if request.method == 'POST':
        form = forms.DrillTypeForm(request.POST)
        form.is_valid()
        c = {'context': context, 'form': form}
    else:

        form = forms.DrillTypeForm()
        c = {'context': context, 'form': form}

    c.update(csrf(request))
    return render(request,
                'sansudrill/index.html',
                c)