import numpy as np
import math
import heapq
from application.glass_management import models

#sim1_threshold, sim2_threshold, sim3_threshold = 0.5, 0.5, 0.5
sim1_threshold, sim2_threshold, sim3_threshold = 0.0, 0.0, 0.0
def recommend(age, career, facial_width,  nose_width, left_ear_distance, lens_weight):
    top_K = 0
    nose_bridge  = nose_width
    ear_distance = left_ear_distance
    lens_weight = lens_weight
    glass_input_list = models.EyeglassFrameDetectionResult.objects.all()
    score_list = []
    glasses_id = []
    for glasses_input in glass_input_list:
        id_score = dict()
        glasses_id = glasses_input.entry.id
        lens_height = glasses_input.lens_height
        temporal_width  = glasses_input.temporal_width
        bridge_width = glasses_input.bridge_width
        temple_length = glasses_input.temple_length
        glasses_weight = glasses_input.glasses_weight
        if lens_weight == None:
            total_weight = None
        else:
            total_weight = lens_weight+glasses_weight
        total_weight = None
        flag, sim1, sim2, sim3 = choose_glass(age, total_weight, facial_width, temporal_width, nose_bridge, bridge_width, ear_distance,
                     temple_length)
        #print(flag, sim1, sim2, sim3)
        if flag == True and sim1 > sim1_threshold and sim2 > sim2_threshold and sim3 > sim3_threshold:
            top_K += 1
            id_score['glasses_id'] = glasses_id
            score = recommend_glass(sim1, sim2, sim3, career, total_weight, temporal_width, lens_height)
            id_score['score'] = float(round(score,3))
            score_list.append(id_score)
    if score_list == [] and glasses_id != []:
        return glasses_id
    elif score_list == [] and glasses_id ==[]:
        return
    else:
        max_score = heapq.nlargest(1, score_list, key=lambda s: s['score'])[0]['score']
        out_id    = heapq.nlargest(top_K, score_list, key=lambda s: s['score'])
        temp = 0
        for i in range(top_K):
            temp = out_id[i]['score']
            out_id[i]['score'] = "%.2f%%" % (math.sqrt((float(temp)/float(max_score)*100))*10)
        return out_id

# import decimal

def beauty_recommedation(shape):
    beauty_shape = {"big":"square","long":"round","round":"square","small":"round","oval":"middle"}#适合镜架需要进一步探究,"脸型":"眼镜形状"
    beauty_size  = {"big":"big","long":"big","round":"small","small":"small","oval":"middle"}
    value1 = beauty_shape[shape]
    value2 = beauty_size[shape]
    return value1,value2

def comfort_recommendation(sim1,sim2,sim3,total_weight):
    if total_weight != None:
        if total_weight < 18 :
            weight_relation = 1
        elif total_weight > 38:
            weight_relation = 0
        else:
            weight_relation = 1-(total_weight-18)/20
        return (sim1+sim2+sim3+weight_relation)/4
    else:
        return (sim1+sim2+sim3)/3

def personal_recommendation(career,glasses_scene):
    score = 0
    student_dict = {"A":0.5,"B":0.3,"C":0.2}
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

def recommend_glass(sim1, sim2, sim3, career, total_weight, temporal_width, lens_height):
    score_beauty,score_comfort = 0, 0
    weight_beauty,weight_comfort = 0.4, 0.3
    score_comfort = 10 * comfort_recommendation(sim1,sim2,sim3,total_weight)
    score = score_beauty * weight_beauty + score_comfort * weight_comfort
    return score

def choose_glass(age,total_weight,facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length):
    def ch_weight(age,total_weight):
        if age!=None and total_weight != None and age <= 14 and total_weight >= 19:
            return False
        return True
    def ch_comfort(facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length):
        def cos_sim(a, b):
            a_norm = np.linalg.norm(a)
            b_norm = np.linalg.norm(b)
            cos = float(min(a_norm,b_norm)) / float(max(a_norm,b_norm))
            return cos
        sim1 = cos_sim(facial_width, temporal_width)
        sim2 = cos_sim(nose_width, bridge_width)
        sim3 = cos_sim(ear_distance, temple_length)
        return sim1,sim2,sim3
    flag = ch_weight(age,total_weight)
    sim1,sim2,sim3 = ch_comfort(facial_width,temporal_width,nose_width,bridge_width,ear_distance,temple_length)
    return flag,sim1,sim2,sim3



