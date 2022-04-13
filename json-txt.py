import json
# 数据集中包含的10个类别
categorys = ['car', 'bus', 'person', 'bike', 'truck', 'motor', 'train', 'rider', 'traffic sign', 'traffic light']
# 图片的分辨率
picture_width = 1282
picture_height = 720


def parseJson(jsonFile):
    '''
      params:
        jsonFile -- BDD00K数据集的一个json标签文件
      return:
        返回一个列表的列表，存储了一个json文件里面的方框坐标及其所属的类，
    '''
    objs = []
    obj = []
    info = jsonFile
    name = info['name']
    objects = info['labels']
    for i in objects:
        if (i['category'] in categorys):
            obj.append(int(i['box2d']['x1']))
            obj.append(int(i['box2d']['y1']))
            obj.append(int(i['box2d']['x2']))
            obj.append(int(i['box2d']['y2']))
            obj.append(i['category'])
            objs.append(obj)
            obj = []
    return name, objs


# test
file_handle = open('traindata.txt', mode='a')
f = open("/home/violet/Documents/dataset/bdd100k/label/train/bdd100k_labels_images_train.json")  # json文件的绝对路径，换成自己的
info = json.load(f)
objects = info
n = len(objects)


# 将左上右下坐标转换成 中心x,y以及w  h
def bboxtrans(box_x_min, box_y_min, box_x_max, box_y_max):
    x_center = (box_x_min + box_x_max) / (2 * picture_width)
    y_center = (box_y_min + box_y_max) / (2 * picture_height)
    width = (box_x_max - box_x_min) / (2 * picture_width)
    height = (box_y_max - box_y_min) / (2 * picture_height)
    return x_center, y_center, width, height


for i in range(n):
    an = ""
    name, result = parseJson(objects[i])
    an = "./data/custom/images/train/" + name  # 这里我改成了图片的相对路径
    for j in range(len(result)):
        cls_id = categorys.index(result[j][4])
        x, y, w, h = bboxtrans(result[j][0], result[j][1], result[j][2], result[j][3])
        an = an + ' ' + str(cls_id) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
    an = an + '\n'
    file_handle.write(an)
    print(len(result))
    print(an)

