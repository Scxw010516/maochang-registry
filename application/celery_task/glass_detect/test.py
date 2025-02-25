import cv2

from calculate.front_calculator import FrontCalculator
from calculate.left_calculator import LeftCalculator
from calculate.up_calculator import UpCalculator
from detect.left_detector import LeftDetector
from detect.up_detector import UpDetector
from preprocess.front_preprocessor import FrontPreprocessor
from preprocess.left_preprocessor import LeftPreprocessor
from preprocess.nose_preprocessor import NosePreprocessor
from preprocess.up_preprocessor import UpPreprocessor
from segment.frame_segmentor import FrameSegmentor
from segment.templeWf_segmentor import TempleWfSegmentor
from segment.temple_segmentor import TempleSegmentor
from segment.lens_segmentor import LensSegmentor
from segment.nose_segmentor import NoseSegmentor
from utils.clean_mask import clean
from utils.get_front import get_front
from visualize.front_visualize import FrontVisualizer
from visualize.left_visualize import LeftVisualizer
from visualize.up_visualize import UpVisualizer
from convert.params_converter import ParamsConverter


# fc = FrontCalculator()


def get_capture(sku=""):
    up_image = cv2.imread(f"./image/capture/{sku}_0.jpg")
    front_image = cv2.imread(f"./image/capture/{sku}_1.jpg")
    left_image = cv2.imread(f"./image/capture/{sku}_2.jpg")

    return up_image, front_image, left_image


def main():
    sku = "201300053024730500"
    up_image, front_image, left_image = get_capture(sku)

    # preprocess
    up, fp, lp, nep = (
        UpPreprocessor(up_image),
        FrontPreprocessor(front_image),
        LeftPreprocessor(left_image),
        NosePreprocessor(front_image),
    )
    up_preprocess_image = up.preprocess()
    front_preprocess_image = fp.preprocess()
    left_preprocess_image = lp.preprocess()
    nose_preprocess_image = nep.preprocess()
    # print(up_preprocess_image.shape)
    # print(front_preprocess_image.shape)
    # print(left_preprocess_image.shape)
    # segment
    fs = FrameSegmentor(device="cuda")
    frame_mask = fs.segment(front_preprocess_image, is_one=False)
    ls = LensSegmentor(device="cuda")
    lens_mask = ls.segment(front_preprocess_image, is_one=False)
    ns = NoseSegmentor(device="cuda")
    nose_mask = ns.segment(nose_preprocess_image, is_one=False)
    tws = TempleWfSegmentor(device="cuda")
    templeWf_mask = tws.segment(left_preprocess_image, is_one=False)

    # ## 后处理（去除小的mask，只保留大的）
    frame_mask = clean(frame_mask, area=10000, k=1)
    lens_mask = clean(lens_mask, area=10000, k=2)
    templeWf_mask = clean(templeWf_mask, area=10000, k=1)

    ## 获取前景
    front_mask, frame_type = get_front(frame_mask, lens_mask)  # 镜框类型
    foreground = front_preprocess_image.copy()
    foreground[front_mask == 0] = [0, 0, 0]

    # detect
    ud = UpDetector(device="cuda")
    ld = LeftDetector(device="cuda")
    #
    up_points = ud.detect(up_preprocess_image)
    left_points = ld.detect(left_preprocess_image)
    # print(left_points)
    # print(up_points)

    # 计算参数
    fc = FrontCalculator(frame_image=frame_mask, lens_image=lens_mask)
    lc = LeftCalculator(keypoints=left_points)
    uc = UpCalculator(keypoints=up_points)

    front_points = fc.get_points()
    front_parameters = fc.get_parameters()
    left_points = lc.get_points()
    left_parameters = lc.get_parameters()
    up_points = uc.get_points()
    up_parameters = uc.get_parameters()

    front_visualize_image = fc.get_rotated_image(front_image)
    left_visualize_image = lc.get_rotated_image(left_image)
    up_visualize_image = uc.get_rotated_image(up_image)

    fv = FrontVisualizer(
        image=front_visualize_image, points=front_points, parameters=front_parameters
    )
    lv = LeftVisualizer(
        image=left_visualize_image, points=left_points, parameters=left_parameters
    )
    uv = UpVisualizer(
        image=up_visualize_image, points=up_points, parameters=up_parameters
    )

    front_visualize_image = fv.visualize_parameters()
    left_visualize_image = lv.visualize_parameters()
    up_visualize_image = uv.visualize_parameters()

    # 计算尺寸
    pc = ParamsConverter({**front_parameters, **left_parameters, **up_parameters})
    sizes = pc.convert()
    print(sizes)
    # print(front_points)
    # print(left_points)
    # print(up_points)
    # print(front_parameters)
    # print(left_parameters)
    # print(up_parameters)

    cv2.imwrite(f"./image/visualize/{sku}_front.jpg", front_visualize_image)
    cv2.imwrite(f"./image/visualize/{sku}_left.jpg", left_visualize_image)
    cv2.imwrite(f"./image/visualize/{sku}_up.jpg", up_visualize_image)
    # cv2.imwrite(f"./image/postprocess/{sku}_frame.png", frame_mask)
    # # cv2.imwrite(f"./image/postprocess/{sku}_temple.png", temple_mask)
    # cv2.imwrite(f"./image/postprocess/{sku}_lens.png", lens_mask)
    # cv2.imwrite(f"./image/postprocess/{sku}_nose.png", nose_mask)
    # cv2.imwrite(f"./image/postprocess/{sku}_templeWf.png", templeWf_mask)
    # cv2.imwrite(f"./image/postprocess/{sku}_front.png", front_mask)
    # cv2.imwrite(f"./image/postprocess/{sku}_foreground.png", foreground)

    # cv2.imwrite(f"./image/visualize/{sku}_pre.png", front_painted_image)

    # cv2.imwrite(f"./image/preprocess/{sku}_0.jpg", up_preprocess_image)
    # cv2.imwrite(f"./image/preprocess/{sku}_1.jpg", front_preprocess_image)
    # cv2.imwrite(f"./image/preprocess/{sku}_2.jpg", left_preprocess_image)


if __name__ == "__main__":
    main()
