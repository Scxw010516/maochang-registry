import decimal
import numpy as np
# from din import DIN
#筛选部分
#############################################################################################################
#筛选部分

def choose_glass(age,total_weight,facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length):
    #筛选小学生过重的眼镜
    def ch_weight(age,total_weight):
        if age!=None and total_weight != None and age <= 14 and total_weight >= 19:
            return False
        return True
    #舒适度筛选
    def ch_comfort(facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length):
        def cos_sim(a, b):  # 计算余弦相似度
            a_norm = np.linalg.norm(a)
            b_norm = np.linalg.norm(b)
            cos = min(a_norm,b_norm) / max(a_norm,b_norm)
            return cos
        sim1 = cos_sim(facial_width, temporal_width)  # 1.人脸宽与镜架宽的相似度
        sim2 = cos_sim(nose_width, bridge_width)  # 2.人鼻宽与镜架中梁宽的相似度
        sim3 = cos_sim(ear_distance, temple_length)# 3.眼外眦至耳距与镜腿长度的相似度
        return sim1,sim2,sim3
    flag = ch_weight(age,total_weight)
    sim1,sim2,sim3 = ch_comfort(facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length)
    return flag,sim1,sim2,sim3
#筛选部分
#############################################################################################################
