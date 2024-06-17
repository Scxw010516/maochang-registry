import decimal
#############################################################################################################
#推荐部分
def beauty_recommedation(shape):#输入脸型
    # 美观度推荐
    #对应脸型与镜架形状字典
    beauty_shape = {"big":"square","long":"round","round":"square","small":"round","oval":"middle"}#适合镜架需要进一步探究,"脸型":"眼镜形状"
    beauty_size  = {"big":"big","long":"big","round":"small","small":"small","oval":"middle"}
    value1 = beauty_shape[shape]
    value2 = beauty_size[shape]
    # cat_dict = torch.load('E:\\research\code\\recommendation-system-model-master\DIN\\recommend.pt')
    # for k, v in cat_dict.items():  # k 参数名 v 对应参数值
    #     print(k, v)
    return value1,value2

def comfort_recommendation(sim1,sim2,sim3,total_weight):
    #舒适度推荐
    # def cos_sim(a, b):#计算余弦相似度
    #     a_norm = np.linalg.norm(a)
    #     b_norm = np.linalg.norm(b)
    #     cos = min(a_norm,b_norm)/max(a_norm,b_norm)
    #     return cos
    #sim4 = cos_sim(ear_eyes_height,height) # 4.眼中在镜片中间(耳朵与瞳孔的高度差，桩头高与镜片一半高度的差)
    if total_weight != None:
        if total_weight < 18 :#模糊数学
            weight_relation = 1
        elif total_weight > 38:
            weight_relation = 0
        else:
            weight_relation = 1-(total_weight-18)/20
        return (sim1+sim2+sim3+weight_relation)/4  #总质量的影响还需要调研结果
    else:
        return (sim1+sim2+sim3)/3

def personal_recommendation(career,glasses_scene):
    #个性化推荐
    score = 0
    student_dict = {"A":0.5,"B":0.3,"C":0.2} #还需调研
    work_dict = {"A":0.3,"B":0.5,"C":0.2}
    elderly_dict = {"A":0.2,"B":0.2,"C":0.6}
    sport_dict = {"A":0.5,"B":0.3,"C":0.2}
    if career == "student":
        score = student_dict[glasses_scene]
    elif career == "work":
        score = work_dict[glasses_scene]
    elif career == "elderly":
        score = elderly_dict[glasses_scene]
    elif career == "sport":
        score = sport_dict[glasses_scene]
    return score

# def recommend_glass(sim1,sim2,sim3,shape,glasses_shape,career,total_weight,temporal_width,lens_height):
def recommend_glass(sim1, sim2, sim3, career, total_weight, temporal_width, lens_height):
    score_beauty,score_comfort,score_personal = 0, 0, 0
    weight_beauty,weight_comfort,weight_personal = decimal.Decimal(0.4),decimal.Decimal(0.3),decimal.Decimal(0.3)
    # weight_beauty = decimal.Decimal(weight_beauty)
    #美观度评分
    # if temporal_width > 10 and lens_height > 10:
    #     glasses_size = "big"
    # else:
    #     glasses_size = "small"
    # value1, value2 = beauty_recommedation(shape)
    # score_beauty1, score_beauty2 = 0, 0
    # if glasses_shape == value1 or shape == "oval":
    #     score_beauty1 = 5.0
    # if glasses_size == value2 or shape == "oval":
    #     score_beauty2 = 5.0
    # score_beauty = decimal.Decimal(score_beauty1)+decimal.Decimal(score_beauty2)
    #舒适度评分
    score_comfort = 10 * comfort_recommendation(sim1,sim2,sim3,total_weight)
    #个性化评分
    # score_personal = decimal.Decimal(10.0 * personal_recommendation(career,glasses_scene))
    score = score_beauty * weight_beauty + score_comfort * weight_comfort #不考虑个性化
    # score = score_beauty * weight_beauty + score_comfort * weight_comfort + score_personal * weight_personal
    return score
#推荐部分
#############################################################################################################