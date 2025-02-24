# -*- coding: utf-8 -*-
# @time: 2024/2/18 9:39
# @author: Dyz
# @file: base_spider.py
# @software: PyCharm
import asyncio
import logging
from pathlib import Path

import httpx
from requests import Session
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_fixed

from du_aio_tools.exceptions import HTTPError
from du_aio_tools.time import timer

logger = logging.getLogger("du_aio_tools.BaseSpider")

MAX_RETRY = 3  # 最大重试次数
WAIT_FIXED = 3  # 重试间隔 3s
TIMEOUT = 10  # 重试间隔 10s


class BaseDataSpider:

    @staticmethod
    async def save_db(table, data):
        """ 保存数据库 """
        await table.create(**data)

    @staticmethod
    async def bulk_save_db(table, data_list):
        """
        批量插入:  Iterable[MODEL], 列表中的元素应为 model
        """
        await table.bulk_create(data_list)

    @staticmethod
    async def parse(resp):
        """
        解析HTML数据 parsel 是 scrapy 内置的解析器
            >>> from parsel import Selector
            >>> doc = Selector(text=resp.text)
        解析json数据
            >>> data = resp.json()
        """
        pass


class BaseSpider(BaseDataSpider):
    """基础爬虫"""

    def __init__(self, name=None,
                 start_url=None,
                 headers=None,
                 ):
        """
        name: str 爬虫名称/域名/表名， 用于记录日志
        """
        self.name = name
        self.start_url = start_url
        self.session: Session = Session()
        self.headers = headers or {}
        self.last_ua = ''
        self.ua = UserAgent()

    def random_ua(self, headers=None):
        """随机 UA"""
        if headers:
            headers['User-Agent'] = self.get_ua()
            return headers
        else:
            self.headers['User-Agent'] = self.get_ua()
            return self.headers

    def get_ua(self):
        while True:
            ua_ = self.ua.random
            # 不是IE 并且 不是上一次使用的 UA
            if 'MSIE' not in str(ua_) and self.last_ua != ua_:
                self.last_ua = ua_
                return ua_

    def responses(self, resp, **kwargs):
        """可以再次处理相关异常"""
        if resp.status_code >= 400:
            # 请求异常
            self.random_ua(**kwargs)  # 切换 UA 重试时使用新UA
            raise HTTPError(f'{resp.url}-{resp.status_code}请求异常')
        return resp

    @retry(retry=stop_after_attempt(MAX_RETRY), wait=wait_fixed(WAIT_FIXED))
    def get(self, url, **kwargs):
        """get 请求"""
        resp = self.session.get(url, **kwargs)
        return self.responses(resp)

    @retry(retry=stop_after_attempt(MAX_RETRY), wait=wait_fixed(WAIT_FIXED))
    def post(self, url, **kwargs):
        """post 请求"""
        resp = self.session.post(url, **kwargs)
        return self.responses(resp)

    @staticmethod
    def parse_range(file_size, slice):
        arr = list(range(0, file_size, slice))
        result = []
        for _ in range(len(arr) - 1):
            s_pos, e_pos = arr[_], arr[_ + 1] - 1
            result.append([s_pos, e_pos])
        result[-1][-1] = file_size - 1
        return result

    @timer
    def download(self, url, file: Path, method='get', **kwargs):
        """requests 数据流 方式下载文件"""
        if not file.exists():
            file.touch()  # 创建文件

        if method.lower() == 'get':  # 1M
            res = self.get(url, **kwargs, stream=True)
            with file.open('wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            res = self.post(url, **kwargs, stream=True)
            with file.open('wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)


class AioSpider(BaseSpider):
    def __init__(self, name=None, headers=None, sem: int = 15):
        """
        name: str 爬虫名称/域名/表名
        """
        super().__init__(name=name, headers=headers)
        # max_keepalive_connections 允许的保持活动状态连接数，或None始终允许。（默认值 20）
        # max_connections 允许的最大连接数，或None无限制。（默认值 100）
        limits = httpx.Limits(max_keepalive_connections=sem, max_connections=sem + 3)
        self.client = httpx.AsyncClient(limits=limits)  # 异步

    @retry(retry=stop_after_attempt(MAX_RETRY), wait=wait_fixed(WAIT_FIXED))
    async def aio_get(self, url, **kwargs):
        """get 请求"""
        resp = await self.client.get(url,
                                     follow_redirects=True,
                                     timeout=TIMEOUT,
                                     **kwargs)
        return self.responses(resp)

    @retry(retry=stop_after_attempt(MAX_RETRY), wait=wait_fixed(WAIT_FIXED))
    async def aio_post(self, url, **kwargs):
        """post 请求"""
        resp = await self.client.post(url,
                                      follow_redirects=True,
                                      timeout=TIMEOUT,
                                      **kwargs)
        return self.responses(resp)

    @retry(retry=stop_after_attempt(MAX_RETRY), wait=wait_fixed(WAIT_FIXED))
    async def async_range_download(self, url, file: Path, s_pos, e_pos, method='get', **kwargs):
        """异步下载 seek 写入对应位置"""
        headers = {"Range": f"bytes={s_pos}-{e_pos}"}
        if method.lower() == 'get':
            res = await self.aio_get(url, headers=headers, **kwargs)
        else:
            res = await self.aio_post(url, headers=headers, **kwargs)
        with open(file, "rb+") as f:
            f.seek(s_pos)
            f.write(res.content)

    @timer
    async def aio_download(self, url, file: Path, method='get',slice=5 **kwargs):
        """httpx 异步分片式 下载文件
            slice 默认最高分成10个分片， 同时并发下载
        """
        if not file.exists():
            file.touch()  # 创建文件  片

        res = httpx.head(url, **kwargs)
        filesize = int(res.headers['Content-Length'])
        if filesize > 1_000_000:  # 1M
            divisional_ranges = self.parse_range(file_size=filesize, slice=slice)
            tasks = [self.async_range_download(url, file, s_pos, e_pos, method=method) for s_pos, e_pos in
                     divisional_ranges]
            await asyncio.gather(*tasks)  # 异步并发下载
        else:
            if method.lower() == 'get':  # 1M
                res = await self.aio_get(url, **kwargs)
            else:
                res = await self.aio_post(url, **kwargs)
            file.write_bytes(res.content)


class BrowserDriver(BaseSpider):
    """浏览器驱动 爬虫"""

    def __init__(self, context, name=None):
        super().__init__(name)
        self.context = context

    @staticmethod
    async def add_js(page, js=None):
        js = js or """Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"""
        await page.add_init_script(js)

    async def new_page(self):
        page = await self.context.new_page()
        await self.add_js(page)
        return page

    @staticmethod
    async def get_html(page):
        """获取page 的 网页源码"""
        return await page.content()

    @staticmethod
    async def download_file(url, page, file: Path, click=None):
        """下载文件"""
        await page.goto(url)
        async with page.expect_download() as download2_info:
            if click:
                await page.locator(click).first.click()
        download = await download2_info.value
        await download.save_as(file)


async def example():
    """浏览器例子"""
    remote_ip = 'ws://127.0.0.1:3000'
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        if remote_ip:
            browser = await p.chromium.connect_over_cdp(remote_ip)
        else:
            browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        br = BrowserDriver(context=context, name='测试网站-浏览器爬虫')
        page = await br.new_page()
        await page.goto('https://earlywarning.fenqubiao.com/#/zh-cn/early-warning-journal-list-2024')
        pass


if __name__ == '__main__':
    asyncio.run(example())
