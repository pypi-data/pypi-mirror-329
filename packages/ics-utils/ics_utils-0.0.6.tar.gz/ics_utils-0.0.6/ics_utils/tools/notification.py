# -*- coding: utf-8 -*-
"""
@author: hanyanling
@date: 2024/12/19 15:35
@email:
---------
@summary:
"""
import base64
import hashlib
import io
import os.path

import requests


class WxWork:
    """
    企微机器人消息通知
    https://developer.work.weixin.qq.com/document/path/91770
    """
    def __init__(self, bot_key):
        if not bot_key:
            raise ValueError('bot_key 不能为空')

        self.bot_key = bot_key
        self.bot_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot_key}'
        self.upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?type=file&key={bot_key}'

    def __send_req(self, data):
        """
        发送HTTP POST请求到企业微信机器人接口。

        :param data: 要发送的JSON数据，包含消息类型和内容。
        :type data: dict
        :return: 企业微信API返回的响应，通常是一个包含状态码和信息的字典。
        :rtype: dict
        """
        return requests.post(url=self.bot_url, json=data).json()

    def send_msg(self, msg_type, msg: str = None,
                 mentioned_list=None, mentioned_mobile_list=None, at_all=False,
                 file_path: str = None, file_content: bytes = None, show_name: str = None):
        """
        使用企业微信机器人发送消息。

        :param msg_type: 要发送的消息类型。支持的类型有 'text', 'markdown', 'image', 'file', 和 'voice'。
        :type msg_type: str
        :param msg: 消息的内容。对于 'text' 和 'markdown' 类型的消息是必需的。
        :type msg: str, 可选
        :param mentioned_list: 在消息中提及的用户ID列表。仅适用于 'text' 和 'markdown' 类型。
        :type mentioned_list: list, 可选
        :param mentioned_mobile_list: 在消息中提及的手机号列表。仅适用于 'text' 和 'markdown' 类型。
        :type mentioned_mobile_list: list, 可选
        :param at_all: 是否提及所有用户。仅适用于 'text' 和 'markdown' 类型。
        :type at_all: bool, 可选
        :param file_path: 要发送的文件路径。适用于 'image', 'file', 和 'voice' 类型。
        :type file_path: str, 可选
        :param file_content: 要发送的文件内容。适用于 'image', 'file', 和 'voice' 类型。
        :type file_content: bytes, 可选
        :param show_name: 文件显示名称。适用于 'file' 和 'voice' 类型。
        :type show_name: str, 可选
        :return: 从企业微信API返回的响应。
        :rtype: dict
        """
        support_type = {
            'text',
            'markdown',
            'image',
            # 'news',
            'file',
            'voice',
            # 'template_card'
        }

        if msg_type not in support_type:
            raise ValueError(f"未知的消息类型，当前输入类型：{msg_type}, 支持的类型：{support_type}")

        if mentioned_list is None:
            mentioned_list = []
        if mentioned_mobile_list is None:
            mentioned_mobile_list = []
        if at_all:
            mentioned_mobile_list.append('@all')

        if msg_type in {'text', 'markdown'}:
            data = {
                'msgtype': msg_type,
                msg_type: {
                    'content': msg,
                    'mentioned_list': mentioned_list,
                    'mentioned_mobile_list': mentioned_mobile_list
                }
            }
            return self.__send_req(data)

        elif msg_type == 'image':
            # 以文件路径为准
            if file_path:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f'找不到图片：{file_path}')
                file_content = open(file_path, 'rb').read()
            img_md5 = hashlib.md5(file_content).hexdigest()
            img_base64 = base64.b64encode(file_content).decode('utf-8')
            data = {
                "msgtype": "image",
                "image": {
                    "base64": img_base64,
                    "md5": img_md5
                }
            }
            return self.__send_req(data)

        elif msg_type in {'file', 'voice'}:
            if file_path:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f'找不到文件：{file_path}')
                file_content = open(file_path, 'rb').read()

                if show_name is None:
                    show_name = os.path.basename(file_path)

            response = requests.post(
                self.upload_url,
                files={
                    'file': (show_name, io.BytesIO(file_content))
                }
            )

            upload_response = response.json()
            if upload_response['errcode'] != 0:
                return upload_response
            else:
                media_id = upload_response.get('media_id')
                data = {'msgtype': msg_type, msg_type: {'media_id': media_id}}
                return self.__send_req(data)


    def send_text_msg(self, msg, mentioned_list=None, mentioned_mobile_list=None, at_all=False):
        """
        使用企业微信机器人发送文本消息。

        :param msg: 要发送的文本消息内容。
        :type msg: str
        :param mentioned_list: 要在消息中提及的用户ID列表。
        :type mentioned_list: list 或 None
        :param mentioned_mobile_list: 要在消息中提及的手机号列表。
        :type mentioned_mobile_list: list 或 None
        :param at_all: 如果为 True，则在群组中提及所有用户。
        :type at_all: bool
        :return: 发送消息后从企业微信API返回的响应。
        :rtype: dict
        """
        return self.send_msg('text', msg=msg, mentioned_list=mentioned_list,
                             mentioned_mobile_list=mentioned_mobile_list, at_all=at_all)


    def send_markdown_msg(self, msg):
        """
        使用企业微信机器人发送Markdown消息。

        该函数利用企业微信机器人发送格式化为Markdown的消息。

        :param msg: 要发送的Markdown内容。
        :type msg: str
        :return: 发送消息后从企业微信API返回的响应。
        :rtype: dict
        """
        return self.send_msg('markdown', msg=msg)

    def send_image_msg(self, file_path=None, file_content=None):
        """
        使用企业微信机器人发送图片消息。

        该函数允许通过指定文件路径或文件内容来发送图片消息。

        :param file_path: 要发送的图片文件路径。如果提供，将使用此路径读取图片内容。
        :type file_path: str, 可选
        :param file_content: 图片文件的字节内容。如果图片内容已在内存中可用，可以使用此参数。
        :type file_content: bytes, 可选
        :return: 发送图片消息后从企业微信API返回的响应。
        :rtype: dict
        """
        return self.send_msg('image', file_path=file_path, file_content=file_content)


    def send_file_msg(self, file_path=None, file_content=None, show_name=None):
        """
        使用企业微信机器人发送文件消息。

        该函数允许通过指定文件路径或文件内容来发送文件消息，并可以指定文件的显示名称。

        :param file_path: 要发送的文件路径。如果提供，将使用此路径读取文件内容。
        :type file_path: str, 可选
        :param file_content: 文件的字节内容。如果文件内容已在内存中可用，可以使用此参数。
        :type file_content: bytes, 可选
        :param show_name: 文件的显示名称。适用于在消息中显示的文件名。
        :type show_name: str, 可选
        :return: 发送文件消息后从企业微信API返回的响应。
        :rtype: dict
        """
        return self.send_msg('file', file_path=file_path, file_content=file_content, show_name=show_name)

    def send_voice_msg(self, file_path=None, file_content=None, show_name=None):
        """
        使用企业微信机器人发送语音消息。

        该函数允许通过指定文件路径或文件内容来发送语音消息，并可以指定语音文件的显示名称。

        :param file_path: 要发送的语音文件路径。如果提供，将使用此路径读取文件内容。
        :type file_path: str, 可选
        :param file_content: 语音文件的字节内容。如果文件内容已在内存中可用，可以使用此参数。
        :type file_content: bytes, 可选
        :param show_name: 语音文件的显示名称。适用于在消息中显示的文件名。
        :type show_name: str, 可选
        :return: 发送语音消息后从企业微信API返回的响应。
        :rtype: dict
        """
        return self.send_msg('voice', file_path=file_path, file_content=file_content, show_name=show_name)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password, receiver_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def send_email(self, subject, body, attachments=None):
        """
        发送邮件

        :param subject: 邮件主题
        :param body: 邮件正文
        :param attachments: 附件列表，每个元素是一个元组 (文件名, 文件内容)
        :return: 成功返回True，失败返回False
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        # 添加邮件正文
        msg.attach(MIMEText(body, 'plain'))

        # 添加附件
        if attachments:
            for filename, file_content in attachments:
                part = MIMEApplication(file_content)
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # 启用TLS加密
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"发送邮件时出错: {e}")
            return False

    def send_simple_email(self, subject, body):
        """
        发送简单的纯文本邮件

        :param subject: 邮件主题
        :param body: 邮件正文
        :return: 成功返回True，失败返回False
        """
        return self.send_email(subject, body)

