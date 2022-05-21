import os

from PIL import Image, ImageDraw, ImageFont


def get_concat_h(imgs, resample=Image.BICUBIC):
    images = []
    font = ImageFont.truetype("arial", 30)
    for i in imgs:
        img = Image.open('downloads/images/' + i)
        text = i.split('.')[1]
        ImageDraw.Draw(img).text((10, 10), f'{text}', fill='red', font=font)
        images.append(img)
    min_height = min(im.height for im in images)

    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height), resample=resample) for im in images]

    total_width = sum(im.width for im in im_list_resize)
    print(total_width)
    dst = Image.new('RGB', (int(total_width / 2) + 250, 2 * (min_height + 50)), color='#e1ecf4')

    pos_x, pos_y = 0, 0
    for im in im_list_resize:
        if pos_x < (int(total_width / 2)):
            dst.paste(im, (pos_x + 50, 30))
            pos_x += im.width + 50
        else:
            dst.paste(im, (pos_y + 50, im.height + 60))
            pos_y += im.width + 50
    img_name='downloads/gr_images/gr.'
    for i in imgs:
        img_name += i.split('.')[1]+'_'
    img_name=img_name+'.jpg'
    dst.save(img_name)
    return img_name




def get_gr_photo(keys):
    images = []
    gr_photo_name=''
    for k in keys:
        gr_photo_name += f'{k}_'
    if f'gr.{gr_photo_name}.jpg' in os.listdir('downloads/gr_images'):
        return f'downloads/gr_images/gr.{gr_photo_name}.jpg'
    print('Topilmadi..')
    for file in os.listdir('downloads/images'):
        if int(file.split('.')[1]) in keys:
            images.append(file)
    return get_concat_h(images)