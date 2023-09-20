from scrapy.utils.project import get_project_settings
from time import gmtime, strftime
from types import SimpleNamespace
import json
import os


settings = get_project_settings()
output_folder = settings.get("JSON_PIPELINE_OUTPUT_FOLDER")


def time_formatter():
    f_time = strftime("%Y%m%d", gmtime())
    print(f_time)
    print(gmtime())


def check_folder_exiest():
    print(os.getcwd())
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
        print(x.name, x.value, x.remark, hasattr(x, "Remark"))


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
        print([x.pdp_url, x.sale_price, x.product_name])


# time_formatter()
# check_folder_exiest()
# simplenamespace_to_dict()
# dict_to_simplenamespace()
# parse_search_api_response()


# VisitId: cookie hawk_visit_id
# VisitorId: cookie hawk_visitor_id
# ClientGuid: process.env.HAWKSEARCH_CLIENT_GUID
js_script = """
    let url = "https://essearchapi-na.hawksearch.com/api/v2/search";
    let input = {
        "query": "type:product",
        "ClientData": {
            "VisitId": "f4359327-1caf-4744-b575-30d553286896",
            "VisitorId": "673cf168-236f-4757-8a0d-ab7aedfcc21b",
            //"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31",
        },
        "PageNo": 2,
        "Keyword": "Laptops",
        "ClientGuid": "bdeebee3d2b74c8ea58522bb1db61f8e"
    };
    let data = await fetch(url, {
        method: "POST",
        body: JSON.stringify(input),
        headers: new Headers({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        })
    });
    let result = await data.json();
    return result;
"""
