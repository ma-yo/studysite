from django import forms
from django.core.exceptions import ValidationError
import logging
class DrillTypeForm(forms.Form):

    # バリデーションを実行する
    def clean(self):
        logging.debug("clean")
        cleaned_data = super().clean()
        left_input = cleaned_data.get('left_input')
        left_small_input = cleaned_data.get('left_small_input')
        if left_input == 0 and left_small_input == 0:
            raise forms.ValidationError('整数部と少数部のどちらかは0以外でなければいけません。')

        right_input = self.cleaned_data.get('right_input')
        right_small_input = self.cleaned_data.get('right_small_input')
        if right_input == 0 and right_small_input == 0:
            raise forms.ValidationError('整数部と少数部のどちらかは0以外でなければいけません。')

        drill_type = cleaned_data.get('drill_type')
        left_minus_select = cleaned_data.get('left_minus_select')
        right_minus_select = cleaned_data.get('right_minus_select')
        answer_minus_select = cleaned_data.get('answer_minus_select')

        logging.debug("drill_type : " + str(drill_type))

        msg_1 = '答えがマイナスにしかならない設定での答えマイナス「無し」はできません。'
        msg_2 = '答えがマイナスにならない設定での答えマイナス「ﾏｲﾅｽのみ」はできません。'
        #足し算バリデーション
        if drill_type == '1':

            if answer_minus_select == '1' and left_minus_select == '3' and right_minus_select == '3':
                raise forms.ValidationError(msg_1)

            if answer_minus_select == '3' and left_minus_select == '1' and right_minus_select == '1':
                raise forms.ValidationError(msg_2)

        #引き算バリデーション
        if drill_type == '2':

            if answer_minus_select == '3' and left_minus_select == '1' and right_minus_select == '3':
                raise forms.ValidationError(msg_2)

        if drill_type == '3':

            if answer_minus_select == '1' and left_minus_select == '1' and right_minus_select == '3':
                raise forms.ValidationError(msg_1)

            if answer_minus_select == '1' and left_minus_select == '3' and right_minus_select == '1':
                raise forms.ValidationError(msg_1)

            if answer_minus_select == '3' and left_minus_select == '1' and right_minus_select == '1':
                raise forms.ValidationError(msg_2)

            if answer_minus_select == '3' and left_minus_select == '3' and right_minus_select == '3':
                raise forms.ValidationError(msg_2)

        if drill_type == '4':

            if answer_minus_select == '1' and left_minus_select == '1' and right_minus_select == '3':
                raise forms.ValidationError(msg_1)

            if answer_minus_select == '1' and left_minus_select == '3' and right_minus_select == '1':
                raise forms.ValidationError(msg_1)

            if answer_minus_select == '3' and left_minus_select == '1' and right_minus_select == '1':
                raise forms.ValidationError(msg_2)

            if answer_minus_select == '3' and left_minus_select == '3' and right_minus_select == '3':
                raise forms.ValidationError(msg_2)

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
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
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
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
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
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
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
        widget=forms.NumberInput(attrs={'class':'text-right form-control'}),
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
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 解答有無
    answer_select = forms.ChoiceField(
        choices=(('1','無し'),('2','有り')),
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
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # マイナス有無
    right_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
    # 答えマイナス
    answer_minus_select  = forms.ChoiceField(
        choices=(('1','無し'),('2','有り'),('3','ﾏｲﾅｽのみ')),
        required=True,
        initial='1',
        widget=forms.Select(attrs={'class':'text-left form-control'}),
    )
