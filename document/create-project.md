## 建立 Scrapy 專案

```bat

:: 1.安裝scrapy
pip3 install scrapy

:: 2.建立 scrapy 專案
:: 專案名稱: project_demo
scrapy startproject project_demo

CD project_demo

:: 3.建立爬蟲 spider
:: spider名稱: demo
:: 目標網址: google.com
scrapy genspider demo google.com

:: 4.使用指令執行 scrapy spider
scrapy crawl demo

```

## 執行與除錯-VS Code
- 啟動vs code
- 執行與偵錯 (Ctrl + Shift + D)
- 新增組態...
- 模組輸入: scrapy
- vs code 自動產生檔案: ```.vscode/launch.json```
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Launch Spider",
            "type": "python",
            "request": "launch",
            "module": "scrapy",
            "args": [
                "runspider",
                "${file}"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

- https://docs.scrapy.org/en/latest/topics/debug.html#visual-studio-code
- https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code
