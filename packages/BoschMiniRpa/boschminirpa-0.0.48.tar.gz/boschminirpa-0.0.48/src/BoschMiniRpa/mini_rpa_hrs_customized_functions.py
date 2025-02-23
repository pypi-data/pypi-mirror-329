import datetime
import os
import traceback
from calendar import monthrange
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from pathlib import Path
from typing import Union
from threading import Thread

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib

from BoschRpaMagicBox.smb_functions import *

from mini_rpa_core import MiniRPACore


def copy_as_new_file(from_folder_path: str, from_file_name: str, update_folder_path: str, update_file_name: str, from_period: str, user_name: str, user_password: str,
                     server_name: str, share_name: str, port: int):
    """This function is used to copy files from from_folder or sub_folder to update folder

    Args:

        from_folder_path: This is the from_folder_path
        from_file_name: This is the file name that contains common file name fragment
        update_folder_path: This is the target folder path
        update_file_name: This is the file name of update file
        from_period(str): This is the start period
        user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
    """
    from_file_extension = Path(from_file_name).suffix
    save_update_file_name = f"{update_file_name}{from_period}.{from_file_extension}"

    from_file_path = from_folder_path + os.sep + from_file_name
    update_file_path = update_folder_path + os.sep + save_update_file_name

    is_from_file_exist, from_file_obj = smb_check_file_exist(user_name, user_password, server_name, share_name, from_file_path, port)

    if is_from_file_exist:
        smb_store_remote_file_by_obj(user_name, user_password, server_name, share_name, update_file_path, from_file_obj, port)
        print(f'--------------- copy file for {from_file_path} to {update_file_path}---------------')
    else:
        print('Target file is not found！')


def hrs_calculate_duration(hrs_time_data: Union[pd.DataFrame, None], from_column_name: str, from_period: str, new_column_name: str, ) -> pd.DataFrame:
    """This function is used to calculate time difference between values of from column and today

    Args:
        hrs_time_data(pd.DataFrame): This is the hrs time related data
        from_column_name:This is the column name
        from_period(str): This is the start period
        new_column_name: This is the new column that will record compare result
    """
    hrs_time_data[from_column_name].fillna('', inplace=True)
    hrs_time_data[from_column_name] = hrs_time_data[from_column_name].apply(MiniRPACore.prepare_date_info)
    # hrs_time_data[from_column_name] = hrs_time_data[from_column_name].astype(str)
    # hrs_time_data[from_column_name] = hrs_time_data[from_column_name].str.strip().str.split(' ', expand=True)[0]
    # hrs_time_data[from_column_name] = (pd.to_datetime(hrs_time_data[from_column_name], errors='coerce')).dt.date
    for row_index in hrs_time_data.index:
        row_data = hrs_time_data.loc[row_index]
        previous_date = row_data[from_column_name]
        if not pd.isna(previous_date) and previous_date:
            if from_period:
                # current_date = datetime.datetime.strptime(f'{from_period[:4]}-{from_period[4:6]}-{from_period[6:8]}', '%Y-%m-%d').date()
                current_date = MiniRPACore.prepare_date_info(from_period)
            else:
                current_date = datetime.datetime.now().date()
            day_duration = (current_date - previous_date).days
            year_duration = current_date.year - previous_date.year
            hrs_time_data.loc[row_index, new_column_name] = f'{day_duration} days'
            if previous_date.month == current_date.month:
                if previous_date.day == current_date.day and year_duration > 0:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                elif previous_date.month == 2 and previous_date.day == 29 and monthrange(current_date.year, current_date.month)[1] == 28 and current_date.day == 28:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                else:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
            else:
                hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
        else:
            hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
    return hrs_time_data


IMAGE_SIZE_DICT = {
    1: (420, 530),
    2: (1750, 180),
    3: (360, 437),
    4: (1430, 215),
    5: (1855, 338),
    6: (1733, 163),
    7: (385, 345),
    8: (800, 426),
    9: (1630, 257),
    10: (1630, 195),
    11: (1745, 257),
    12: (1890, 143),
    13: (395, 425),
    14: (368, 487),
    15: (1810, 116),
}


def read_image_from_bytesio(user_name, user_password, server_name, share_name, image_file_path, port):
    """ Read image from BytesIO

    Args:
        user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        image_file_path(str): This is the file path of image
        port(int): This is the port number of the server name
    """
    byte_data = smb_load_file_obj(user_name, user_password, server_name, share_name, image_file_path, port)
    byte_array = np.frombuffer(byte_data.getvalue(), np.uint8)
    image = cv2.imdecode(byte_array, cv2.IMREAD_COLOR)
    return image


