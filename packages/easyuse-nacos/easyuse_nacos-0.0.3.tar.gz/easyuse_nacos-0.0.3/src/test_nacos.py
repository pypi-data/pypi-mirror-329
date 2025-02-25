import os
from nacos import NacosClient


from easyuse_nacos import NacosConfigProperty, NacosConfig
os.environ['NACOS_SERVER'] = '43.144.249.194:8848'
os.environ['NACOS_NAMESPACE_ID'] = 'dae4701a-dae4-48a0-ab98-fb984cf28be6'
os.environ['NACOS_USERNAME'] = 'AKIDkPyQk9SqQs66sWyCrOhlhQEwVzXx9Zpz'
os.environ['NACOS_PASSWORD'] = '5ybHtGXikbQ6sY8dw2uZq0xhDXcT68pJ'



# client = NacosClient(server_addresses=os.environ['NACOS_SERVER'],
#                      namespace=os.environ['NACOS_NAMESPACE_ID'],
#                      username=os.environ['NACOS_USERNAME'],
#                      password=os.environ['NACOS_PASSWORD'])




if __name__ == '__main__':
    import time

    class MyData(NacosConfig):
        test_key:str= NacosConfigProperty(group='group1')

    while True:
        print(MyData.test_key)
        time.sleep(3)
