import logging
import random
import reportlab
import math
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from . import forms
from datetime import datetime as dt

from reportlab.pdfgen import canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from decimal import Decimal, getcontext, Overflow, DivisionByZero, InvalidOperation

context = {'title':'計算ドリル', 'message':'', 'timestamp':dt.now().strftime('%Y%m%d%H%M%S')}

def init_context():
    context['message'] = ""
    context['timestamp'] = dt.now().strftime('%Y%m%d%H%M%S')

# 描画
def _draw(p):
    pass

# ランダムな整数を取得する
def create_randint(value):
    result = 0
    if value > 0:
        number_max = 1
        num = 0
        while num < value:
            number_max *= 10
            num += 1

        result = random.randint(0, number_max) - 1
        if result < 0:
            result = 0
    return str(result)

# ランダムな整数を取得する
def create_randint2(value, is_shosu):
    result = ""
    if value == 0:
        return 0

    for num in range(value):
        if is_shosu:
            if num == value - 1:
                result += str(random.randint(1, 9))
            else:
                result += str(random.randint(0, 9))
        else:
            if num == 0:
                result += str(random.randint(1, 9))
            else:
                result += str(random.randint(0, 9))

    return str(result)

# ドリルタイトルを描画する
def draw_title(p, font_name, width, height, drill_name, answer_dec):

    inner_title = '算数ドリル('+drill_name+')'
    if answer_dec:
        inner_title += "(答え)"
    font_size = 18
    str_width = pdfmetrics.stringWidth(inner_title, font_name, font_size)
    str_height = pdfmetrics.getAscent(font_name, font_size) + pdfmetrics.getDescent(font_name, font_size)
    x = width / 2 - str_width / 2
    y = height - 25 - str_height
    p.setFont(font_name, font_size)  # フォントを設定
    p.drawString(x, y, inner_title)

# 計算問題をPDFに描画する
def draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, answer_dec, mod_flg):
    for num in range(25):
        y -= 31
        p.drawString(x, y, str(drill_list[num + start][0]) + ")")

        kigo = ""
        if drill_type == 1:
            kigo = "+"
        elif drill_type == 2:
            kigo = "-"
        elif drill_type == 3:
            kigo = "×"
        elif drill_type == 4:
            kigo = "÷"

        kigo_width = pdfmetrics.stringWidth(kigo, font_name, font_size)
        sahen = str(drill_list[num + start][3])
        sahen_width = pdfmetrics.stringWidth(sahen, font_name, font_size)
        add_x1 = 27
        p.drawString(x + add_x1, y, sahen)
        p.drawString(x + add_x1 + sahen_width + 2, y, kigo)

        uhen = str(drill_list[num + start][4])
        if drill_list[num + start][4] < 0:
            uhen = "(" + uhen + ")"

        uhen_width = pdfmetrics.stringWidth(uhen, font_name, font_size)
        p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2, y, uhen)
        p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5, y, "=")

        equals_width = pdfmetrics.stringWidth("=", font_name, font_size)

        if answer_dec:
            if drill_type == 4 and mod_flg == False:
                ans_num = drill_list[num + start][5].quantize(Decimal("0.00001"))
                ans = str(ans_num)
            else:
                ans_num = drill_list[num + start][5]
                ans = str(ans_num)
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5, y, ans)
            if drill_list[num + start][2] == True and drill_list[num + start][6] != 0:
                ans_width = pdfmetrics.stringWidth(ans, font_name, font_size)
                p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5 + ans_width, y, "余り" + str(drill_list[num + start][6]))

