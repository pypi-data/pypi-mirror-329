from PIL.Image import Transpose, Resampling
from PIL import Image, ImageDraw, ImageFont

image = "bmp"

def crop_image(input_file, output_file, left, top, right, bottom):
    """图像裁剪"""
    try:
        image = Image.open(input_file)
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(output_file, 'bmp')
        image.close()
        cropped_image.close()
    except Exception as e:
        print(f"图像裁剪过程中出现错误: {e}")


def convert_image(input_file, output_file):
    """图像格式转换"""
    try:
        image = Image.open(input_file)
        image.save(output_file, 'bmp')
        image.close()
    except Exception as e:
        print(f"图像格式转换过程中出现错误: {e}")


def add_watermark(input_file, output_file, text):
    """添加文字水印"""
    try:
        image = Image.open(input_file)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        width, height = image.size
        text_width, text_height = draw.textsize(text, font=font)
        position = (width - text_width - 10, height - text_height - 10)
        draw.text(position, text, fill=(255, 255, 255), font=font)
        image.save(output_file, 'bmp')
        image.close()
    except Exception as e:
        print(f"图像添加水印过程中出现错误: {e}")


def rotate_image(input_file, output_file, angle):
    """图像旋转"""
    try:
        image = Image.open(input_file)
        rotated_image = image.rotate(angle, expand=True)
        rotated_image.save(output_file, 'bmp')
        image.close()
        rotated_image.close()
    except Exception as e:
        print(f"图像旋转过程中出现错误: {e}")


def flip_image(input_file, output_file, flip_type):
    """图像翻转"""
    try:
        image = Image.open(input_file)
        if flip_type == 'horizontal':
            flipped_image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
        elif flip_type == 'vertical':
            flipped_image = image.transpose(Transpose.FLIP_TOP_BOTTOM)
        else:
            print("不支持的翻转类型，请输入 'horizontal' 或 'vertical'。")
            return
        flipped_image.save(output_file, 'bmp')
        image.close()
        flipped_image.close()
        print(f"图像 {flip_type} 翻转成功，保存为 {output_file}")
    except Exception as e:
        print(f"图像翻转过程中出现错误: {e}")

        
def resize_image(input_file, output_file, width, height):
    """图像缩放"""
    try:
        image = Image.open(input_file)
        resized_image = image.resize((width, height), Resampling.LANCZOS)
        resized_image.save(output_file, 'bmp')
        image.close()
        resized_image.close()
    except Exception as e:
        print(f"图像缩放过程中出现错误: {e}")