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

#コンテキスト
context = {'title':'計算ドリル', 'message_type':'alert-info', 'message':'', 'timestamp':dt.now().strftime('%Y%m%d%H%M%S')}

# 最大ループ回数
MAX_LOOP_COUNT = 100000

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
def create_randint(value):
    result = 0
    number_max = "0"
    num = 0
    while num != value:
        num+=1
        number_max += "9"

    result = random.randint(0, int(number_max))
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
def draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, answer_dec):
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
            if drill_type == 4 and drill_list[num + start][2] == 3 and str(drill_list[num + start][5]).__contains__("."):
                ans_num = drill_list[num + start][5].quantize(Decimal("0.00001"))
                ans = str(ans_num)
            else:
                ans_num = drill_list[num + start][5]
                ans = str(ans_num)
            p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5, y, ans)

            if drill_list[num + start][2] == 2 and drill_list[num + start][6] != 0:
                ans_width = pdfmetrics.stringWidth(ans, font_name, font_size)
                p.drawString(x + add_x1 + sahen_width + 2 + kigo_width + 2 + uhen_width + 5 + equals_width + 5 + ans_width, y, "余り" + str(drill_list[num + start][6]))

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
, answer_select, keta_fix_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select):
    # 作成した計算式を格納
    drill_list = []
    cnt = 0
    while True:
        cnt+=1
        if cnt > MAX_LOOP_COUNT:
            return []
        # 桁固定の場合
        if keta_fix_flg == 2:
            left_number_str = create_randint2(left_input, False)
            right_number_str = create_randint2(right_input, False)
        else:
            left_number_str = create_randint(left_input)
            right_number_str = create_randint(right_input)

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

        if drill_type == 4: # 割り算

            # どちらかが0はやり直す
            if left_value_dec == 0 or right_value_dec == 0:
                continue
            # 同数値もループ
            if left_value_dec == right_value_dec:
                continue

            if mod_select == 1: #余り無し
                if abs(left_value_dec) < abs(right_value_dec):
                    continue
                # 余り無しは結果が余り無しになるのをLoopし続けると時間がかかりすぎるため、
                # 素因数分解した割り切れる値からランダムに選択する仕様とする
                divide_arg = Decimal(0)
                minus_flg = left_value_dec < 0
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
                if keta_fix_flg == 2:
                    fix_divide_list = []
                    for p in divide_list:
                        if len(str(abs(p))) == right_input:
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
                else:
                    divide_idx = random.randint(0, len(divide_list) - 1)
                    right_value_dec = Decimal(divide_list[divide_idx])
            elif mod_select == 2:
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
            if mod_select == 2 and answer_mod_dec == 0:
                continue

        elif drill_type == 1: #足し算
            answer_dec = left_value_dec + right_value_dec
        elif drill_type == 2: #引き算
            answer_dec = left_value_dec - right_value_dec
        elif drill_type == 3: #掛け算
            answer_dec = left_value_dec * right_value_dec

        # ﾏｲﾅｽ無し 結果がﾏｲﾅｽの場合やり直す
        if answer_minus_flg == 1:
            if answer_dec < 0:
                continue

        # ﾏｲﾅｽ固定 結果がﾏｲﾅｽでない場合やり直す
        if answer_minus_flg == 3:
            if answer_dec >= 0:
                continue

        drill_data = [0, drill_type, mod_select, int(left_value_dec), int(right_value_dec), answer_dec, int(answer_mod_dec)]
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
    right_input = int(request.POST.get("right_input"))
    answer_select = int(request.POST.get("answer_select"))
    keta_fix_flg = int(request.POST.get("keta_fix_select"))
    left_minus_flg = int(request.POST.get("left_minus_select"))
    right_minus_flg = int(request.POST.get("right_minus_select"))
    answer_minus_flg = int(request.POST.get("answer_minus_select"))

    mod_select = 0
    if drill_type == 4:
        mod_select = int(request.POST.get("mod_select"))
    drill_name = get_drill_name(drill_type)
    # Decimalを初期化する
    getcontext().Emin = -999999999999999
    getcontext().Emax = 999999999999999
    getcontext().prec = 15

    # left_minus_input_list = [1,2,3]
    # right_minus_input_list = [1,2,3]
    # keta_input_list = [[2,3],[3,3],[3,2]]
    # keta_fix_list = [1,2]
    # answer_minus_list = [1,2,3]
    # mod_list = [1,2,3]

    # for v1 in left_minus_input_list:
    #     left_minus_flg = v1
    #     for v2 in right_minus_input_list:
    #         right_minus_flg = v2
    #         for v3 in keta_input_list:
    #             left_input = v3[0]
    #             right_input = v3[1]
    #             for v4 in keta_fix_list:
    #                 keta_fix_flg = v4
    #                 for v5 in answer_minus_list:
    #                     answer_minus_flg = v5
    #                     for v6 in mod_list:
    #                         mod_select = v6
    #                         # 計算ドリルを作成する
    #                         drill_list = create_drill_list(request, drill_type, left_input
    #                         , right_input, answer_select, keta_fix_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select)

    #                         if len(drill_list) == 0:
    #                             log = "左辺ﾏｲﾅｽ:" + str(left_minus_flg)
    #                             log += " 左辺:" + str(left_input)
    #                             log += " 右辺ﾏｲﾅｽ:" + str(right_minus_flg)
    #                             log += " 右辺:" + str(right_input)
    #                             log += " 余り有無:" + str(mod_select)
    #                             log += " 指定桁固定:" + str(keta_fix_flg)
    #                             log += " 答えﾏｲﾅｽ:" + str(answer_minus_flg)

    #                             logging.debug(log)

    # 計算ドリルを作成する
    drill_list = create_drill_list(request, drill_type, left_input
    , right_input, answer_select, keta_fix_flg, left_minus_flg, right_minus_flg, answer_minus_flg, mod_select)

    # 処理が基底ループ回数で終わらなかった場合は終了する
    if len(drill_list) == 0:
        context['message'] = '問題作成時間がかかりすぎます。桁数を絞ってお試しください。'
        context['message_type'] = "alert-warning"
        form = forms.DrillTypeForm(request.POST)
        c = {'context': context, 'form': form}
        c.update(csrf(request))
        return render(request,
                'sansudrill/index.html',
                c)

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
    input_sum = left_input + right_input
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

            draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, False)

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

            draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, False)

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

                draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, True)

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

                draw_keisan(p, font_name, font_size, x, y, start, drill_type, drill_list, True)

                p.showPage()

    p.save()

    #_draw(p)

    return response

# 計算ドリルを作成する
def create_drill(request):
    logging.debug("start - create_drill")
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