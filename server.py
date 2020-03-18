from flask import Flask, request, flash, send_file
import json
import numpy as np
import matplotlib as mlp
from function import generate_mask, post_stanfordnlp, generate_word_cloud
import uuid

app = Flask(__name__)

@app.route('/image_color', methods= ['POST'])
def image_color():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'file_path not found!'

        if 'text' not in request.files:
            return 'txt_path not found!'
        
        if 'lang' not in request.form :
            return 'lang not found!'
        
        id = str(uuid.uuid4())
        f = request.files['image']
        jpg_path = id + '.jpg'
        f.save(jpg_path)
        
        f = request.files['text']
        txt_path = id + '.txt'
        f.save(txt_path)

        lang = request.form['lang']
        
        print("upload complete!")

        mask_path = id + 'mask.jpg'
        generate_mask(mask_path, jpg_path)
        print(mask_path)

        #post stanfordnlp
        txt = post_stanfordnlp(txt_path, lang)
        
        print('post to stanfordnlp success!')
        
        out_path = id + 'out.png'
        #execute word_cloud
        generate_word_cloud(out_path, mask_path, txt)

        return send_file(out_path, mimetype='image/png')        
    return 'complete'

@app.route('/random_color', methods= ['PUT', 'POST'])
def random_color():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'image not found!'

        if 'text' not in request.files:
            return 'text not found!'
        
        if 'lang' not in request.form :
            return 'lang not found!'
        
        id = str(uuid.uuid4())
        f = request.files['image']
        jpg_path = id + '.jpg'
        f.save(jpg_path)
        
        f = request.files['text']
        txt_path = id + '.txt'
        f.save(txt_path)

        lang = request.form['lang']
        
        print("upload complete!")

        mask_path = id + 'mask.jpg'
        generate_mask(mask_path, jpg_path)
        print(mask_path)

        #post stanfordnlp
        txt = post_stanfordnlp(txt_path, lang)
        
        print('post to stanfordnlp success!')
        
        out_path = id + 'out.png'
        #execute word_cloud
        generate_word_cloud(out_path, mask_path, txt)

        return send_file(out_path, mimetype='image/png')        
    return 'complete'

if __name__ == "__main__" :
    app.run(host='0.0.0.0')