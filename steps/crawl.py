from dataExtraction.crawlers import CrawlerDispatcher
from urllib.parse import urlparse
from loguru import logger
from clearml import Task
#from models.documentModels import UserDocument
from typing_extensions import Annotated
from tqdm import tqdm
from clearml import PipelineDecorator
# task = Task.init(
#     project_name="My Project",
#     task_name="Data Collection",
#     task_type=Task.TaskTypes.data_processing
# )
@PipelineDecorator.component(name="get_links",output_name="links")
def get_links(filePath:str) -> list[str]:
    links = []
    with open(filePath) as f:
        for line in f:
            links.append(line.strip())
    return links
@PipelineDecorator.component(name="crawl_links",)
def crawl_links( links: list[str]) -> Annotated[list[str], "crawled_links"]:
    dispatcher = CrawlerDispatcher.build().register_github().register_medium().register_youtube()#.register_linkedin()

    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successfull_crawls = 0
    for link in tqdm(links):
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link)
        successfull_crawls += successfull_crawl
    #     metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    # step_context = get_step_context()
    #step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)
    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.",link)

    return links


def _crawl_link(dispatcher: CrawlerDispatcher, link: str) -> tuple[bool, str]:
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        print(crawler)
        crawler.extract(link=link)
        return (True, crawler_domain)
    except Exception as e:
        logger.error(f"An error occurred while crawling: {str(e)}")
        return (False, crawler_domain)