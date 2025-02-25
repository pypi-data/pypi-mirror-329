from playwright.async_api import async_playwright
import trafilatura
import random
import time
import urllib.parse
import asyncio
import subprocess
import sys
from kirara_ai.logger import get_logger
import os

logger = get_logger("WebSearchPlugin")

class WebSearcher:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.search_engines = {
            'bing': {
                'url': 'https://www.bing.com/search?q={}',
                'selectors': ['.b_algo', '#b_results .b_algo', 'main .b_algo'],
                'title_selector': 'h2',
                'link_selector': 'h2 a',
                'snippet_selector': '.b_caption p'
            },
            'google': {
                'url': 'https://www.google.com/search?q={}',
                'selectors': ['.MjjYud', 'div.g', 'div[data-hveid]'],
                'title_selector': 'h3.LC20lb',
                'link_selector': 'a[jsname="UWckNb"], div.yuRUbf a',
                'snippet_selector': 'div.VwiC3b'
            },
            'baidu': {
                'url': 'https://www.baidu.com/s?wd={}',
                'selectors': ['.result', '.result-op'],
                'title_selector': 'h3',
                'link_selector': 'h3 a',
                'snippet_selector': '.content-right_8Zs40'
            }
        }

    @classmethod
    async def create(cls):
        """创建 WebSearcher 实例的工厂方法"""
        self = cls()
        return self

    async def _ensure_initialized(self,proxy):
        """确保浏览器已初始化"""
        try:
            self.playwright = await async_playwright().start()

            # 创建用户数据目录路径
            user_data_dir = os.path.join(os.path.expanduser("~"), ".playwright_user_data")
            os.makedirs(user_data_dir, exist_ok=True)

            # 合并所有选项到一个字典
            context_options = {
                'headless': True,
                'chromium_sandbox': False,
                'slow_mo': 50,  # 减慢操作速度，更像人类
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',  # 隐藏自动化控制痕迹
                    '--disable-features=IsolateOrigins,site-per-process',
                ],
                'ignore_default_args': ['--enable-automation'],  # 屏蔽自动化标志
                'viewport': {'width': 1920, 'height': 1080},
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'locale': 'zh-CN',
                'timezone_id': 'Asia/Shanghai',
                'color_scheme': 'dark',  # 或 'light'，根据用户习惯
                'device_scale_factor': 1.75,  # 高DPI设备
                'has_touch': True,  # 支持触摸
                'is_mobile': False,
                'reduced_motion': 'no-preference'
            }

            # 如果是 Google 搜索，添加代理设置
            if proxy:
                context_options['proxy'] = {
                    'server': proxy
                }

            try:
                # 使用 launch_persistent_context 代替分开的 launch 和 new_context
                self.context = await self.playwright.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    **context_options
                )

                self.browser = None  # 不再需要单独的browser引用

            except Exception as e:
                if "Executable doesn't exist" in str(e):
                    logger.info("Installing playwright browsers...")
                    process = subprocess.Popen(
                        [sys.executable, "-m", "playwright", "install", "chromium"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        raise RuntimeError(f"Failed to install playwright browsers: {stderr.decode()}")

                    # 重试使用 launch_persistent_context
                    self.context = await self.playwright.chromium.launch_persistent_context(
                        user_data_dir=user_data_dir,
                        **context_options
                    )
                else:
                    raise

            # 注入脚本来伪装webdriver标记
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });

                // 防止 iframe 检测
                window.parent.document;

                // 防止检测到 Chrome Devtools 协议
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)

            return self.context

        except Exception as e:
            logger.error(f"Failed to initialize WebSearcher: {e}")
            await self.close()
            raise

    async def simulate_human_scroll(self, page):
        """模拟人类滚动"""
        for _ in range(3):
            await page.mouse.wheel(0, random.randint(300, 700))

    async def get_webpage_content(self, url: str, timeout: int,context) -> str:
        """获取网页内容"""
        start_time = time.time()
        try:
            # 创建新标签页获取内容
            page = await context.new_page()
            try:
                # 设置更严格的资源加载策略
                await page.route("**/*", lambda route: route.abort()
                    if route.request.resource_type in ['image', 'stylesheet', 'font', 'media']
                    else route.continue_())

                # 使用 domcontentloaded 而不是 networkidle
                await page.goto(url, wait_until='domcontentloaded', timeout=timeout * 1000)

                # 等待页面主要内容加载，但设置较短的超时时间
                try:
                    await page.wait_for_load_state('domcontentloaded', timeout=5000)
                except Exception as e:
                    logger.warning(f"Load state timeout for {url}, continuing anyway: {e}")

                await self.simulate_human_scroll(page)

                content = await page.content()
                text = trafilatura.extract(content)

                await page.close()
                logger.info(f"Content fetched - URL: {url} - Time: {time.time() - start_time:.2f}s")
                return text or ""
            except Exception as e:
                await page.close()
                logger.error(f"Failed to fetch content - URL: {url} - Error: {e}")
                return ""
        except Exception as e:
            logger.error(f"Failed to create page - URL: {url} - Error: {e}")
            return ""

    async def process_search_result(self, result, idx: int, timeout: int, fetch_content: bool, context, engine='bing'):
        """处理单个搜索结果"""
        try:
            engine_config = self.search_engines[engine]
            title_element = await result.query_selector(engine_config['title_selector'])
            link_element = await result.query_selector(engine_config['link_selector'])
            snippet_element = await result.query_selector(engine_config['snippet_selector'])

            if not title_element or not link_element:
                return None

            title = await title_element.inner_text()
            link = await link_element.get_attribute('href')

            # 对于百度搜索需要特殊处理链接
            if engine == 'baidu':
                try:
                    # 创建新页面来获取真实URL
                    new_page = await context.new_page()
                    await new_page.goto(link, wait_until='domcontentloaded', timeout=5000)
                    real_url = new_page.url
                    await new_page.close()
                    link = real_url
                except Exception as e:
                    logger.warning(f"Failed to get real URL from Baidu: {e}")

            snippet = await snippet_element.inner_text() if snippet_element else "无简介"

            if not link:
                return None

            result_text = f"[{idx+1}] {title}\nURL: {link}\n搜索简介: {snippet}"

            if fetch_content:

                content = await self.get_webpage_content(link, timeout,context)
                if content:
                    result_text += f"\n内容详情:\n{content}"

            return result_text

        except Exception as e:
            logger.error(f"Failed to process result {idx}: {e}")
            return None

    async def search(self, query: str, max_results: int = 3, timeout: int = 10, fetch_content: bool = True, engine: str = 'bing', proxy: str = None) -> str:
        """执行搜索"""
        if engine not in self.search_engines:
            return f"不支持的搜索引擎: {engine}"

        # 设置当前搜索引擎
        self.current_engine = engine
        context = await self._ensure_initialized(proxy)
        engine_config = self.search_engines[engine]
        search_start_time = time.time()
        page = None

        try:
            encoded_query = urllib.parse.quote(query)
            page = await context.new_page()

            # Google搜索特定处理
            await page.goto(
                                engine_config['url'].format(encoded_query),
                                wait_until='load',
                                timeout=timeout * 1000
                            )

            # 使用搜索引擎特定的选择器
            results = None

            # 对于Google，让页面有更多时间加载
            if engine == 'google':
                await self.simulate_human_scroll(page)

            for selector in engine_config['selectors']:
                try:
                    logger.info(f"Trying selector: {selector}")
                    await page.wait_for_selector(selector, timeout=8000)  # 增加等待时间
                    results = await page.query_selector_all(selector)
                    if results and len(results) > 0:
                        logger.info(f"Found {len(results)} results with selector {selector}")
                        break
                except Exception as e:
                    logger.warning(f"Selector {selector} failed: {e}")
                    continue

            if not results:
                # 尝试直接使用 JavaScript 获取元素
                if engine == 'google':
                    try:
                        # 使用更通用的JavaScript选择器尝试获取结果
                        results = await page.evaluate("""
                            () => {
                                const elements = document.querySelectorAll('div[data-sokoban-container], div.g, .MjjYud');
                                return Array.from(elements).length;
                            }
                        """)
                        logger.info(f"JavaScript found {results} elements")

                        # 如果找到了元素，使用evaluate来处理它们
                        if results > 0:
                            # 自定义处理逻辑...
                            pass
                    except Exception as e:
                        logger.error(f"JavaScript evaluation failed: {e}")

                logger.error("No search results found with any selector")
                await page.screenshot(path=f'search_failed_{engine}.png')
                return "搜索结果加载失败"

            logger.info(f"Found {len(results)} search results")

            tasks = []
            for idx, result in enumerate(results[:max_results]):
                tasks.append(self.process_search_result(result, idx, timeout, fetch_content, context, engine))

            detailed_results = []
            completed_results = await asyncio.gather(*tasks)

            for result in completed_results:
                if result:
                    detailed_results.append(result)

            total_time = time.time() - search_start_time
            results = "\n---\n".join(detailed_results) if detailed_results else "未找到相关结果"
            logger.info(f"Search completed - Query: {query} - Time: {total_time:.2f}s - Found {len(detailed_results)} valid results")
            return results

        except Exception as e:
            logger.error(f"Search failed - Query: {query} - Error: {e}", exc_info=True)
            return f"搜索失败: {str(e)}"
        finally:
            if page:
                try:
                    await page.close()
                except Exception as e:
                    logger.error(f"Error closing page: {e}")

    async def close(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
