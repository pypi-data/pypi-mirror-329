from playwright.async_api import async_playwright
import trafilatura
import random
import time
import urllib.parse
import asyncio
import subprocess
import sys
from framework.logger import get_logger

logger = get_logger("WebSearchPlugin")

class WebSearcher:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None

    @classmethod
    async def create(cls):
        """创建 WebSearcher 实例的工厂方法"""
        self = cls()
        return self

    async def _ensure_initialized(self):
        """确保浏览器已初始化"""
        try:
            self.playwright = await async_playwright().start()
            try:
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    chromium_sandbox=False,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
                )
            except Exception as e:
                if "Executable doesn't exist" in str(e):
                    logger.info("Installing playwright browsers...")
                    # 使用 python -m playwright install 安装浏览器
                    process = subprocess.Popen(
                        [sys.executable, "-m", "playwright", "install", "chromium"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()
                    if process.returncode != 0:
                        raise RuntimeError(f"Failed to install playwright browsers: {stderr.decode()}")

                    # 重试启动浏览器
                    self.browser = await self.playwright.chromium.launch(
                        headless=False,
                        chromium_sandbox=False,
                        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
                    )
                else:
                    raise
            return await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            )
        except Exception as e:
            logger.error(f"Failed to initialize WebSearcher: {e}")
            await self.close()
            raise

    async def random_sleep(self, min_time=1, max_time=3):
        """随机等待"""
        await asyncio.sleep(random.uniform(min_time, max_time))

    async def simulate_human_scroll(self, page):
        """模拟人类滚动"""
        for _ in range(3):
            await page.mouse.wheel(0, random.randint(300, 700))
            await self.random_sleep(0.3, 0.7)

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

                await self.random_sleep(1, 2)
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

    async def process_search_result(self, result, idx: int, timeout: int, fetch_content: bool,context):
        """处理单个搜索结果"""
        try:
            title_element = await result.query_selector('h2')
            link_element = await result.query_selector('h2 a')
            snippet_element = await result.query_selector('.b_caption p')

            if not title_element or not link_element:
                return None

            title = await title_element.inner_text()
            link = await link_element.get_attribute('href')
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

    async def search(self, query: str, max_results: int = 3, timeout: int = 10, fetch_content: bool = True) -> str:
        """执行搜索"""
        context = await self._ensure_initialized()

        search_start_time = time.time()
        page = None
        try:
            encoded_query = urllib.parse.quote(query)
            page = await context.new_page()

            # 添加重试逻辑
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logger.info(f"Attempting to load search page (attempt {attempt + 1}/{max_retries})")
                    await page.goto(
                        f"https://www.bing.com/search?q={encoded_query}",
                        wait_until='domcontentloaded',
                        timeout=timeout * 1000
                    )

                    # 检查页面是否为空
                    content = await page.content()
                    if 'b_algo' not in content:
                        if attempt < max_retries - 1:
                            await page.reload()
                            await self.random_sleep(1, 2)
                            continue
                    else:
                        break
                except Exception as e:
                    logger.warning(f"Page navigation failed on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        await self.random_sleep(1, 2)
                        continue
                    else:
                        raise

            # 使用更可靠的选择器等待策略
            try:
                selectors = ['.b_algo', '#b_results .b_algo', 'main .b_algo']
                results = None

                for selector in selectors:
                    try:
                        await page.wait_for_selector(selector, timeout=5000)
                        results = await page.query_selector_all(selector)
                        if results and len(results) > 0:
                            break
                    except Exception:
                        continue

                if not results:
                    logger.error("No search results found with any selector")
                    return "搜索结果加载失败"

            except Exception as e:
                logger.error(f"Failed to find search results: {e}")
                return "搜索结果加载失败"

            logger.info(f"Found {len(results)} search results")

            tasks = []
            for idx, result in enumerate(results[:max_results]):
                tasks.append(self.process_search_result(result, idx, timeout, fetch_content,context))

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
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
