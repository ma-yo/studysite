from django import forms
from django.core.exceptions import ValidationError
import logging
class DrillTypeForm(forms.Form):

    d1_validate_list = []
    d2_validate_list = []
    d3_validate_list = []
    d4_validate_list = []

    def __init__(self, *args,**kwargs):
        super(DrillTypeForm, self).__init__(*args, **kwargs)
        self.d1_validate_list.append([1 ,2 ,1 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,2 ,1 ,3 ,2 ,1])
        self.d1_validate_list.append([1 ,2 ,1 ,3 ,2 ,2])
        self.d1_validate_list.append([1 ,2 ,1 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,1 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,1 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,1 ,2 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,1 ,2 ,2 ,3])
        self.d1_validate_list.append([1 ,2 ,2 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,2 ,2 ,3 ,2 ,1])
        self.d1_validate_list.append([1 ,2 ,2 ,3 ,2 ,2])
        self.d1_validate_list.append([1 ,2 ,2 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,2 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,2 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,2 ,2 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,2 ,2 ,2 ,3])
        self.d1_validate_list.append([1 ,2 ,3 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,2 ,3 ,3 ,2 ,1])
        self.d1_validate_list.append([1 ,2 ,3 ,3 ,2 ,2])
        self.d1_validate_list.append([1 ,2 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,3 ,3 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,3 ,3 ,2 ,1])
        self.d1_validate_list.append([1 ,3 ,3 ,3 ,2 ,2])
        self.d1_validate_list.append([1 ,3 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([1 ,3 ,3 ,2 ,1 ,3])
        self.d1_validate_list.append([1 ,3 ,3 ,2 ,2 ,1])
        self.d1_validate_list.append([1 ,3 ,3 ,2 ,2 ,2])
        self.d1_validate_list.append([1 ,3 ,3 ,2 ,2 ,3])
        self.d1_validate_list.append([2 ,2 ,1 ,3 ,2 ,1])
        self.d1_validate_list.append([2 ,2 ,1 ,3 ,2 ,2])
        self.d1_validate_list.append([2 ,2 ,1 ,3 ,2 ,3])
        self.d1_validate_list.append([2 ,2 ,2 ,3 ,2 ,1])
        self.d1_validate_list.append([2 ,2 ,2 ,3 ,2 ,2])
        self.d1_validate_list.append([2 ,2 ,2 ,3 ,2 ,3])
        self.d1_validate_list.append([2 ,2 ,3 ,3 ,2 ,1])
        self.d1_validate_list.append([2 ,2 ,3 ,3 ,2 ,2])
        self.d1_validate_list.append([2 ,2 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([2 ,3 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([2 ,3 ,3 ,2 ,2 ,3])
        self.d1_validate_list.append([3 ,2 ,1 ,3 ,2 ,1])
        self.d1_validate_list.append([3 ,2 ,1 ,3 ,2 ,2])
        self.d1_validate_list.append([3 ,2 ,1 ,3 ,2 ,3])
        self.d1_validate_list.append([3 ,3 ,1 ,3 ,2 ,1])
        self.d1_validate_list.append([3 ,3 ,1 ,2 ,2 ,1])
        self.d1_validate_list.append([3 ,2 ,2 ,3 ,2 ,1])
        self.d1_validate_list.append([3 ,2 ,2 ,3 ,2 ,2])
        self.d1_validate_list.append([3 ,2 ,2 ,3 ,2 ,3])
        self.d1_validate_list.append([3 ,2 ,3 ,3 ,2 ,1])
        self.d1_validate_list.append([3 ,2 ,3 ,3 ,2 ,2])
        self.d1_validate_list.append([3 ,2 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([3 ,3 ,3 ,3 ,2 ,3])
        self.d1_validate_list.append([3 ,3 ,3 ,2 ,2 ,3])

        self.d2_validate_list.append([1 ,2 ,1 ,3 ,2 ,1])
        self.d2_validate_list.append([1 ,3 ,1 ,2 ,2 ,3])
        self.d2_validate_list.append([1 ,3 ,2 ,2 ,2 ,3])
        self.d2_validate_list.append([1 ,2 ,3 ,3 ,1 ,3])
        self.d2_validate_list.append([1 ,2 ,3 ,3 ,2 ,3])
        self.d2_validate_list.append([1 ,3 ,3 ,3 ,1 ,3])
        self.d2_validate_list.append([1 ,3 ,3 ,3 ,2 ,3])
        self.d2_validate_list.append([1 ,3 ,3 ,2 ,1 ,3])
        self.d2_validate_list.append([1 ,3 ,3 ,2 ,2 ,3])
        self.d2_validate_list.append([2 ,2 ,1 ,3 ,2 ,1])
        self.d2_validate_list.append([2 ,2 ,3 ,3 ,2 ,3])
        self.d2_validate_list.append([3 ,2 ,1 ,3 ,1 ,1])
        self.d2_validate_list.append([3 ,2 ,1 ,3 ,2 ,1])
        self.d2_validate_list.append([3 ,3 ,1 ,3 ,1 ,1])
        self.d2_validate_list.append([3 ,3 ,1 ,3 ,2 ,1])
        self.d2_validate_list.append([3 ,3 ,1 ,2 ,1 ,1])
        self.d2_validate_list.append([3 ,3 ,1 ,2 ,2 ,1])
        self.d2_validate_list.append([3 ,3 ,2 ,2 ,2 ,1])
        self.d2_validate_list.append([3 ,2 ,3 ,3 ,2 ,3])
        self.d2_validate_list.append([3 ,3 ,3 ,2 ,2 ,1])

        self.d3_validate_list.append([1 ,3 ,1 ,3 ,2 ,3])
        self.d3_validate_list.append([1 ,3 ,1 ,2 ,1 ,3])
        self.d3_validate_list.append([1 ,3 ,1 ,2 ,2 ,3])
        self.d3_validate_list.append([1 ,2 ,3 ,3 ,2 ,1])
        self.d3_validate_list.append([1 ,3 ,3 ,3 ,2 ,1])
        self.d3_validate_list.append([1 ,3 ,3 ,2 ,2 ,1])
        self.d3_validate_list.append([3 ,2 ,1 ,3 ,2 ,1])
        self.d3_validate_list.append([3 ,3 ,1 ,3 ,2 ,1])
        self.d3_validate_list.append([3 ,3 ,1 ,2 ,2 ,1])
        self.d3_validate_list.append([3 ,2 ,3 ,3 ,1 ,3])
        self.d3_validate_list.append([3 ,2 ,3 ,3 ,2 ,3])
        self.d3_validate_list.append([3 ,3 ,3 ,3 ,1 ,3])
        self.d3_validate_list.append([3 ,3 ,3 ,3 ,2 ,3])
        self.d3_validate_list.append([3 ,3 ,3 ,2 ,1 ,3])
        self.d3_validate_list.append([3 ,3 ,3 ,2 ,2 ,3])

        self.d4_validate_list.append([1 ,2 ,1 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,2 ,1 ,3])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,3 ,1 ,3])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,1 ,3 ,3 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,2 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,3 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,3 ,3 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,2 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,3 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,2 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,1 ,2 ,3 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,2 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,2 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,2 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,2 ,2 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,2 ,2 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,2 ,1 ,1])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,3 ,1 ,1])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,3 ,2 ,1])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,2 ,3 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,2 ,1 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,3 ,1 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,3 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([1 ,3 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,2 ,1 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,3 ,1 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,1 ,1 ,3])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,1 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,2 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,3 ,2 ,1])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,1 ,2 ,2])
        self.d4_validate_list.append([1 ,3 ,3 ,2 ,1 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,1 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,2 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([2 ,2 ,3 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([2 ,3 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([2 ,3 ,3 ,2 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,2 ,1 ,1])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,3 ,1 ,1])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,3 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,1 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,1 ,3 ,2 ,1 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,3 ,3 ,1 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,3 ,3 ,2 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,2 ,2 ,1 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,2 ,3 ,1 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,2 ,1 ,2 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,2 ,2 ,2 ,1])
        self.d4_validate_list.append([3 ,3 ,1 ,2 ,3 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,2 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,2 ,1 ,3])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,3 ,1 ,3])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,1 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,2 ,2 ,1])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,1 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,2 ,2 ,2])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([3 ,2 ,3 ,3 ,3 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,3 ,2 ,1 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,3 ,3 ,1 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,3 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,3 ,2 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,3 ,3 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,2 ,2 ,1 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,2 ,3 ,1 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,2 ,1 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,2 ,2 ,2 ,3])
        self.d4_validate_list.append([3 ,3 ,3 ,2 ,3 ,2 ,3])


    # バリデーションを実行する
    def clean(self):
        logging.debug("clean")
        if len(self.errors) > 0: return
        cleaned_data = super().clean()

        drill_type = int(cleaned_data.get('drill_type'))
        left_minus_select = int(cleaned_data.get('left_minus_select'))
        left_input = int(cleaned_data.get('left_input'))
        right_minus_select = int(cleaned_data.get('right_minus_select'))
        right_input = int(cleaned_data.get('right_input'))
        mod_select = 0
        if drill_type == 4:
            try:
                mod_select = int(cleaned_data.get('mod_select'))
            except:
                mod_select = 1
        keta_fix_select = int(cleaned_data.get('keta_fix_select'))
        answer_minus_select = int(cleaned_data.get('answer_minus_select'))

        msg = '選択した組み合わせでは問題作成をすることができません。'
        if drill_type == 1:
            check_list = [left_minus_select,left_input,right_minus_select,right_input,keta_fix_select,answer_minus_select]
            if self.d1_validate_list.__contains__(check_list):
                raise forms.ValidationError(msg)
        elif drill_type == 2:
            check_list = [left_minus_select,left_input,right_minus_select,right_input,keta_fix_select,answer_minus_select]
            if self.d2_validate_list.__contains__(check_list):
                raise forms.ValidationError(msg)
        elif drill_type == 3:
            check_list = [left_minus_select,left_input,right_minus_select,right_input,keta_fix_select,answer_minus_select]
            if self.d3_validate_list.__contains__(check_list):
                raise forms.ValidationError(msg)
        elif drill_type == 4:
            check_list = [left_minus_select,left_input,right_minus_select,right_input,mod_select,keta_fix_select,answer_minus_select]
            if self.d4_validate_list.__contains__(check_list):
                raise forms.ValidationError(msg)

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
