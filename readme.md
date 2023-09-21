# scrapy

## create project

```bat
:: 1.Install package
pip3 install scrapy
pip3 install selenium
pip3 install scrapy-selenium

:: 2.Create scrapy project
scrapy startproject {project}

CD {project}

:: 3.Gengerate py
scrapy genspider {file} localhost

```

## using package
- scrapy (BSD-3) [https://docs.scrapy.org/en/latest/](https://docs.scrapy.org/en/latest/)
- selenium (Apache-2.0) [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)
- scrapy-selenium [https://github.com/clemfromspace/scrapy-selenium](https://github.com/clemfromspace/scrapy-selenium)


## vscode debugging setting
- [https://docs.scrapy.org/en/latest/topics/debug.html](https://docs.scrapy.org/en/latest/topics/debug.html)
- [https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code](https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code)



## storeApp webApi
### 所有產品清單
- https://essearchapi-na.hawksearch.com/api/v2/search
  - request

```python
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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
opts = Options()
driver = webdriver.Chrome(options=opts)
driver.get(url)
result = driver.execute_script(js_script)

print(result)

```

  - response
```json
{
    "Results": [
        {
            "DocId": "3074457345620733324",
            "Document": {
                "pdp_url": [
                    "https://www.hp.com/us-en/shop/pdp/hp-envy-laptop-17-cr1087nr"
                ],
                "list_price": [
                    "1249.99"
                ],
                "sale_price": [
                    "899.99"
                ],
                "product_name": [
                    "HP Envy Laptop 17-cr1087nr"
                ],
            }
        }
    ],
    "Pagination": {
        "NofResults": 305,
        "CurrentPage": 1,
        "MaxPerPage": 24,
        "NofPages": 13,
    },
}
```

### 產品詳細資料
- https://www.hp.com/us-en/shop/app/api/web/graphql/page/{product_pdp_url_su}/async
  - 產品: https://www.hp.com/us-en/shop/pdp/omen-gaming-laptop-16t-wf000-161-76w27av-1
  - 產品詳細: https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fomen-gaming-laptop-16t-wf000-161-76w27av-1/async
- response

```json
{
    "data": {
        "page": {
            "pageComponents": {
                    "technical_specifications": [
                        {
                            "name": "Operating system",
                            "tooltip": "",
                            "value": [
                                {
                                    "value": "Windows 11 Home",
                                    "subheading": "Included in Current Configuration"
                                },
                                {
                                    "value": "Windows 11 Home\u003Cbr/\u003EWindows 11 Pro\u003Cbr/\u003EWindows 11 Pro",
                                    "subheading": "Alternate Options"
                                }
                            ]
                        },
                        {
                            "name": "Processor and graphics",
                            "tooltip": "",
                            "value": [
                                {
                                    "value": "Intel\u00AE Core\u2122 i5-13500H (up to 4.7 GHz, 18 MB L3 cache, 12 cores, 16 threads) + NVIDIA\u00AE GeForce RTX\u2122 3050 Laptop GPU (6 GB)",
                                    "subheading": "Included in Current Configuration"
                                },
                                {
                                    "value": "Intel\u00AE Core\u2122 i7-13700H (up to 5.0 GHz, 24 MB L3 cache, 14 cores, 20 threads) + NVIDIA\u00AE GeForce RTX\u2122 4050 Laptop GPU (6 GB)",
                                    "subheading": "Alternate Options"
                                }
                            ]
                        },
                        {
                            "name": "Chipset",
                            "tooltip": "",
                            "value": [
                                {
                                    "value": [
                                        "Intel\u00AE integrated SoC"
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "Memory",
                            "tooltip": "",
                            "value": [
                                {
                                    "value": "16 GB DDR5-5200 MHz RAM (2 x 8 GB)",
                                    "subheading": "Included in Current Configuration"
                                },
                                {
                                    "value": "32 GB DDR5-5200 MHz RAM (2 x 16 GB)",
                                    "subheading": "Alternate Options"
                                }
                            ]
                        },
                        {
                            "name": "Storage",
                            "tooltip": "",
                            "value": [
                                {
                                    "value": "512 GB PCIe\u00AE NVMe\u2122 TLC M.2 SSD (4x4 SSD)",
                                    "subheading": "Included in Current Configuration"
                                },
                                {
                                    "value": "1 TB PCIe\u00AE NVMe\u2122 TLC M.2 SSD (4x4 SSD)\u003Cbr/\u003E2 TB PCIe\u00AE NVMe\u2122 TLC M.2 SSD (4x4 SSD)",
                                    "subheading": "Alternate Options"
                                }
                            ]
                        },
                    ]
            }
        }
    }
}
```