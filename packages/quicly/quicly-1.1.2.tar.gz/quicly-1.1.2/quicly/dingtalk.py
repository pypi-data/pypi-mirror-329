import requests


class DingRobot(object):
    def __init__(self, access_token):
        self._access_token = access_token
        self._webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(access_token)

    @property
    def access_token(self):
        return self._access_token

    @property
    def webhook_url(self):
        return self._webhook_url

    def send_message(self, data):
        assert isinstance(data, dict)
        requests.post(self._webhook_url, json=data, headers={
            'Content-Type': 'application/json',
        })


class DingMessageBuilder(object):
    def build(self):
        raise NotImplementedError()


class DingTextMessageBuilder(DingMessageBuilder):
    def __init__(self):
        self._text = []
        self._at_mobiles = []
        self._is_at_all = False

    def at(self, mobile):
        if isinstance(mobile, str):
            self._at_mobiles.append(mobile)
        elif isinstance(mobile, (list, tuple, set)):
            self._at_mobiles.append(x for x in mobile if isinstance(x, str))
        return self

    def at_all(self, is_at_all=True):
        self._is_at_all = is_at_all
        return self

    def set_text(self, text):
        self._text = [text]
        return self

    def clear_text(self):
        self._text = []
        return self

    def append_text(self, text):
        self._text.append(text)
        return self

    def append_at(self, mobile):
        self._text.append(u'@{}'.format(mobile))
        return self

    def append_newline(self):
        self._text.append(u'\n')
        return self

    def build(self):
        msg = {
            'msgtype': 'text',
            'text': {
                'content': ''.join(self._text),
            },
            'at': {
                'atMobiles': self._at_mobiles,
                'isAtAll': self._is_at_all,
            },
        }
        return msg


class DingLinkMessageBuilder(DingMessageBuilder):
    def __init__(self):
        self._title = u''
        self._text = u''
        self._url = None
        self._image_url = None

    def set_title(self, title):
        self._title = title
        return self

    def set_text(self, text):
        self._text = text
        return self

    def set_url(self, url):
        self._url = url
        return self

    def set_image_url(self, image_url):
        self._image_url = image_url
        return self

    def build(self):
        msg = {
            'msgtype': 'link',
            'link': {
                'title': self._title,
                'text': self._text,
                'messageUrl': self._url,
                'picUrl': self._image_url,
            },
        }
        return msg


class _DingMarkdownMessageBuilderBase(DingMessageBuilder):
    def __init__(self):
        self._text = []

    def set_text(self, text):
        self._text = [text]
        return self

    def clear_text(self):
        self._text = []
        return self

    def append_text(self, text):
        if isinstance(text, str) and len(text):
            self._text.append(text)
        return self

    def append_newline(self):
        self._text.append('\n')

    def ensure_newline(self):
        is_newline = False
        if len(self._text) == 0:
            is_newline = True
        elif self._text[-1].endswith('\n'):
            is_newline = True
        if not is_newline:
            self.append_newline()

    def append_h1(self, title):
        self.ensure_newline()
        self._text.append('# {}'.format(title))
        self.append_newline()
        return self

    def append_h2(self, title):
        self.ensure_newline()
        self._text.append('## {}'.format(title))
        self.append_newline()
        return self

    def append_h3(self, title):
        self.ensure_newline()
        self._text.append('### {}'.format(title))
        self.append_newline()
        return self

    def append_h4(self, title):
        self.ensure_newline()
        self._text.append('#### {}'.format(title))
        self.append_newline()
        return self

    def append_h5(self, title):
        self.ensure_newline()
        self._text.append('##### {}'.format(title))
        self.append_newline()
        return self

    def append_h6(self, title):
        self.ensure_newline()
        self._text.append('###### {}'.format(title))
        self.append_newline()
        return self

    def append_ref(self, text):
        self.ensure_newline()
        self._text.append('> {}'.format(text))
        self.append_newline()
        return self

    def append_bold(self, text):
        self._text.append('**{}**'.format(text))
        return self

    def append_italic(self, text):
        self._text.append('*{}*'.format(text))
        return self

    def append_link(self, title, url):
        if not (isinstance(title, str) and len(title)):
            title = url
        self._text.append('[{}]({})'.format(title, url))
        return self

    def append_image(self, title, url):
        if not isinstance(title, str):
            title = ''
        self._text.append('![{}]()'.format(title, url))
        return self

    def append_unordered_list(self, items):
        assert isinstance(items, (list, tuple, set))
        self.ensure_newline()
        for item in items:
            self._text.append('- {}'.format(item))
            self.append_newline()
        return self

    def append_ordered_list(self, items):
        assert isinstance(items, (list, tuple, set))
        self.ensure_newline()
        for i in range(len(items)):
            item = items[i]
            self._text.append('{}. {}'.format(i, item))
            self.append_newline()
        return self


class DingMarkdownMessageBuilder(_DingMarkdownMessageBuilderBase):
    def __init__(self):
        self._title = u''
        self._at_mobiles = []
        self._is_at_all = False
        super(DingMarkdownMessageBuilder, self).__init__()

    def at(self, mobile):
        if isinstance(mobile, str):
            self._at_mobiles.append(mobile)
        elif isinstance(mobile, (list, tuple, set)):
            self._at_mobiles.append(x for x in mobile if isinstance(x, str))
        return self

    def at_all(self, is_at_all=True):
        self._is_at_all = is_at_all
        return self

    def set_title(self, title):
        self._title = title
        return self

    def build(self):
        msg = {
            'msgtype': 'markdown',
            'markdown': {
                'title': self._title,
                'text': u''.join(self._text),
            },
            'at': {
                'atMobiles': self._at_mobiles,
                'isAtAll': self._is_at_all,
            },
        }
        return msg


class DingActionCardMessageBuilder(_DingMarkdownMessageBuilderBase):
    def __init__(self):
        self._title = u''
        self._single_title = None
        self._single_url = None
        self._btns = None
        self._btn_orientation = 0
        self._hide_avatar = False
        super(DingActionCardMessageBuilder, self).__init__()

    def set_title(self, title):
        self._title = title
        return self

    def set_single_btn(self, title, url):
        self._single_title = title
        self._single_url = url
        self._btns = None
        return self

    def append_button(self, title, url):
        self._single_title = None
        self._single_url = None
        self._btns = self._btns if isinstance(self._btns, list) else []
        self._btns.append({
            'title': title,
            'actionURL': url,
        })
        return self

    def set_btn_orientation_vertical(self):
        self._btn_orientation = 1
        return self._btn_orientation

    def set_btn_orientation_horizontal(self):
        self._btn_orientation = 0
        return self._btn_orientation

    def hide_avatar(self, hide=True):
        self._hide_avatar = hide
        return self

    def build(self):
        action_card = {
            'title': self._title,
            'text': u''.join(self._text),
            'btnOrientation': self._btn_orientation,
            'hideAvatar': self._hide_avatar,
        }
        if isinstance(self._btns, list) and len(self._btns):
            action_card['btns'] = self._btns
        else:
            action_card['singleTitle'] = self._single_title
            action_card['singleURL'] = self._single_url

        msg = {
            'msgtype': 'actionCard',
            'actionCard': action_card,
        }
        return msg


class DingFeedCardMessageBuilder(DingMessageBuilder):
    def __init__(self):
        self._links = []

    def append_link(self, title, url, image_url):
        self._links.append({
            'title': title,
            'messageURL': url,
            'picURL': image_url,
        })
        return self

    def build(self):
        msg = {
            'msgtype': 'feedCard',
            'feedCard': {
                'links': self._links[:10],
            },
        }
        return msg
