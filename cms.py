import aiohttp
import asyncio
from utils.tools import titles_html, FingerPrintcms, parse_args, banner, readurlfile, save_csv
from loguru import logger


class Reqfing(object):
    def __init__(self):
        self.cms = FingerPrintcms()
        self.headers = {"Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
        self.args = parse_args()

    async def get_fingerprint(self, url, sem):
        async with sem:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                try:
                    async with session.get(url, ssl=False, timeout=self.args.t) as resp:
                        title = await titles_html(await resp.text())
                        zhiwenname = await self.parser(title, resp.headers, await resp.text())
                        print(resp.status, title, zhiwenname, url)
                        return [resp.status, title, zhiwenname, url]
                except Exception as e:
                    print(e)

    async def parser(self, title, header, body):
        # 遍历规则字符串列表并解析
        name = self.cms.astz(title, header, body)
        return name

    async def start(self):
        sem = asyncio.Semaphore(int(self.args.sem))
        if self.args.f != None and self.args.u != None:
            banner()
            logger.debug("请输入单个url或者文件")

        elif self.args.f != None:
            try:
                banner()
                urls = readurlfile(self.args.f)
                logger.info("开始进行批量cms识别 共计{}个".format(len(urls)))
                tasks = [asyncio.create_task(self.get_fingerprint(url, sem)) for url in urls]
                done, pending = await asyncio.wait(tasks)
                data = [result.result() for result in done]
                save_csv(data)

            except Exception as e:
                logger.error(e)
        elif self.args.u != None:
            try:
                banner()
                logger.info("开始进行单个cms识别")
                target = self.args.u
                if str(target).startswith(("http://", "https://")):
                    data = await self.get_fingerprint(target, sem)
                    self.cms.update()
                else:
                    logger.debug("python3 cms.py -u https://www.baidu.com。")

            except Exception as e:
                logger.error(e)
        else:
            logger.info('python3 cms.py -h 查看帮助')

    async def main(self):
        await self.start()


if __name__ == '__main__':
    import time

    start = time.time()
    test = Reqfing()
    asyncio.run(main=test.main())
    print(time.time() - start)
