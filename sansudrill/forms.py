from django import forms
from django.core.exceptions import ValidationError
import logging
# 計算式選択フォーム
class DrillTypeForm(forms.Form):

    # 計算式タイプ
    KEISAN_CHOICE = [('1','足し算'),('2','引き算'),('3','掛け算'),('4','割り算'),('5','ランダム')]
    AMARI_CHOICE = [('1','余り無し'),('2','有り'),('3','小数点')]
    ANSWER_CHOIDE = [('1','しない'),('2','する')]
    KETA_FIX_CHOIDE = [('1','しない'),('2','する')]
    MINUS_CHOICE = [('1','無し'),('2','有り'),('3','マイナスのみ')]
    MONDAI_CNT_CHOICE = [('1','10問'),('2','20問'),('3','30問'),('4','40問'),('5','50問')]
    MONDAI_TYPE_CHOIDE = [('1','通常'),('2','逆算'),('3','ひっ算')]

    # カスタムバリデーションを行う
    def clean(self):
        mondai_type = self.cleaned_data.get('mondai_type_select')
        mondai_cnt = self.cleaned_data.get('mondai_cnt_select')
        if int(mondai_type) == 3:
            if int(mondai_cnt) >= 3:
                raise forms.ValidationError("ひっ算の場合は20問以下にしてください。")
        return self.cleaned_data

    # 計算タイプラジオ
    drill_type = forms.ChoiceField(
        label='',
        required=True,
        disabled=False,
        initial='1',
        choices=KEISAN_CHOICE,
        widget=forms.RadioSelect(attrs={
            'id': 'drill_type','class': 'form-check-input', 'data-action':'/'}))

    # 左辺整数部分
    left_input = forms.IntegerField(
        label='左辺整数部',
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
        min_value=0,
        max_value=8,
        initial=3,
        required=True,
        error_messages={
        'min_value':'左辺整数部は0以上です。'
        ,'max_value':'左辺整数部は10以下です。'
        ,'required':'左辺整数部は入力必須です。'},)

    # 右辺整数部分
    right_input = forms.IntegerField(
        label='右辺整数部',
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
        min_value=0,
        max_value=8,
        initial=3,
        required=True,
        error_messages={
        'min_value':'右辺整数部は1以上です。'
        ,'max_value':'右辺整数部は10以下です。'
        ,'required':'右辺整数部は入力必須です。'},)


    # 左辺小数部分
    left_small_input = forms.IntegerField(
        label='左辺小数部',
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
        min_value=0,
        max_value=2,
        initial=0,
        required=True,
        error_messages={
        'min_value':'左辺小数部は0以上です。'
        ,'max_value':'左辺小数部は2以下です。'
        ,'required':'左辺小数部は入力必須です。'},)

    # 右辺小数部分
    right_small_input = forms.IntegerField(
        label='右辺小数部',
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
        min_value=0,
        max_value=2,
        initial=0,
        required=True,
        error_messages={
        'min_value':'右辺小数部は0以上です。'
        ,'max_value':'右辺小数部は2以下です。'
        ,'required':'右辺小数部は入力必須です。'},)

    # 余り有無
    mod_select = forms.ChoiceField(
        choices=AMARI_CHOICE,
        required=False,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 答え出力
    answer_select = forms.ChoiceField(
        choices=ANSWER_CHOIDE,
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 指定桁固定
    keta_fix_left_select  = forms.ChoiceField(
        choices=KETA_FIX_CHOIDE,
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 指定桁固定
    keta_fix_right_select  = forms.ChoiceField(
        choices=KETA_FIX_CHOIDE,
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # マイナス有無
    left_minus_select  = forms.ChoiceField(
        choices=MINUS_CHOICE,
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # マイナス有無
    right_minus_select  = forms.ChoiceField(
        choices=MINUS_CHOICE,
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 答えマイナス
    answer_minus_select  = forms.ChoiceField(
        choices=MINUS_CHOICE,
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )

    # 問題数
    mondai_cnt_select  = forms.ChoiceField(
        choices=MONDAI_CNT_CHOICE,
        required=True,
        initial='5',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 計算式タイプ
    mondai_type_select  = forms.ChoiceField(
        choices=MONDAI_TYPE_CHOIDE,
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )

    # 問題コード
    load_drill_type_input = forms.CharField(
        label='問題コード',
        required=False,
        initial='',
        widget=forms.TextInput(attrs={'class':'text-left form-control'}),
    )
