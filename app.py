from dataExtraction.crawlers import GitHubCrawler
from loguru import logger
from models.documentModels import UserDocument
from typing_extensions import Annotated
from tqdm import tqdm
from dataExtraction.crawlers import CrawlerDispatcher
from urllib.parse import urlparse
def openFile():
    file = open("urls.txt", "r")
    urls = file.readlines()
    file.close()    
    return urls
# def crawl(url):
#     visited_urls = []
#     crawled_urls = []
#     for url in openFile():
#         if url not in visited_urls:
#             url = url.strip()
#             response = requests.get(url)
#             soup = BeautifulSoup(response.content, "html.parser")
#             visited_urls.append(url)
#             crawled_urls.append(soup)
#             #print(soup.find("p"))   
#         else:
#             print("Already visited")
#     return crawled_urls
def split_user_full_name(user: str | None) -> tuple[str, str]:
    if user is None:
        raise Exception("User name is empty")

    name_tokens = user.split(" ")
    if len(name_tokens) == 0:
        raise Exception("User name is empty")
    elif len(name_tokens) == 1:
        first_name, last_name = name_tokens[0], name_tokens[0]
    else:
        first_name, last_name = " ".join(name_tokens[:-1]), name_tokens[-1]

    return first_name, last_name
def get_or_create_user(user_full_name: str) -> Annotated[UserDocument, "user"]:
    logger.info(f"Getting or creating user: {user_full_name}")

    first_name, last_name = split_user_full_name(user_full_name)

    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    # step_context = get_step_context()
    # step_context.add_output_metadata(output_name="user", metadata=_get_metadata(user_full_name, user))

    return user

def crawl_links(user: UserDocument, links: list[str]) -> Annotated[list[str], "crawled_links"]:
    dispatcher = CrawlerDispatcher.build().register_github()#.register_linkedin().register_medium()

    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successfull_crawls = 0
    for link in tqdm(links):
        print(user)
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successfull_crawls += successfull_crawl

    #     metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    # step_context = get_step_context()
    #step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.")

    return links


def _crawl_link(dispatcher: CrawlerDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        print(crawler)
        crawler.extract(link=link, user=user)

        return (True, crawler_domain)
    except Exception as e:
        logger.error(f"An error occurred while crowling: {e!s}")
        return (False, crawler_domain)
if __name__ == "__main__":
    githubCrawler = GitHubCrawler()
    user = get_or_create_user("John Doe")
    urls=["https://github.com/ros/ros.git","https://github.com/ros/ros.git"]
    # for url in openFile():
    #    urls.append(url)
    crawl_links(user, urls)



