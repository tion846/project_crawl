from project_crawl.share.utils import print_line
from scrapy.utils.project import get_project_settings
from time import gmtime, strftime, localtime
from types import SimpleNamespace
from urllib.parse import urlparse, parse_qs, urljoin, quote
import json
import os


settings = get_project_settings()
output_folder = settings.get("JSON_PIPELINE_OUTPUT_FOLDER")


# region method
def encode_url():
    # See https://www.urlencoder.io/python/
    # See https://stackoverflow.com/questions/10113090/best-way-to-parse-a-url-query-string

    url_list = [
        "/us-en/shop/pdp/hp-envy-x360-2-in-1-laptop-15z-fh000-156-77w47av-1",
        "/us-en/shop/pdp/victus-gaming-laptop-16-s0097nr",
        "/us-en/shop/pdp/omen-gaming-laptop-16-xf0087nr",
    ]
    host = "https://www.hp.com/us-en/shop/app/api/web/graphql/page/"
    suffix = "async"
    for url in url_list:
        prod = url.replace("/us-en/shop/", "")
        encode_prod = quote(prod, safe="")
        result = urljoin(host, f"{encode_prod}/{suffix}")
        print_line(result)


def time_formatter():
    f_time = strftime("%Y/%m/%d %H:%M:%S", gmtime())
    print_line(f_time)
    f_time = strftime("%Y/%m/%d %H:%M:%S", localtime())
    print_line(f_time)
    print_line(gmtime())


def check_folder_exiest():
    print_line(os.getcwd())
    output_path = os.path.join(os.getcwd(),
                               output_folder)

    if not os.path.exists(output_path):
        os.mkdir(output_path)


def simplenamespace_to_dict():
    """
    simplenamesapce to dict
    See https://stackoverflow.com/questions/52783883/how-to-initialize-a-dict-from-a-simplenamespace
    """
    output_file = "simplenamespace_items.json"
    output_file_path = os.path.join(
        os.getcwd(),
        output_folder,
        output_file
    )

    # 產生SimpleNamespace假資料
    data_set = []
    for i in range(5):
        item = SimpleNamespace(name=f"Name_{i}",
                               value=f"Value_{i}",
                               remark=[i, i**2, i**3])
        data_set.append(item)

    # SimpleNamespace轉換成dict
    dict_data = []
    for ds in data_set:
        dict_data.append(vars(ds))

    # dumps dict
    result = json.dumps(dict_data)

    file = open(output_file_path, "w")
    file.write(result)
    file.close()


def dict_to_simplenamespace():
    """
    取得json檔案內容
    See https://stackoverflow.com/a/15882054

    dict to simplenamespace
    See https://stackoverflow.com/questions/50296097/how-to-initialize-a-simplenamespace-from-a-dict
    """
    output_file = "simplenamespace_items.json"
    output_file_path = os.path.join(
        os.getcwd(),
        output_folder,
        output_file
    )

    with open(f"{output_file_path}", "r") as file_json:
        contnets = file_json.readlines()

    # 將json資料轉換成SimpleNamespace
    data = json.loads("".join(contnets),
                      object_hook=lambda d: SimpleNamespace(**d))

    # 操作SimpleNamespace
    for x in data:
        print_line(x.name, x.value, x.remark, hasattr(x, "Remark"))


def parse_search_api_response():
    """
    ’cp950′ codec can’t decode byte 0xe6 in position 111: illegal multibyte sequence
    See https://www.wongwonggoods.com/all-posts/python/python-debug-error/cp950-codec-python/
    """
    folder = "reference"
    file_name = "search.json"
    path = os.path.join(os.getcwd(), folder, file_name)

    with open(f"{path}", "r", encoding="utf-8") as file_json:
        contnets = file_json.readlines()

    data = json.loads("".join(contnets),
                      object_hook=lambda x: SimpleNamespace(**x))

    for doc in data.Results:
        x = doc.Document
        print_line([x.pdp_url, x.sale_price, x.product_name])
# endregion


# time_formatter()
# check_folder_exiest()
# simplenamespace_to_dict()
# dict_to_simplenamespace()
# parse_search_api_response()
# encode_url()
