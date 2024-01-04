import ddddocr
def get_code_by_img(imgname):
    """
     #通过验证码的图片获取验证码
    :param imgname: 验证码图片的位置
    :return: 字符串
    """
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(imgname, 'rb') as f:
        img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res