import os
import time
import json

import torch
from torchvision import transforms
import numpy as np
from PIL import Image
from transforms import letterbox_pil
from src import fcn_resnet50
from typing import Tuple

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class imgResize_solo(object):
    def __init__(self,size:Tuple[int, int]):
        self.max_size = (max(size),max(size))

    def __call__(self, image):
        image=letterbox_pil(image,self.max_size)
        return image

def main():
    aux = False  # inference time not need aux_classifier
    classes = 3
    weights_path = "./save_weights/model_19.pth"
    img_path = "./testdog/1_horizontal.jpg"
    palette_path = "./palette.json"
    assert os.path.exists(weights_path), f"weights {weights_path} not found."
    assert os.path.exists(img_path), f"image {img_path} not found."
    assert os.path.exists(palette_path), f"palette {palette_path} not found."
    with open(palette_path, "rb") as f:
        pallette_dict = json.load(f)
        pallette = []
        for v in pallette_dict.values():
            pallette += v

    # get devices
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))

    # create model
    model = fcn_resnet50(aux=aux, num_classes=classes+1)

    # delete weights about aux_classifier
    weights_dict = torch.load(weights_path, map_location='cpu')['model']
    for k in list(weights_dict.keys()):
        if "aux" in k:
            del weights_dict[k]

    # load weights
    model.load_state_dict(weights_dict)
    model.to(device)

    # load image
    original_img = Image.open(img_path)

    # from pil image to tensor and normalize
    data_transform = transforms.Compose([imgResize_solo((640, 640)),
                                         transforms.ToTensor(),
                                         transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                                              std=(0.229, 0.224, 0.225))])
    img = data_transform(original_img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    model.eval()  # 进入验证模式
    with torch.no_grad():
        # init model
        img_height, img_width = img.shape[-2:]
        init_img = torch.zeros((1, 3, img_height, img_width), device=device)
        model(init_img)

        t_start = time_synchronized()
        output = model(img.to(device))
        t_end = time_synchronized()
        print("inference time: {}".format(t_end - t_start))

        prediction = output['out'].argmax(1).squeeze(0)
        prediction = prediction.to("cpu").numpy().astype(np.uint8)
        mask = Image.fromarray(prediction)
        mask.save("E:/ALLvision/pycharmproject/yoloseg/githubtry/diyFCN/try2_yaml/fcn/testdog/test_result.png")
        mask.putpalette(pallette)
        # mask.save("test_result.png")


if __name__ == '__main__':
    main()
