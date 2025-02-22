# tb-data-collection
淘系店铺数据采集工具

## 安装
```bash
pip install tb-data-collection
```

## 使用方法
### 连接浏览器
```python
from TbDataCollection import Collector

collector = Collector()
collector.connect_browser(port=9527)
collector.login(username='your_username', password='your_password')
```