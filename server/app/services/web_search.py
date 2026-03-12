import httpx
import asyncio
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import logging

from app.core.exceptions import SearchException
from app.utils.retry import async_retry

logger = logging.getLogger(__name__)


class WebSearchServiceV2:
    """Enhanced web search service with error handling"""

    def __init__(self):
        self.timeout = 30.0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    @async_retry(
        max_attempts=3, delay=2.0, exceptions=(httpx.HTTPError, httpx.TimeoutException)
    )
    async def search(
        self, query: str, num_results: int = 10, provider: str = "duckduckgo"
    ) -> List[dict]:
        """Search with retry logic"""
        try:
            if not query or not query.strip():
                raise SearchException("Search query cannot be empty", "EMPTY_QUERY")

            if provider == "duckduckgo":
                return await self._search_duckduckgo(query, num_results)
            else:
                raise SearchException(
                    f"Unknown provider: {provider}", "INVALID_PROVIDER"
                )

        except httpx.TimeoutException:
            logger.error(f"Search timeout for query: {query}")
            raise SearchException(
                "Search request timed out. Please try again.", "SEARCH_TIMEOUT"
            )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during search: {str(e)}")
            raise SearchException(
                "Failed to connect to search service", "SEARCH_CONNECTION_ERROR"
            )
        except Exception as e:
            logger.error(f"Unexpected search error: {str(e)}")
            raise SearchException(f"Search failed: {str(e)}", "SEARCH_FAILED")

    async def _search_duckduckgo(self, query: str, num_results: int) -> List[dict]:
        """DuckDuckGo search implementation"""
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout, headers=self.headers
            ) as client:
                url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
                response = await client.get(url)

                if response.status_code != 200:
                    raise SearchException(
                        f"Search returned status code: {response.status_code}",
                        "SEARCH_HTTP_ERROR",
                    )

                soup = BeautifulSoup(response.text, "html.parser")
                results = []

                for result in soup.find_all("div", class_="result")[:num_results]:
                    title_tag = result.find("a", class_="result__a")
                    snippet_tag = result.find("a", class_="result__snippet")

                    if title_tag and snippet_tag:
                        href = title_tag.get("href", "")
                        # Extract actual URL from DuckDuckGo redirect
                        actual_url = href
                        if "uddg=" in href:
                            from urllib.parse import unquote, urlparse

                            try:
                                parsed = href.split("uddg=")[1].split("&")[0]
                                actual_url = unquote(parsed)
                            except:
                                actual_url = href

                        # Skip if URL is empty or invalid
                        if not actual_url or not actual_url.startswith("http"):
                            continue

                        results.append(
                            {
                                "title": title_tag.get_text(strip=True),
                                "url": actual_url,
                                "snippet": snippet_tag.get_text(strip=True),
                                "source": "duckduckgo",
                            }
                        )

                if not results:
                    logger.warning(f"No results found for query: {query}")

                return results

        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            raise

    @async_retry(max_attempts=2, delay=1.0)
    async def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch page content with retry"""
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout, headers=self.headers
            ) as client:
                response = await client.get(url, follow_redirects=True)

                if response.status_code != 200:
                    logger.warning(
                        f"Failed to fetch {url}: status {response.status_code}"
                    )
                    return None

                soup = BeautifulSoup(response.text, "html.parser")

                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                text = soup.get_text(separator="\n", strip=True)
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                content = "\n".join(lines)

                return content[:5000]  # Limit content size

        except Exception as e:
            logger.warning(f"Error fetching {url}: {str(e)}")
            return None

    async def search_and_fetch(
        self,
        query: str,
        num_results: int = 5,
        fetch_content: bool = True,
        provider: str = "duckduckgo",
    ) -> List[dict]:
        """Search and fetch with error handling"""
        results = await self.search(query, num_results, provider)

        if not fetch_content:
            return results

        enriched_results = []

        for result in results:
            try:
                content = await self.fetch_page_content(result["url"])
                result["content"] = content if content else result["snippet"]
                enriched_results.append(result)
            except Exception as e:
                logger.warning(f"Failed to fetch content for {result['url']}: {str(e)}")
                result["content"] = result["snippet"]
                enriched_results.append(result)

        return enriched_results


web_search_service_v2 = WebSearchServiceV2()


# import httpx
# from typing import List, Optional
# from bs4 import BeautifulSoup
# from urllib.parse import quote_plus
# import logging
# from app.core.exceptions import SearchException
# from app.utils.retry import async_retry

# logger = logging.getLogger(__name__)

# class WebSearchService:
#     """Web search service with error handling"""

#     def __init__(self):
#         self.timeout = 30.0
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
#         }

#     @async_retry(max_attempts=3, delay=2.0, exceptions=(httpx.HTTPError, httpx.TimeoutException))
#     async def search(self, query: str, num_results: int = 10) -> List[dict]:
#         """Search using DuckDuckGo"""
#         try:
#             if not query or not query.strip():
#                 raise SearchException("Search query cannot be empty", "EMPTY_QUERY")

#             async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
#                 url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
#                 response = await client.get(url)

#                 if response.status_code != 200:
#                     raise SearchException(
#                         f"Search returned status code: {response.status_code}",
#                         "SEARCH_HTTP_ERROR"
#                     )

#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 results = []

#                 for result in soup.find_all('div', class_='result')[:num_results]:
#                     title_tag = result.find('a', class_='result__a')
#                     snippet_tag = result.find('a', class_='result__snippet')

#                     if title_tag and snippet_tag:
#                         results.append({
#                             'title': title_tag.get_text(strip=True),
#                             'url': title_tag.get('href', ''),
#                             'snippet': snippet_tag.get_text(strip=True),
#                             'source': 'duckduckgo'
#                         })

#                 return results

#         except httpx.TimeoutException:
#             logger.error(f"Search timeout for query: {query}")
#             raise SearchException("Search request timed out", "SEARCH_TIMEOUT")
#         except Exception as e:
#             logger.error(f"Search error: {str(e)}")
#             raise SearchException(f"Search failed: {str(e)}", "SEARCH_FAILED")

#     @async_retry(max_attempts=2, delay=1.0)
#     async def fetch_page_content(self, url: str) -> Optional[str]:
#         """Fetch and extract text from URL"""
#         try:
#             async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
#                 response = await client.get(url, follow_redirects=True)

#                 if response.status_code != 200:
#                     return None

#                 soup = BeautifulSoup(response.text, 'html.parser')

#                 for script in soup(["script", "style", "nav", "footer", "header"]):
#                     script.decompose()

#                 text = soup.get_text(separator='\n', strip=True)
#                 lines = [line.strip() for line in text.split('\n') if line.strip()]
#                 content = '\n'.join(lines)

#                 return content[:5000]

#         except Exception as e:
#             logger.warning(f"Error fetching {url}: {str(e)}")
#             return None

#     async def search_and_fetch(
#         self,
#         query: str,
#         num_results: int = 5,
#         fetch_content: bool = True
#     ) -> List[dict]:
#         """Search and optionally fetch content"""
#         results = await self.search(query, num_results)

#         if not fetch_content:
#             return results

#         enriched_results = []

#         for result in results:
#             try:
#                 content = await self.fetch_page_content(result['url'])
#                 result['content'] = content if content else result['snippet']
#                 enriched_results.append(result)
#             except Exception as e:
#                 logger.warning(f"Failed to fetch content for {result['url']}: {str(e)}")
#                 result['content'] = result['snippet']
#                 enriched_results.append(result)

#         return enriched_results

# web_search_service = WebSearchService()
