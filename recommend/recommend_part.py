import decimal
import time,pymysql
import math
import warnings
import heapq
from choose import choose_glass
from recommend import recommend_glass
warnings.filterwarnings('ignore')
#############################################################################################################
# 各种参数
global userid,sim1_threshold, sim2_threshold, sim3_threshold,table1,table2
userid = -1  # 控制读取的用户，默认-1读取最新的用户信息
sim1_threshold, sim2_threshold, sim3_threshold = 0.75, 0.75, 0.75  # 舒适度的阈值
table1 = 'maochang_eyeglassframerecommandationrequest' #人脸的
table2 = 'maochang_eyeglassframedetectionresult' #镜架的
#############################################################################################################
#############################################################################################################
#数据库部分
# database_name = 'user_glass'
# password = '111111'
# hostname ='localhost'
database_name = 'antdvue'
password = 'P8ssw0rd_'
hostname = '127.0.0.1'
# 打开数据库连接
database = pymysql.connect( host= hostname,
                            user='root',
                            password=password,
                            port=3306,
                            database=database_name,
                            charset='utf8')  # port必须写int类型,MySQL的默认端口为3306. charset必须写utf8
# 创建游标
cursor = database.cursor()

#将数据放入list中
# def get_mysql_list(table_name):
#     # 执行sql语句
#     sql = 'select * from %s ;' % table_name
#     cursor.execute(sql)
#     # 获取到sql执行的全部结果
#     results = cursor.fetchall()
#     table_list = []
#     for r in results:
#         table_list.append(list(r))  # 将其转换为list
#     return list(table_list)  # 返回一个完整的列表数据
#数据库部分
#############################################################################################################

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
def recommend():
    #############################################################################################################
    # 各种参数
    top_K = 0
    #############################################################################################################
    start_time = time.time()

    # 调用得到各个数据集中的数据
    # user_info_list = get_mysql_list('maochang_eyeglassframerecommandationrequest')#用户个人信息表
    sql1 = 'select age,career,facial_width,nose_width,left_ear_distance,lens_weight from %s ;' % table1
    cursor.execute(sql1)
    # 获取到sql执行的全部结果
    results = cursor.fetchall()
    user_info_list = []
    for r in results:
        user_info_list.append(list(r))  # 将其转换为list
    # glass_input_list = get_mysql_list('maochang_eyeglassframedetectionresult')#镜架检测信息表
    # user_info_list
    age    = user_info_list[userid][0]
    career = user_info_list[userid][1]
    # user_face_list
    facial_width = user_info_list[userid][2]
    nose_bridge  = user_info_list[userid][3]
    ear_distance = user_info_list[userid][4]
    # shape        = user_info_list[userid][8]#加东西
    # user_opt_list
    lens_weight = user_info_list[userid][5]

    sql2 = 'select glasses_id, lens_height, temporal_width,bridge_width, temple_length, glasses_weight from %s ;' % table2
    cursor.execute(sql2)
    total_glasses = cursor.rowcount
    # 获取到sql执行的全部结果
    results = cursor.fetchall()
    glass_input_list = []
    for r in results:
        glass_input_list.append(list(r))  # 将其转换为list

    #其他的初始化
    score_list = []
    glasses_id = []
    value = None
    for i in range(total_glasses):
        id_score = dict()
        #获得一个镜架的输入和检测信息
        # glasses_info  = glass_info_list[i]
        glasses_input = glass_input_list[i]
        #glass_input
        glasses_id, lens_height, temporal_width      = glasses_input[0],glasses_input[1], glasses_input[2]
        bridge_width, temple_length, glasses_weight = glasses_input[3], glasses_input[4], glasses_input[5]
        # glasses_shape = glasses_input[10]
        #计算镜架总重量
        if lens_weight == None:
            total_weight = None
        else:
            total_weight = lens_weight+glasses_weight
        total_weight = None
        flag,sim1,sim2,sim3 = choose_glass(age, total_weight, facial_width, temporal_width, nose_bridge, bridge_width, ear_distance,
                     temple_length)
        if flag == True and sim1 > sim1_threshold and sim2 > sim2_threshold and sim3 > sim3_threshold:
            #若符合筛选则立马计算推荐分数
            top_K += 1
            id_score['glasses_id'] = glasses_id
            score = recommend_glass(sim1, sim2, sim3, career, total_weight, temporal_width, lens_height)
            # score,value = recommend_glass(sim1,sim2,sim3,shape,glasses_shape,career,total_weight,temporal_width,lens_height)
            id_score['score'] = float(round(score,3))
            # print(round(score,3))
            score_list.append(id_score)
            # print(score_list)
    ######获得top-K的字典
    # end_time = time.time()
    cursor.close()    # 关闭游标
    database.close()  # 关闭连接
    if score_list == [] and glasses_id != []:
        return glasses_id
    elif score_list == [] and glasses_id ==[]:
        return
    else:
        max_score = heapq.nlargest(1, score_list, key=lambda s: s['score'])[0]['score']
        out_id    = heapq.nlargest(top_K, score_list, key=lambda s: s['score'])  # 按score降序排列
        temp = 0
        for i in range(top_K):
            temp = out_id[i]['score']
            #输出的数值太小时
            out_id[i]['score'] = "%.2f%%" % (math.sqrt((float(temp)/float(max_score)*100))*10)
            # out_id[i]['score'] = "%.2f%%" % ((float(temp) / float(max_score) * 100))
        #####输出推荐结果
        # print(top_K)
        # print(out_id)
        # print('本次推荐所用时间：{}'.format(end_time - start_time))
        return out_id
