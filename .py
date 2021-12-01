def create_mask_image(img):
    # cv2.rectangle(img,(0,0),(img.shape[1],img.shape[0]),255,-1)
    im=img.copy()
    im[:,:]=0
    return im

if not os.path.exists('./main_data/unet_annotations'):
    os.mkdir('./main_data/unet_annotations')
    if not os.path.exists('./main_data/unet_annotations/labels'):
        os.mkdir('./main_data/unet_annotations/labels')
    if not os.path.exists('./main_data/unet_annotations/train'):
        os.mkdir('./main_data/unet_annotations/train')

def mask_for_unet(filename,image,mask_image,points,color):
    x,y,w,h=[int(x) for x in points]
    cv2.rectangle(mask_image,(x,y),(x+w,y+h),color,-1)
    mask_image=cv2.resize(mask_image,(512,512),cv2.INTER_AREA)
    image=cv2.resize(image,(512,512),cv2.INTER_AREA)
    cv2.imwrite(f'./main_data/unet_annotations/labels/{filename}.jpg',mask_image)
    cv2.imwrite(f'./main_data/unet_annotations/train/{filename}.jpg',image)
    # cv2.imshow('',mask_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

images=get_images() 
image=''
mask_image=''
points=[]
for i in data:
    # print(i)
    if i.split(':')[0] == 'filename':
        image=images[i.split(':')[1]]
        filename=i.split(':')[1].split('.')[0]
        mask_image=create_mask_image(image)
    else:
        if i.split(":")[0] in ['x','y','width','height']:
            points.append(i.split(":")[1])
        else:
            c=255-int(i.split(":")[0])
            mask_for_unet(filename,image,mask_image,points,[c,c,c]) 
            points=[]