#計算ドリルリストを作成する
def create_drill_list(request, drill_type, left_input, left_small_input, right_input
, right_small_input, answer_select, keta_fix_flg, left_minus_flg, right_minus_flg, answer_minus_flg):
    # 作成した計算式を格納
    drill_list = []
    # 余りフラグ
    mod_flg = False

    while True:

        # 桁固定の場合
        if keta_fix_flg == 2:
            left_number_str = create_randint2(left_input, False)
            left_small_number_str = create_randint2(left_small_input, True)
            right_number_str = create_randint2(right_input, False)
            right_small_number_str = create_randint2(right_small_input, True)
        else:
            left_number_str = create_randint(left_input)
            left_small_number_str = create_randint(left_small_input)
            right_number_str = create_randint(right_input)
            right_small_number_str = create_randint(right_small_input)

        # 小数点とつなげる
        left_value_dec = Decimal(left_number_str)
        if left_small_number_str != 0:
            left_value_dec = Decimal.normalize(Decimal(left_number_str + "." + left_small_number_str))

        # ﾏｲﾅｽ有無
        if left_minus_flg == 2: # ﾏｲﾅｽ含む
            minus_div = random.randint(0,1)
            if minus_div == 1:
                left_value_dec *= Decimal(-1)
        if left_minus_flg == 3: # ﾏｲﾅｽ固定
            left_value_dec *= Decimal(-1)

        # 小数点とつなげる
        right_value_dec = Decimal(right_number_str)
        if right_small_number_str != 0:
            right_value_dec = Decimal.normalize(Decimal(right_number_str + "." + right_small_number_str))

        # ﾏｲﾅｽ有無
        if right_minus_flg == 2: # ﾏｲﾅｽ含む
            minus_div = random.randint(0,1)
            if minus_div == 1:
                right_value_dec *= Decimal(-1)
        if right_minus_flg == 3: # ﾏｲﾅｽ固定
            right_value_dec *= Decimal(-1)

        answer_dec = Decimal(0)
        answer_mod_dec = Decimal(0)

        if drill_type == 4: # 割り算

            # どちらかが0はやり直す
            if left_value_dec == 0 or right_value_dec == 0:
                continue

            # 余り有無を取得
            mod_select = int(request.POST.get("mod_select"))

            if mod_select == 2:
                if abs(left_value_dec) < abs(right_value_dec):
                    continue

            answer_dec = 0
            answer_mod_dec = 0
            try:
                answer_dec = left_value_dec / right_value_dec
                answer_mod_dec = left_value_dec % right_value_dec
                if mod_select == 2 and answer_mod_dec != 0:
                    if answer_dec < 0:
                        answer_dec = Decimal(math.ceil(answer_dec))
                    else:
                        answer_dec = Decimal(math.floor(answer_dec))
            except ZeroDivisionError:
                # 結果が0除算はやり直す
                continue

            # 余りあり指定で余りが0のものはやり直す
            mod_flg = mod_select == 2
            if mod_select == 2 and answer_mod_dec == 0:
                continue

        elif drill_type == 1: #足し算
            answer_dec = left_value_dec + right_value_dec
        elif drill_type == 2: #引き算
            answer_dec = left_value_dec - right_value_dec
        elif drill_type == 3: #掛け算
            answer_dec = left_value_dec * right_value_dec
            logging.debug(str(left_value_dec) + "*" + str(right_value_dec))

        # ﾏｲﾅｽ無し 結果がﾏｲﾅｽの場合やり直す
        if answer_minus_flg == 1:
            if answer_dec < 0:
                continue

        # ﾏｲﾅｽ固定 結果がﾏｲﾅｽでない場合やり直す
        if answer_minus_flg == 3:
            if answer_dec >= 0:
                continue

        drill_data = [0, drill_type, mod_flg, left_value_dec, right_value_dec, answer_dec, answer_mod_dec]
        if drill_list.__contains__(drill_data) == False:
            drill_list.append(drill_data)

        # 問題は50問とする
        if len(drill_list) == 50:
            break

    # 問題番号をつける
    cnt = 1
    for siki in drill_list:
        siki[0] = cnt
        cnt += 1

    return drill_list

# ドリル名を取得する
def get_drill_name(drill_type):
    drill_name=""
    if drill_type == 4:
         drill_name = "割り算"
    elif drill_type == 1: #足し算
        drill_name = "足し算"
    elif drill_type == 2: #引き算
        drill_name = "引き算"
    elif drill_type == 3: #掛け算
        drill_name = "かけ算"

    return drill_name
