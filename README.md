[![Run on Ainize](https://ainize.ai/static/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=github.com/gkswjdzz/word_cloud)

# Word Cloud

This repository provides API server that generate word cloud using object detection and natural language processing.

## How to Deploy

### docker run

```
docker pull gkswjdzz/word-cloud
docker run -p 80:5000 -it gkswjdzz/word-cloud
```

api server will be running on http://localhost.

## How to Query
<!--

<img src="/images/image1-1.png" width="700" />

First, select language that you are trying to use. Actually, this is pretrained UD NLP models from stanfordnlp. 

then, select the text file that will be words of cloud.

finally, select the image file that will be shape of cloud.

<img src="/images/image3.png" width="700" />

Wait a few seconds, the results come back.
<!--
### On Local
```
curl -X POST "http://localhost/image-color" -H "accept: image/*" -H "Content-Type: multipart/form-data" -d "model_treebank={languages_treebank} sentences={sentences}"
```

You can see the detail of models for human languages from [here](https://stanfordnlp.github.io/stanfordnlp/models.html).
-->
## References

[word_cloud](https://github.com/amueller/word_cloud)