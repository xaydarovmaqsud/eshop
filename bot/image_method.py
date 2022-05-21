

# #Read the two images
# image1 = Image.open('downloads/images/img_3.jpg')
# image2 = Image.open('downloads/images/img_4.jpg')
# #resize, first image
# image1 = image1.resize((426, 240))
# image1_size = image1.size
# image2_size = image2.size
# new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
# new_image.paste(image1,(0,0))
# new_image.paste(image2,(image1_size[0],0))
# new_image.save('hozir.jpg')


# import numpy as np
# import PIL
# from PIL import Image
#
# list_im = ['downloads/images/img_3.jpg', 'downloads/images/img_4.jpg', 'downloads/images/img_9.jpg']
# imgs = [PIL.Image.open(i) for i in list_im]
# # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
# min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
# imgs_comb = np.hstack([np.asarray(i.resize(min_shape)) for i in imgs])
#
# # save that beautiful picture
# imgs_comb = PIL.Image.fromarray(imgs_comb)
# imgs_comb.save('Trifecta.jpg')
#
# # for a vertical stacking it is simple: use vstack
# imgs_comb = np.vstack([np.asarray(i.resize(min_shape)) for i in imgs])
# imgs_comb = PIL.Image.fromarray(imgs_comb)
# imgs_comb.save('Trifecta_vertical.jpg')
# from PIL.ImageDraw import ImageDraw


from PIL import Image, ImageDraw, ImageFont


def get_image_resize(im_list, resample=Image.BICUBIC):
    images=[]
    font = ImageFont.truetype("arial", 30)
    for i in im_list:
        img = Image.open('downloads/images/'+i)
        text=i.split('.')[0].split('_')[-1]
        ImageDraw.Draw(img).text((10, 10), f'{text}', fill='red',font=font)
        images.append(img)
    min_height = min(im.height for im in images)

    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height), resample=resample) for im in images]

    total_width = sum(im.width for im in im_list_resize)
    print(total_width)
    dst = Image.new('RGB', (int(total_width/2)+250,2*(min_height+50)),color='#e1ecf4')

    pos_x, pos_y = 0, 0
    for im in im_list_resize:
        if pos_x<(int(total_width/2)):
            dst.paste(im, (pos_x+50, 30))
            pos_x += im.width + 50
        else:
            dst.paste(im, (pos_y+50, im.height+60))
            pos_y += im.width + 50
    return dst

imgs=['img_3.jpg','img_4.jpg','img_9.jpg','img_12.jpg','img_13.jpg','img_27.jpg']

get_image_resize(imgs).save('concat_001.jpg')
