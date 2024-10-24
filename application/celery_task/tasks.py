from celery import shared_task
import time


@shared_task
def test(x):
    time.sleep(5)
    print('执行完毕')
    return x


#############1.在网页调用接口（上传参数至celery，把计算的函数接进来，然后保存） 2，result.py获取计算结果/进程进展 3.