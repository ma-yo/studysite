from django import forms
from django.core.exceptions import ValidationError
import logging
class DrillTypeForm(forms.Form):

    # バリデーションを実行する
    def clean(self):
        cleaned_data = super().clean()
        logging.debug("clean_left_input")
        input1 = cleaned_data.get('left_input')
        input2 = cleaned_data.get('left_small_input')
        if input1 == 0 and input2 == 0:
            raise forms.ValidationError('整数部と少数部のどちらかは0以外でなければいけません。')

        logging.debug("clean_right_input")
        input1 = self.cleaned_data.get('right_input')
        input2 = self.cleaned_data.get('right_small_input')
        if input1 == 0 and input2 == 0:
            raise forms.ValidationError('整数部と少数部のどちらかは0以外でなければいけません。')

        return cleaned_data

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
        widget=forms.NumberInput(attrs={'class':'text-right'}),
        min_value=0,
        max_value=10,
        initial=3,
        required=True,
        error_messages={
        'min_value':'左辺整数部は0以上です。'
        ,'max_value':'左辺整数部は10以下です。'
        ,'required':'左辺整数部は入力必須です。'},)

    # 左辺少数部分
    left_small_input  = forms.IntegerField(
        label='左辺少数部',
        widget=forms.NumberInput(attrs={'class':'text-right'}),
        min_value=0,
        max_value=5,
        initial=0,
        required=True,
        error_messages={
        'min_value':'左辺少数部は0以上です。'
        ,'max_value':'左辺少数部は5以下です。'
        ,'required':'左辺少数部は入力必須です。'},)

    # 右辺整数部分
    right_input = forms.IntegerField(
        label='右辺整数部',
        widget=forms.NumberInput(attrs={'class':'text-right'}),
        min_value=0,
        max_value=10,
        initial=3,
        error_messages={
        'min_value':'右辺整数部は1以上です。'
        ,'max_value':'右辺整数部は10以下です。'
        ,'required':'右辺整数部は入力必須です。'},
        required=True,)

    # 右辺少数部分
    right_small_input  = forms.IntegerField(
        label='右辺少数部',
        widget=forms.NumberInput(attrs={'class':'text-right'}),
        min_value=0,
        max_value=5,
        initial=0,
        required=True,
        error_messages={
        'min_value':'右辺少数部は0以上です。'
        ,'max_value':'右辺少数部は5以下です。'
        ,'required':'右辺少数部は入力必須です。'},)

    # 余り有無
    mod_select = forms.ChoiceField(
        choices=(('1','無し'),('2','有り')),
        required=False,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
    # 解答有無
    answer_select = forms.ChoiceField(
        choices=(('1','無し'),('2','有り')),
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
    # 指定桁固定
    keta_fix_select  = forms.ChoiceField(
        choices=(('1','しない'),('2','する')),
        required=True,
        initial='2',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
    # マイナス有無
    left_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
    # マイナス有無
    right_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
    # 答えマイナス
    answer_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left'}),
    )
