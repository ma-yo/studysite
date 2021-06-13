import hashlib
from django.db import models

# Create your models here.

# NGパターン保持テーブル
class NgPattern(models.Model):
    hash_key = models.CharField(max_length=256, primary_key=True)
    drill_type = models.CharField(max_length=3)
    left_input = models.CharField(max_length=3)
    right_input = models.CharField(max_length=3)
    answer_select = models.CharField(max_length=3)
    keta_fix_left_flg = models.CharField(max_length=3)
    keta_fix_right_flg = models.CharField(max_length=3)
    left_minus_flg = models.CharField(max_length=3)
    right_minus_flg = models.CharField(max_length=3)
    answer_minus_flg = models.CharField(max_length=3)
    mod_select = models.CharField(max_length=3)
    create_date = models.DateField(auto_now_add=True)
    # SHA256を用いてハッシュ値を生成する
    def get_hash(self):
        val = self.drill_type + self.left_input + self.right_input + self.answer_select \
            + self.keta_fix_left_flg + self.keta_fix_right_flg + self.left_minus_flg + self.right_minus_flg \
            + self.answer_minus_flg + self.mod_select

        return hashlib.sha256(val.encode()).hexdigest()
    class Meta:
        db_table = 'ngpattern'