def hrs_generate_email_content(service_year, user_name, user_name_en, manager_name, manager_name_en, seq_id, template_folder_path,
                               smb_user_name, user_password, server_name, share_name, port):
    """ Initialization parameters

    Args:
        service_year(str): This is the server year value
        user_name(str): This is the username
        user_name_en(str): This is the username in English
        manager_name(str): This is the manager name
        manager_name_en(str): This is the manager name in English
        seq_id(int): This is the sequence id
        template_folder_path(str): This is the template folder path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name

    """
    try:
        new_img_prename = f'add_text_{seq_id}'
        new_img_fullname = os.path.join(template_folder_path, f'add_text_{seq_id}.png')
        card_path_old = template_folder_path + os.sep + 'Card Template' + os.sep + f'{service_year}-Anniversary.png'

        # only available for mount option, or it will violate EULA license
        font_path = "/usr/share/fonts/simsun/simsun.ttc"
        font = ImageFont.truetype(font_path, 69)

        byte_io = BytesIO()
        service_year = int(service_year)
        if service_year <= 15:
            # bk_img = cv2.imread(card_path_old)
            bk_img = read_image_from_bytesio(smb_user_name, user_password, server_name, share_name, card_path_old, port)
            img_pil = Image.fromarray(bk_img)
            draw = ImageDraw.Draw(img_pil)
            image_size = IMAGE_SIZE_DICT[service_year]
            draw.text(image_size, user_name, font=font, fill=(0, 0, 0))
            bk_img = np.array(img_pil)
            # cv2.imwrite(new_img_fullname, bk_img)

            success, encoded_image = cv2.imencode('.png', bk_img)
            if success:
                byte_io.write(encoded_image.tobytes())
                byte_io.seek(0)

            smb_store_remote_file_by_obj(smb_user_name, user_password, server_name, share_name, new_img_fullname, byte_io, port)
            email_content = f'''
                            <body>                                                     
                            <p><img src=cid:{new_img_prename} alt=newimg_prename></p>
                            </body>
                            '''
        else:
            # For employees with more than 15 years of service, send it to the manager first for review and modifications before it is distributed to the staff.
            email_content = f'''
                            <body>           
                            <p>Dear {manager_name_en}：</p>                     
                            <p>亲爱的{manager_name}：</p>
                            <p>Your employee {user_name_en} has been working at Bosch for {service_year} years.</p>
                            <p>您的员工{user_name}工作年限已经满{service_year}年。</p>
                            <p>Please send an email to congratulate him/her~</p>
                            <p>请发个邮件祝福下吧~</p>
                            </body>
                            '''

        return {'is_successful': True, 'email_content': email_content, 'image_bytes': byte_io}
    except:
        return {'is_successful': False, 'email_content': traceback.format_exc()}


def hrs_send_html_content_email(mail_host, mail_user, mail_pass, email_to, email_cc, email_header, email_subject, service_year, user_name,
                                user_name_en, manager_name, manager_name_en, sender, seq_id, template_folder_path, smb_user_name, user_password, server_name, share_name, port):
    """ Send email with html content

    Args:
        mail_host (str): The SMTP server address for sending emails.
        mail_user (str): The username for authenticating with the SMTP server.
        mail_pass (str): The password or authentication token for the SMTP server.
        email_to (list): The primary recipient(s) of the email.
        email_cc (list): The carbon copy (CC) recipient(s) of the email.
        email_header (str): The header or display name to use for the email.
        email_subject (str): The subject line of the email.
        service_year (str): The service year for which the email is being generated (e.g., employee milestone year).
        user_name (str): The full name of the user (in the local language) being addressed in the email.
        user_name_en (str): The full name of the user in English.
        manager_name (str): The full name of the manager (in the local language) for reference in the email.
        manager_name_en (str): The full name of the manager in English.
        sender (str): The email address of the sender.
        seq_id (int): A unique identifier for the email sequence, used for tracking or logging.
        template_folder_path(str): This is the template folder path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name

    """
    try:
        smtp_obj = smtplib.SMTP(mail_host, 25)
        # connect to server
        smtp_obj.starttls()
        # login in server
        smtp_obj.login(mail_user, mail_pass)

        to_receivers = ','.join(email_to)
        cc_receivers = ','.join(email_cc)

        # set email content
        message = MIMEMultipart()
        message['From'] = Header(email_header, 'utf-8')
        message['To'] = to_receivers
        message['Cc'] = cc_receivers
        message['Subject'] = email_subject

        email_content_template_data = hrs_generate_email_content(service_year, user_name, user_name_en, manager_name, manager_name_en, seq_id, template_folder_path, smb_user_name,
                                                                 user_password, server_name, share_name, port)
        if email_content_template_data['is_successful']:
            content = MIMEText(email_content_template_data['email_content'], 'html', 'utf-8')
            # msg = MIMEMultipart('related')
            message.attach(content)
            if int(service_year) <= 15:
                img_prename = f'add_text_{seq_id}'
                img_fullname = os.path.join(template_folder_path, f'add_text_{seq_id}.png')
                # load image
                # fp = open(img_fullname, 'rb')
                # fp.close()
                msg_image_bytes = email_content_template_data['image_bytes']
                msg_image = MIMEImage(msg_image_bytes.getvalue())

                # set image id as img_prename
                msg_image.add_header('Content-ID', img_prename)
                message.attach(msg_image)

            # send
            smtp_obj.sendmail(from_addr=sender, to_addrs=email_to + email_cc, msg=message.as_string())

            # quit
            smtp_obj.quit()
            print(print(f'-----email is sent successfully to {email_to[0]}!-----'))
        else:
            print(f'Email template was generated failed,please check from the log file!')
            print(f"{user_name}-{service_year}: Failed to generate email template!\n{email_content_template_data['email_content']}")
    except:
        print(f'Failed send email to {email_to[0]}')
        print(traceback.format_exc())


