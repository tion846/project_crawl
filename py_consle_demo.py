from project_crawl.share.models import Product, Base
from project_crawl.share.utils import print_line, get_settings, init_logging, init_db_connect, get_db_connect_string
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from time import gmtime, strftime, localtime
from types import SimpleNamespace
from urllib.parse import urlparse, parse_qs, urljoin, quote
import datetime
import json
import os
import requests
import scrapy
import sqlalchemy
import sqlite3


settings = get_project_settings()
output_folder = settings.get("JSON_PIPELINE_OUTPUT_FOLDER")
init_logging()

init_db_connect()

products = []

db_connect_string = get_db_connect_string()
engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

with Session(engine) as session:
    statement = select(Product).where(Product.Spec_Json == None).limit(1)
    products = session.scalars(statement).all()

    item = products[0]
    print_line(item)

    item.Spec_Json = "spec"
    print_line(item.Spec_Json)

    session.execute(update(Product), [
        {"Id": item.Id, "Spec_Json": "spec"}
    ])
    session.commit()


data = {
    "Name": "T1",
    "Link": "/store/pdb/T1",
    "Spec_Api": "/store/app/web/api/pdb%2FT1/async",
    "Sale_price": "$699.99",
    "Brand": "HP",
    "Category": "Docking",
}


# item = Product(**data)
# print_line(item)


# url = "https://www.hp.com/us-en/shop/sitesearch?keyword=Docking"
# parsed_url = urlparse(url)
# dict_query_string = parse_qs(parsed_url.query)
# print_line(dict_query_string)
# category = dict_query_string["keyword"].pop()

# print_line(category)

# Base = declarative_base()
# metadata = MetaData()
# db_connect_string = os.path.join(os.getcwd(), "SQLite", "testDB.db")
# engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

# db_connect_string = os.path.join(os.getcwd(), "SQLite", "testDB.db")
# engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)
# Base.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add_all([
#         Product(name="T1",
#                 link="/store/pdb/T1",
#                 spec_link="/store/app/web/api/pdb%2FT1/async",
#                 sale_price="$699.99"),
#         Product(name="T2",
#                 link="/store/pdb/T2",
#                 spec_link="/store/app/web/api/pdb%2FT2/async",
#                 sale_price="$899.00")
#     ])
#     session.commit()


def add_product_samples():
    """ SqlAlchemy ORM """
    db_connect_string = os.path.join(os.getcwd(), "SQLite", "CrawlDB.db")
    print_line(db_connect_string)
    engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

    with Session(engine) as session:
        session.add_all([
            Product(name="T1",
                    link="/store/pdb/T1",
                    spec_link="/store/app/web/api/pdb%2FT1/async",
                    sale_price="$699.99"),
            Product(name="T2",
                    link="/store/pdb/T2",
                    spec_link="/store/app/web/api/pdb%2FT2/async",
                    sale_price="$899.00")
        ])
        session.commit()

# region method


def httpRequset():
    print_line(get_settings("NONE_EXIST"))
    print_line(get_settings("JSON_PIPELINE_OUTPUT_FOLDER"))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    url = "https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fomen-gaming-laptop-16t-wf000-161-76w27av-1/async"
    res = requests.get(url=url, headers=headers)
    result = res.json()

    print_line(type(result))
    print_line(result["data"]["page"]["pageComponents"]
               ["pdpTechSpecs"]["technical_specifications"])


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
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    print_line(t)
    print_line(s[:-3])

    print_line("today", datetime.date.today())
    print_line("now", datetime.datetime.now())

    f_time = strftime("%Y/%m/%d %H:%M:%S", gmtime())
    print_line("gmtime", f_time)
    f_time = strftime("%Y/%m/%d %H:%M:%S", localtime())
    print_line("localtime", f_time)


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
