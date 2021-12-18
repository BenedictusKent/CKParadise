from PIL import Image, ImageDraw, ImageFont
import random
from demo_new import choice


def pic_design(text):

    img_num = str(random.randrange(1, 2)) #底圖檔名範圍
    #print(img_num)
    img = Image.open(img_num + ".png").convert('RGB')  # 把背景圖轉成RGB格式
    font = ImageFont.truetype('HanaMinA.ttf', 18)  # 設定字型及字體大小
    font_title = ImageFont.truetype('HanaMinA.ttf', 36)  # 設定字型及字體大小
    draw = ImageDraw.Draw(img)

    title = text.split('\n\n')[0]
    hashtag = text.split('\n\n')[1]
    content = text.split('\n\n\n\n')[1]

    draw.text(((img.size[0] / 8), (img.size[1] / 6) + 70), title, font=font_title, fill=(0, 0, 0))
    draw.text(((img.size[0] / 8), (img.size[1] / 6) + 130), hashtag, font=font, fill=(0, 0, 0))
    draw.text(((img.size[0] / 8), (img.size[1] / 6) + 200), content, font=font, fill=(0, 0, 0))

    img.save('menu.png')
    return 'menu.png'


if __name__ == '__main__':
    text = choice('甜', '果香', '檸檬萊姆')
    print(text)
    print(pic_design(text))