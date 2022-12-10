# coding: UTF-8
import sys
import os
from utils import driver
from utils import line_bot
import parser

text = driver.get_monthly_bills()
line_bot.push_text(text)