import pickle
import cv2

def load_pkl(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def load_img(file_path):
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Image at {file_path} could not be loaded.")
    return img

def show_points(points, image_path):
    image = load_img(image_path)
    for point in points:
        cv2.circle(image, tuple(point), 5, (0, 255, 0), -1)  # Draw a green circle at each point
    cv2.namedWindow('Points', cv2.WINDOW_NORMAL)
    cv2.imshow("Points", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 递归得到所有列表

def load_points(data,points=[]):
    for key, value in data.items():
        if isinstance(value, list):
            if isinstance(value[0], int):
                points.append(value)
            else:
                points.extend(value)
        elif isinstance(value, dict):
            load_points(value, points)
    return points



if __name__ == "__main__":
    pkl_path = "C:/Downloads/temp/output.pkl"
    img_path = "C:/Downloads/temp/0_rot.jpg"
    data = load_pkl(pkl_path)
    points = data['point']['data']['up']
    points = load_points(points)
    show_points(points, img_path)
    # print(points)