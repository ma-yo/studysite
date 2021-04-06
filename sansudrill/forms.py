from django import forms
from django.core.exceptions import ValidationError
import logging
# 計算式選択フォーム
class DrillTypeForm(forms.Form):

    # 計算式タイプ
    CHOICE = [
        ('1','足し算'),
        ('2','引き算'),
        ('3','掛け算'),
        ('4','割り算')]

    # 計算タイプラジオ
    drill_type = forms.ChoiceField(
        label='',
        required=True,
        disabled=False,
        initial='1',
        choices=CHOICE,
        widget=forms.RadioSelect(attrs={
            'id': 'drill_type','class': 'form-check-input', 'data-action':'/'}))

    # 左辺整数部分
    left_input = forms.IntegerField(
        label='左辺整数部',
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
        min_value=0,
        max_value=10,
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
        max_value=10,
        initial=3,
        error_messages={
        'min_value':'右辺整数部は1以上です。'
        ,'max_value':'右辺整数部は10以下です。'
        ,'required':'右辺整数部は入力必須です。'},
        required=True,)

    # 余り有無
    mod_select = forms.ChoiceField(
        choices=(('1','余り無し'),('2','有り'),('3','小数点')),
        required=False,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 答え出力
    answer_select = forms.ChoiceField(
        choices=(('1','しない'),('2','する')),
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 指定桁固定
    keta_fix_select  = forms.ChoiceField(
        choices=(('1','しない'),('2','する')),
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # マイナス有無
    left_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','マイナスのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # マイナス有無
    right_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','マイナスのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 答えマイナス
    answer_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','マイナスのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
