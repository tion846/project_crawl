
"""
import time
from time import gmtime, strftime

tt = strftime("%Y%m%d", gmtime())
print(tt)
print(gmtime())
"""


"""
import os

print(os.getcwd())
output_folder = "Output"
output_path = os.path.join(os.getcwd(), output_folder)

if not os.path.exists(output_path):
    os.mkdir(output_path)
"""

"""
# See https://stackoverflow.com/a/15882054
import json
import os
from types import SimpleNamespace

output_folder = "Output"
output_file = "items.json"
output_path = os.path.join(os.getcwd(), output_folder, output_file)

with open(f"{output_path}", "r") as file_json:
    contnet = file_json.readlines()

# Parse JSON into an object with attributes corresponding to dict keys.
data = json.loads(contnet.pop(), object_hook=lambda d: SimpleNamespace(**d))

for x in data:
    print(x.name, x.value, hasattr(x, "values"))

"""


"""
var url = "https://essearchapi-na.hawksearch.com/api/v2/search";
var data = {
  "query": "type:product",
  "ClientData": {
    "VisitId": "171032c9-4157-4ff8-9011-b8da8b36600e",
    "VisitorId": "db0717a3-1569-40cc-8bf2-32e224656f88",
    "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Custom": {}
  },
  "Keyword": "Laptops",
  "ClientGuid": "bdeebee3d2b74c8ea58522bb1db61f8e"
}

fetch(url, {
  method: "POST",
  body: JSON.stringify(data),
  headers: new Headers({
    "Content-Type": "application/json",
  }),
})
  .then((res) => res.json())
  .catch((error) => console.error("Error:", error))
  .then((response) => console.log("Success:", response));
"""

"""
let input = {
    method: "POST",
};
let url = "http://localhost:5410/PurchaseReport/GetPlantCode?processType=SA"
let data = await fetch(url)
let result = await data.json()
return result
"""

# ’cp950′ codec can’t decode byte 0xe6 in position 111: illegal multibyte sequence
# See https://www.wongwonggoods.com/all-posts/python/python-debug-error/cp950-codec-python/

# dict to simplenamespace
# See https://stackoverflow.com/questions/50296097/how-to-initialize-a-simplenamespace-from-a-dict

import os
import json
from types import SimpleNamespace


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

# VisitId: cookie hawk_visit_id
# VisitorId: cookie hawk_visitor_id
# ClientGuid: ??

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
    let headers = new Headers({
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    });
    let data = await fetch(url, {
        method: "POST",
        body: JSON.stringify(input),
        headers :headers
    });
    let result = await data.json();
    return result;
"""
