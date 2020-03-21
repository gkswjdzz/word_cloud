from flask import Flask, request, send_file
from function import generate_mask, post_stanfordnlp, generate_word_cloud
import uuid

app = Flask(__name__)

def generate(id, is_colored, out_path, png_path, txt_path, lang) :

    result_path = id + 'mask.png'
    
    generate_mask(is_colored, result_path, png_path)
    print(result_path)

    #post stanfordnlp
    txt = post_stanfordnlp(txt_path, lang)
    
    print('post to stanfordnlp success!')
    
    #execute word_cloud
    generate_word_cloud(out_path, result_path, is_colored, txt)

def upload(files, form, id):
    f = request.files['image']
    png_path = id + '.png'
    f.save(png_path)
    
    f = request.files['text']
    txt_path = id + '.txt'
    f.save(txt_path)

    lang = request.form['lang']    
        
    return png_path, txt_path, lang

@app.route('/random_color', methods= ['POST'])
def random_color():
    if request.method == 'POST':    
        if 'image' not in request.files:
            return 'image not found!'

        if 'text' not in request.files:
            return 'text not found!'
        
        if 'lang' not in request.form :
            return 'lang not found!'
    
        id = str(uuid.uuid4())
        png_path, txt_path, lang = upload(request.files, request.form, id)
        
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, False, out_path, png_path, txt_path, lang)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

@app.route('/image_color', methods= ['POST'])
def image_color():
    if request.method == 'POST':    
        if 'image' not in request.files:
            return 'image not found!'

        if 'text' not in request.files:
            return 'text not found!'
        
        if 'lang' not in request.form :
            return 'lang not found!'
    
        id = str(uuid.uuid4())
        png_path, txt_path, lang = upload(request.files, request.form, id)
        
        print("upload complete!")

        out_path = id + 'out.png'
        generate(id, True, out_path, png_path, txt_path, lang)
        
        return send_file(out_path, mimetype='image/png')        
    return "Record not found", 400

if __name__ == "__main__" :
    app.run(host='0.0.0.0')
    #app.run(debug=True)