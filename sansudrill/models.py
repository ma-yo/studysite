from django.db import models
import hashlib

# Create your models here.

class NgPattern(models.Model):
    hash_key = models.CharField(max_length=256, primary_key=True)
    drill_type = models.CharField(max_length=3)
    left_input = models.CharField(max_length=3)
    right_input = models.CharField(max_length=3)
    answer_select = models.CharField(max_length=3)
    keta_fix_flg = models.CharField(max_length=3)
    left_minus_flg = models.CharField(max_length=3)
    right_minus_flg = models.CharField(max_length=3)
    answer_minus_flg = models.CharField(max_length=3)
    mod_select = models.CharField(max_length=3)

    def get_hash(self):
        val = self.drill_type + self.left_input + self.right_input + self.answer_select \
            + self.keta_fix_flg + self.left_minus_flg + self.right_minus_flg \
            + self.answer_minus_flg + self.mod_select

        return hashlib.sha256(val.encode()).hexdigest()
    class Meta:
        db_table = 'ngpattern'
