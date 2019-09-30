from pycocotools.coco import COCO
import requests
import sys
import os


# load coco.names
with open("coco.names") as f:
    data = f.read()
names = data.split('\n')


# check if classes exists
if len(sys.argv) < 2:
    sys.exit(0)
for i in range(1, len(sys.argv)):
    if not sys.argv[i] in names:
        print("ERROR: " + sys.argv[i] + " class doesn't exists")
        sys.exit(0)


# create output directory
if not os.path.exists("./downloaded_images/"):
    os.makedirs("./downloaded_images/")


# load coco annotations
coco = COCO('annotations/instances_train2017.json')
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]


# browse annotations
for index in range (1, len(sys.argv)):
    ind = 0
    print ("Category : " + sys.argv[index])
    catIds = coco.getCatIds(catNms=[sys.argv[index]])
    imgIds = coco.getImgIds(catIds=catIds )
    images = coco.loadImgs(imgIds)
    for im in images:
        print("Category : " + sys.argv[index] + ", " + str(ind) + "/" + str(len(images)) + ", im: ", im)
        print (ind)
        annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        output = open("./downloaded_images/" + im['file_name'].split('.')[0] + ".txt", 'a')
        for i in range(len(anns)):
            output.write(str(index - 1) + " " + " ".join(map(str, anns[i]['bbox'])) + "\n")
        img_data = requests.get(im['coco_url']).content
        with open('downloaded_images/' + im['file_name'], 'wb') as handler:
            handler.write(img_data)
        output.close()
        ind += 1