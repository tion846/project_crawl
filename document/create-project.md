## 建立 Scrapy 專案

```bat

:: 1.安裝scrapy
pip3 install scrapy

:: 2.建立 scrapy 專案
:: {project} = 專案名稱
scrapy startproject {project}

CD {project}

:: 3.建立 spider
:: {spider} = spider名稱
:: google.com = 初始化目標網址
scrapy genspider {spider} google.com

:: 4.透過指令執行 scrapy
:: {spider} = spider名稱
scrapy crawl {spider}

```

## 執行與除錯-VS Code

- https://docs.scrapy.org/en/latest/topics/debug.html#visual-studio-code
- https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code



