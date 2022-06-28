import cv2 as cv
import numpy as np
from PIL import Image


#cv_background_image：貼り付け元の画像（np.ndarray）
#cv_overlay_image：貼り付ける透過素材（np.array）
#point：貼り付け位置（tupple）
def overlay(cv_background_image, cv_overlay_image, point,):
    
    overlay_height, overlay_width = cv_overlay_image.shape[:2]

    # OpenCV形式の画像をPIL形式に変換(α値含む)

    # 背景画像
    #PILで画像を扱うためにRGBからBGRに変換する
    cv_rgb_bg_image = cv.cvtColor(cv_background_image, cv.COLOR_BGR2RGB)
    #変換したPILをarrayに変換
    pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
    #RGBAに変換
    pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')

    # オーバーレイ画像
    #PILで画像を扱うためにRGBからBGRに変換する
    cv_rgb_ol_image = cv.cvtColor(cv_overlay_image, cv.COLOR_BGRA2RGBA)
    #変換したPILをarrayに変換
    pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
    #RGBAに変換
    pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

    # composite()は同サイズ画像同士が必須のため、合成用画像を用意
    pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
                                  (255, 255, 255, 0))
    # 座標を指定し重ね合わせる
    pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
    result_image = \
        Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

    # pilloをnumpy.ndarray形式に変換
    # RGBAをBGRAに変換
    cv_bgr_result_image = cv.cvtColor(
        np.asarray(result_image), cv.COLOR_RGBA2BGRA)

    return cv_bgr_result_image

