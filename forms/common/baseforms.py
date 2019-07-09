# !/usr/bin/env python
# coding: utf-8

from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_error(self):
        _, value = self.errors.popitem()
        message = value[0]
        return message
