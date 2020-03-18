from os import path
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from config import Config

import os
import requests

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
    predictions = requests.post(Config.STANFORDNLP_URL, data= data, files=files)

    text = []
    
    ret = predictions.json()
    
    for key in ret :
        for word in ret[key] :
            if word['upos'] == 'NOUN' or word['upos'] == 'PROPN':
                text.append(word['lemma'])

    txt = ' '.join(text)
    
    print(txt)
    print('end post stanfordnlp')
    
    return txt

def generate_word_cloud(out_path, mask_path, text):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    #alice_mask = np.array(Image.open(path.join(d, mask_path)))
    alice_coloring = np.array(Image.open(path.join(d, mask_path)))
    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                max_font_size=40, random_state=42, stopwords=stopwords, contour_width=0, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    image_colors = ImageColorGenerator(alice_coloring)
    wc.recolor(color_func=image_colors)
    # store to file
    wc.to_file(path.join(d, out_path))

def get_ax_size(fig, ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height

def generate_mask(mask_path, jpg_path):
    print('in function generate_mask')
    predictions = post_detectron2(jpg_path)
    polygons = get_polygons(predictions, None)

    img = Image.open(jpg_path)
    img_np = np.array(img)

    print(img_np.shape)
    height, width, _ = img_np.shape

    img_np = np.array([255] * (height * width * 3), dtype=np.uint8)
    img_np = img_np.reshape(height, width, 3)
    
    print(img_np.shape)

    xy = polygons[0]['0']

    fig = plt.figure(figsize=(width/100, height/100))
    ax = plt.subplot()
    ax.imshow(img_np)
    ax.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    fig_width, fig_height = get_ax_size(fig, ax)
    
    ax.add_patch(mpl.patches.Polygon(xy, fill=True, facecolor='k', edgecolor='none', alpha=1.0))
    
    fig.savefig(mask_path, bbox_inches='tight', pad_inches=0, dpi=100*height/fig_height)

def post_detectron2(filepath) :
    files = { 'file' : open(filepath, 'rb')}
    predictions = requests.post(Config.DETECTRON_URL, files=files)

    return predictions.json()

def get_polygons(predictions, className) :
    polygons = []

    for idx in predictions.keys() :
        polygons.append(predictions[idx]['polygons'])

    return polygons
