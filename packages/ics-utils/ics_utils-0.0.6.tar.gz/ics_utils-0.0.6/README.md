

# ics_utils
爬虫工具包

## 安装
```shell
pip install ics-utils
```

## 使用
### 发送企微消息通知

```python
from ics_utils import WxWork

work = WxWork(bot_key='')
work.send_text_msg('hello')
work.send_markdown_msg('# 标题 \n ## 小标题')

# 发送图片,二选一
work.send_image_msg(file_path='')
work.send_image_msg(file_content=b'')

# 发送文件或者音频，三选一
work.send_voice_msg(file_path='')
work.send_voice_msg(file_path='', show_name='')
work.send_voice_msg(file_content=b'', show_name='')

work.send_file_msg(file_path='')
work.send_file_msg(file_path='', show_name='')
work.send_file_msg(file_content=b'', show_name='')
```


[修订记录](docs/修订记录.md)