def hrs_send_anniversary_email(email_to_manager_column, manager_name_column, anniversary_year_column, email_to_column, user_name_column, email_cc, email_subject, email_header,
                               email_account, email_password, email_address, anniversary_file_path, template_folder_path, smb_user_name, user_password, server_name, share_name,
                               port):
    """ Send anniversary email

    Args:
        email_to_manager_column(str): This is the email to manager column name
        manager_name_column(str): This is the manager name column name
        anniversary_year_column(str): This is the anniversary year column name
        email_to_column(str): This is the email to column name
        user_name_column(str): This is the username column name
        email_cc(list): This is the email cc list
        email_subject(str): This is the email subject
        email_header(str): This is the email header
        email_account(str): This is the email account
        email_password(str): This is the email password
        email_address(str): This is the email address
        anniversary_file_path(str): This is the file path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
        template_folder_path(str): This is the template folder path
    """
    mail_host = 'rb-smtp-int.bosch.com'
    mail_user = f'APAC\\{email_account}'
    mail_pass = f'{email_password}'
    sender = email_address

    file_obj = smb_load_file_obj(smb_user_name, user_password, server_name, share_name, anniversary_file_path, port)

    anniversary_data = pd.read_excel(file_obj, dtype={email_to_column: str, email_to_manager_column: str, user_name_column: str, manager_name_column: str,
                                                      anniversary_year_column: str})
    anniversary_data.fillna('', inplace=True)
    for column in [email_to_column, email_to_manager_column, user_name_column, manager_name_column, anniversary_year_column]:
        anniversary_data[column] = anniversary_data[column].str.strip()

    for row_index in anniversary_data.index:
        row_data = anniversary_data.loc[row_index]
        # email_to is set to [row_data[email_to_column]] if row_data[email_to_column] is not empty; otherwise, use email_cc
        if int(row_data[anniversary_year_column]) <= 15 and row_data[email_to_column] != '':
            # For service years 15 or less, send to the employee
            # The expression below assigns a string or a list. Without [] it would be a string; with [], it is a list.
            email_to = [row_data[email_to_column]]
        elif int(row_data[anniversary_year_column]) >= 16 and row_data[email_to_manager_column] != '':
            # For service years 16 or more, send to the manager
            email_to = [row_data[email_to_manager_column]]
        else:
            # If neither the manager nor the employee has an email, send to CC
            email_to = email_cc

        if email_to:
            # Log in and send the email. Handle both Chinese and English names.
            service_year, user_name, manager_name, seq_id = row_data[anniversary_year_column], row_data[user_name_column].split('/')[0], \
                row_data[manager_name_column].split('/')[0], row_index

            if '/' in row_data[user_name_column]:
                user_name_en = row_data[user_name_column].split('/')[1]
            else:
                user_name_en = row_data[user_name_column].split('/')[0]

            if '/' in row_data[manager_name_column]:
                manager_name_en = row_data[manager_name_column].split('/')[1]
            else:
                manager_name_en = row_data[manager_name_column].split('/')[0]

            thr = Thread(target=hrs_send_html_content_email,
                         args=[mail_host, mail_user, mail_pass, email_to, email_cc, email_header, email_subject, service_year, user_name,
                               user_name_en, manager_name, manager_name_en, sender, seq_id, template_folder_path, smb_user_name, user_password, server_name, share_name, port])
            thr.start()
