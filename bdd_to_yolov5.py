import os
import json
class BDD_to_YOLOv5:
    def __init__(self):
        self.writepath = "C:/Users/10604/Desktop/dataset/bdd100k/labels_txt/val/" #写入路径，txt文件存放路径
        self.bdd100k_width_ratio = 1.0 / 1280
        self.bdd100k_height_ratio = 1.0 / 720
        self.select_categorys = ["person", "rider", "car", "bus", "truck", "bike","motor"]
        self.categorys_nums = {
            "person": 0,"rider": 1,"car": 2,"bus": 3,"truck": 4,"bike": 5,"motor": 6,
        }
    def bdd_to_yolov5(self, path):
        lines = ""
        with open(path) as fp:
            j = json.load(fp) #加载文件数据
            write = open(self.writepath + "%s.txt" % os.path.basename(path).split('.')[0], 'w') #写入文件，若文件不存在直接创建
            for fr in j["frames"]: #对frame循环
                for objs in fr["objects"]: #对frame内的object循环
                    if objs["category"] in self.select_categorys:
                        temp_category = objs["category"] #获取当前object属性名

                        idx = self.categorys_nums[temp_category] #获取属性名对应数组下标
                        # 中心点坐标
                        cx = (objs["box2d"]["x1"] + objs["box2d"]["x2"]) / 2.0
                        cy = (objs["box2d"]["y1"] + objs["box2d"]["y2"]) / 2.0
                        # 宽和高
                        w = objs["box2d"]["x2"] - objs["box2d"]["x1"]
                        h = objs["box2d"]["y2"] - objs["box2d"]["y1"]

                        if w <= 0 or h <= 0:
                            continue
                        # 根据图片尺寸进行归一化
                        cx, cy, w, h = cx * self.bdd100k_width_ratio, cy * self.bdd100k_height_ratio, w * self.bdd100k_width_ratio, h * self.bdd100k_height_ratio
                        line = f"{idx} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n" #每个对象的信息
                        lines += line #不止一个对象，接着输入

                if len(lines) != 0:
                    write.writelines(lines)
                    write.close()
                    print("%s has been dealt!" % j["name"])

if __name__ == "__main__":
    bdd_labels_dir = "C:/Users/10604/Desktop/dataset/bdd100k/labels/val/" #存放标签文件夹地址
    fileList = os.listdir(bdd_labels_dir) #生成文件列表
    obj = BDD_to_YOLOv5() #类对象
    for path in fileList: #对文件列表循环
        filepath = bdd_labels_dir + path
        print(path)

        obj.bdd_to_yolov5(filepath) 