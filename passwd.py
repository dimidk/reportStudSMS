#!/usr/bin/python
#-*-coding: utf-8 -*-

import os

"""urlsms="https://easysms.gr/api/sms/bulk?key=72416f5e5edecd"""
"""έλεγχος αν υπάρχει συγκεκριμένη σειρά όπου γράφονται στο url τα tags"""

urlsms="https://easysms.gr/api/sms/send?key=72416f5e5edecd"

urlbalance="https://easysms.gr/api/me/balance?key=72416f5e5edecd"
urlcheckSent="https://easysms.gr/api/history/single/list?key=72416f5e5edecd"

"""try to use regular expressions for subject in email"""
username="dimi.epalefimeries"
password="epalEfimeries"

"""targets=['garwas74@gmail.com ','charitakis.ioannis@gmail.com','chairetaki@gmail.com','glemon1@gmail.com','plastara_katerina@yahoo.gr','dekadimi@gmail.com']"""

targets=['dekadimi@gmail.com','dekadimi.epal@gmail.com']


"""https://easysms.gr/api/sms/send?\
key=72416f5e5edecd&\
text=your_message&\
from=sender&\
to=306971000000&\
type=xml"""




