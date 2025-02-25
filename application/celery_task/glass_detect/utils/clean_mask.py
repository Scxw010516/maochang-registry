import cv2


def remove_small(mask, area=10000):
    temp = mask.copy()
    contours, hierarchy = cv2.findContours(
        temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    contours = [contour for contour in contours if cv2.contourArea(contour) < area]
    cv2.fillPoly(temp, contours, 0)
    return temp


def keep_topk(mask, k=1):
    temp = mask.copy()
    contours, hierarchy = cv2.findContours(
        temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    # print(len(contours))
    contours_small = sorted(contours, key=cv2.contourArea, reverse=True)[
        min(k, len(contours)) :
    ]
    cv2.fillPoly(temp, contours_small, 0)
    return temp


def clean(mask, area=10000, k=1):
    temp = mask.copy()
    temp = remove_small(temp, area=area)
    temp = keep_topk(temp, k=k)
    return temp
