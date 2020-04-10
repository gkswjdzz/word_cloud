from os import path
from PIL import Image, ImageDraw, ImageColor
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from config import Config

import os
import requests

import time

mpl.use('agg')

def post_stanfordnlp(filepath, lang) :
    """
        input : txt file
        lang : ko => model_version : ko_kaist
    """

    files = { 
        'file' : open(filepath, 'rb')
    }
    data = {
        'model_version' : lang
    }
    start = time.time()
    predictions = requests.post(Config.STANFORDNLP_URL, data= data, files=files)
    print("post stafordnlp time : ", time.time() - start)
    text = []
    
    ret = predictions.json()
    if type(ret) == str :
        return 400
        
    for key in ret :
        for word in ret[key] :
            if word['upos'] == 'NOUN' or word['upos'] == 'PROPN':
                text.append(word['lemma'])

    txt = ' '.join(text)
    
    print('end post stanfordnlp')
    
    return txt

def generate_word_cloud(out_path, result_path, is_colored, text, font_size):
    start = time.time()
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    #alice_mask = np.array(Image.open(path.join(d, mask_path)))
    img = np.array(Image.open(path.join(d, result_path)))
    
    stopwords = set(STOPWORDS)
    stopwords.add("said")
    
    wc = WordCloud(mode="RGBA", background_color=None, max_words=4000, mask=img,
                max_font_size=font_size, random_state=42, stopwords=stopwords, contour_width=0, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    if is_colored is True :
        image_colors = ImageColorGenerator(img)
        wc.recolor(color_func=image_colors)

    # store to file
    wc.to_file(path.join(d, out_path))
    print("generate word cloud time : ", time.time() - start)
    
def get_ax_size(fig, ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height

def generate_mask(is_colored, colored_path, jpg_path, class_name):
    print('in function generate_colored')
    img = Image.open(jpg_path).convert("RGB")

    img_np = np.asarray(img)

    predictions = post_detectron2(jpg_path)
    polygons_list = get_polygons(predictions, class_name)
    colored_img = Image.new('1', (img_np.shape[1], img_np.shape[0]), 0)

    for polygons in polygons_list :
        polygons = polygons['0']
        polygons_tuple = [tuple(x) for x in polygons]

        print(len(polygons_tuple))
        
        ImageDraw.Draw(colored_img).polygon(polygons_tuple, outline=1, fill=1)
    
    colored_np = np.array(colored_img)

    print(np.count_nonzero(colored_np))
    t = time.time()

    if is_colored is False :
        reversal_np = np.where(colored_np, False, True)
        new_img_np = np.full(img_np.shape, 255, dtype='uint8')
        
        new_img_np[:,:,0] = new_img_np[:,:,0] * reversal_np
        new_img_np[:,:,1] = new_img_np[:,:,1] * reversal_np
        new_img_np[:,:,2] = new_img_np[:,:,2] * reversal_np

    else:
        new_img_np = np.empty(img_np.shape, dtype='uint8')

        new_img_np[:,:,:3] = img_np[:,:,:3]

        new_img_np[:,:,0] = new_img_np[:,:,0] * colored_np
        new_img_np[:,:,1] = new_img_np[:,:,1] * colored_np
        new_img_np[:,:,2] = new_img_np[:,:,2] * colored_np
        
        for row in new_img_np:
        	for col in row:
		        if np.all(col==0):
			        col.fill(255)
    print('time : ', time.time() - t)

    newIm = Image.fromarray(new_img_np, "RGB")
    
    width, height = newIm.size
    ratioHW = height/width
    if width > 1200 :
        newIm = newIm.resize((1200, int(1200*ratioHW)))
    print(newIm.size)
    newIm.save(colored_path)

def post_detectron2(filepath) :
    files = { 'file' : open(filepath, 'rb')}
    start = time.time()
    
    predictions = requests.post(Config.DETECTRON_URL, files=files)
    
    print("post detectron2 time : ", time.time() - start)
    
    return predictions.json()

def get_polygons(predictions, class_name) :
    polygons = []

    for idx in predictions.keys() :
        if predictions[idx]['class'] == class_name :
            polygons.append(predictions[idx]['polygons'])

    return polygons
