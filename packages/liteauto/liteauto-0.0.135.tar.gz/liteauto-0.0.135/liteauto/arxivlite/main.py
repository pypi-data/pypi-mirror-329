from pandas import DataFrame

from .schema import ArxivTags,Paper
from .utils import (build_urls_from_tag,
                    download_html,
                    multiprocessing_parse_arxiv_html,
                    post_process_deduplication)


def get_todays_arxiv_papers() -> DataFrame:
    """return dataframe of todays reserach papers and its infromation release in arxiv website"""
    tags = ArxivTags()

    urls = build_urls_from_tag(tags)
    data = download_html(urls)
    results: list[Paper] = multiprocessing_parse_arxiv_html(data)

    df_filtered: DataFrame = post_process_deduplication(results)
    return df_filtered