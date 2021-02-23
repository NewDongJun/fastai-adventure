from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from .models import User
from datetime import datetime
import time

from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from django.views.generic import View
from .models import User, Stock, Bookmark
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import plotly
from functools import wraps
import plotly.express as px
import plotly.graph_objs as go
import datetime
from .utils import get_plot,get_bar_graph
from django.core.paginator import Paginator
from PIL import Image
import os
import numpy as np
from django.contrib.auth import login as login_a 
# ,authenticaste

from .prediction import predict, getLabels

from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage



class EmailThread(threading.Thread):
    def __init__(self):
        # self.email = email
        threading.Thread.__init__(self)

    def run (self):


        while(1): 
            
            alarm_users=User.objects.exclude(mail_alarm_time_hour=None)
            print("유저수" , len(alarm_users))

            time.sleep(2)

            for user in alarm_users :

                bookmarks = Bookmark.objects.filter(user__email=user.email) 
                print(bookmarks)

                now = datetime.datetime.now()

                print(user.username)
                print(user.mail_alarm_time_hour,"시")
                print(user.mail_alarm_time_minute,"분")

                time.sleep(2)

                if now.hour == user.mail_alarm_time_hour and now.minute == user.mail_alarm_time_minute :

                    # if sleep[index] == 0 :

                    title = "🔔 "+user.username + ". Bookmark Prediction Mail has arrived from FASTOCK!"
                

                    html_content = render_to_string('stock/mail_template.html', context ={'bookmarks':bookmarks, 'user':user}) # render with dynamic value
                    text_content = strip_tags(html_content)
                    
                    # create the email, and attach the HTML version as well.
                    
                    msg = EmailMultiAlternatives(title, text_content,  to=[user.email])
                    msg.mixed_subtype = 'related'
                    msg.attach_alternative(html_content, "text/html")

                    img_dir = 'stock/templates/static/logo/'
                    image = 'for_mail.PNG'
                    file_path = os.path.join(img_dir, image)
                    with open(file_path, 'rb' ) as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', '<{name}>'.format(name=image))
                        img.add_header('Content-Disposition', 'inline', filename=image)
                    msg.attach(img)

                    msg.send(fail_silently=False)
                    print('스레드 한 개 작업 완료')

                    # time.sleep(55)
                    # sleep[index]=1
                    
                    # else :
                    #     print("이미 메일을 보냈어요!")   아니 왜 안댐 ;;
                    #     pass
                    
                    # print('시작 - time sleep 50 초 기다림')
                    # start = time.time()
                    # time.sleep(50)
                    # end = time.time()
                    # print('종료 시간 측정 결과 :', end - start)
                    # pass


            else :
                pass
                # print(now.hour)
                # print(now.minute)
                # time.sleep(1)
                
            # time.sleep(1)



#이렇게 하면 views.py 에 임포트 될때 딱 한번 실행 됨 
#views.py에서는 이거 실행하기 위해 임포트 하는거고 views.py 안에서 이 클래스를 사용할 일은 없고 사용 하려면 디자인을 바꿔야함 
# def send_email(subject, body, to_email): 


# 알람 성정한 user 객체 수 만큼  for문 돌리기 
# alarm_users=User.objects.exclude(mail_alarm_time_hour=None)
# print(alarm_users)

# for alarm_user in alarm_users :
#     EmailThread(alarm_user.email,alarm_user.username).start()  #start()가 run메서드를 호출함

EmailThread().start()  #start()가 run메서드를 호출함