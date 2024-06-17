"""
文件结构：
- migrations 文件夹：由Django自动生成（修改数据表后，在项目根目录下使用python manger.py makemigrations即可更新）
- admin.py: Django所属，用于注册ORM类/数据库表信息
- forms.py: 表单验证类，用于验证前端传入的数据
- models.py: 配合admin.py，定义数据库的表结构
- apps.py: Django所属，无需改动
- data_import.py: 包含了一些导入黄晨同学之前扫描的镜架的数据的代码
- recommend.py: 推荐算法部分，由弋羽同学维护
- service.py: 接口所使用的服务函数
- urls.py: 后端路由
- utils.py: 工具函数
- views.py: 后端请求接口
"""