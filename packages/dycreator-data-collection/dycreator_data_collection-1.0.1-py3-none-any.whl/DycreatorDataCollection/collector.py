"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-02-22
Author: Martian Bugs
Description: 数据采集器
"""

from DrissionPage import Chromium, ChromiumOptions

from .content.content import Content
from .data.data import Data


class Collector:
    """采集器. 使用之前请先调用 `connect_browser` 方法连接浏览器."""

    def __init__(self):
        self._content = None
        self._data = None

    def connect_browser(self, port: int):
        """
        连接浏览器

        Args:
            port: 浏览器调试端口号
        """

        chrome_options = ChromiumOptions(read_file=False)
        chrome_options.set_local_port(port=port)

        self.browser = Chromium(addr_or_opts=chrome_options)

    @property
    def content(self):
        """内容管理模块数据采集"""

        if self._content is None:
            self._content = Content(self.browser)

        return self._content

    @property
    def data(self):
        """数据管理模块数据采集"""

        if self._data is None:
            self._data = Data(self.browser)

        return self._data