# 計算ドリル作成処理
def create_drill_exec(request):

    drill_type = int(request.POST.get("drill_type"))
    left_input = int(request.POST.get("left_input"))
    left_small_input = int(request.POST.get("left_small_input"))
    right_input = int(request.POST.get("right_input"))
    right_small_input = int(request.POST.get("right_small_input"))
    answer_select = int(request.POST.get("answer_select"))
    keta_fix_flg = int(request.POST.get("keta_fix_select"))
    left_minus_flg = int(request.POST.get("left_minus_select"))
    right_minus_flg = int(request.POST.get("right_minus_select"))
    answer_minus_flg = int(request.POST.get("answer_minus_select"))
    drill_name = get_drill_name(drill_type)

    mod_flg = False
    if drill_type == 4: # 割り算
        mod_flg = int(request.POST.get("mod_select")) == 2
    # Decimalを初期化する
    getcontext().Emin = -999999999999999
    getcontext().Emax = 999999999999999
    getcontext().prec = 15

    # 計算ドリルを作成する
    drill_list = create_drill_list(request, drill_type, left_input, left_small_input
    , right_input, right_small_input, answer_select, keta_fix_flg, left_minus_flg, right_minus_flg, answer_minus_flg)

    filename = 'drill_' + dt.now().strftime('%Y%m%d%H%M%S') + '.pdf'  # 出力ファイル名
    title = '算数ドリル'
    font_name = 'HeiseiKakuGo-W5'  # フォント
    width, height = A4

    # PDF出力
    response = HttpResponse(status=200, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    # A4縦書きのpdfを作る
    size = portrait(A4)

    # pdfを描く場所を作成：位置を決める原点は左上にする(bottomup)
    # デフォルトの原点は左下
    p = canvas.Canvas(response, pagesize=size, bottomup=True)
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    font_size = 12
    p.setFont(font_name, font_size)  # フォントを設定
    # pdfのタイトルを設定
    p.setTitle(title)

    # 桁数合計を取得
    input_sum = left_input + right_input + left_small_input + right_small_input

    #12桁以内は1ページに出力
    if input_sum <= 12:

        draw_title(p, font_name, width, height, drill_name, False)

        font_size = 12
        p.setFont(font_name, font_size)  # フォントを設定

        for col in range(2):
            y = height - 30
            if col == 0:
                x = 5
                start = 0
            else:
                x = width / 2
                start = 25

            draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, False, mod_flg)

        p.showPage()
    else:
        for col in range(2):

            draw_title(p, font_name, width, height, drill_name, False)

            p.drawString(width - 50, height - 35, str(col + 1) + "/2")

            font_size = 12
            p.setFont(font_name, font_size)  # フォントを設定

            x = 25
            y = height - 30
            if col == 0:
                start = 0
            else:
                start = 25

            draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, False, mod_flg)

            p.showPage()

    if answer_select == 2:

        #16以内は1ページに出力
        if input_sum <= 12:

            draw_title(p, font_name, width, height, drill_name, True)

            font_size = 12
            p.setFont(font_name, font_size)  # フォントを設定

            for col in range(2):
                y = height - 30
                if col == 0:
                    x = 5
                    start = 0
                else:
                    x = width / 2
                    start = 25

                draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, True, mod_flg)

            p.showPage()
        else:
            for col in range(2):

                draw_title(p, font_name, width, height, drill_name, True)

                p.drawString(width - 50, height - 35, str(col + 1) + "/2")

                font_size = 12
                p.setFont(font_name, font_size)  # フォントを設定

                x = 25
                y = height - 30
                if col == 0:
                    start = 0
                else:
                    start = 25

                draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, True, mod_flg)

                p.showPage()

    p.save()

    _draw(p)

    return response

# 計算ドリルを作成する
def create_drill(request):
    logging.debug("start - create_drill")
    init_context()
    logging.debug("method : " + request.method)
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
            logging.debug("goto - drill.html")
            response = create_drill_exec(request)
            return response

        else:
            logging.debug("goto - index.html")
            c = {'context': context, 'form': form}
            c.update(csrf(request))
            return render(request,
                        'sansudrill/index.html',
                        c)

def index(request):
    logging.debug("start - index")
    init_context()
    if request.method == 'POST':
        form = forms.DrillTypeForm(request.POST)
        c = {'context': context, 'form': form}
        form.is_valid()
    else:
        form = forms.DrillTypeForm()
        c = {'context': context, 'form': form}

    c.update(csrf(request))
    return render(request,
                'sansudrill/index.html',
                c)