import io
from flask import Flask, jsonify, request
from PIL import Image
from flask_cors import CORS, cross_origin
import os
import json
import base64
import sys


# import modules
# computer vision
#  from imageClassification import classifier

from imageClassification.predict import image_predict

# recommendation system
from contentbasedMovieRec import contentbased

# style transfer
#  from styletransfer import transfer

app = Flask(__name__)
CORS(app)


@app.route("/")
def imageClassification():
    return "landing page"


#  @app.route("/imageCls", methods=["POST"])
#  def imagefunc():
#      content = request.get_json(force=True, silent=True)
#      print("content:", content)
#      if request.method == "POST":
#          img = content["imageFile"]  # get blob
#          print(type(img))
#          #  print("img", img)
#          imgdata = base64.b64decode(img)
#          filename = "local_image.jpg"
#          with open(filename, "wb") as f:
#              f.write(imgdata)
#          image = Image.open("local_image.jpg")
#          image = classifier.transforms_test(image).unsqueeze(0).to(classifier.device)
#
#          class_name = classifier.imagepredict(image)
#          print("result:", {"class_name": class_name})
#          os.remove("./local_image.jpg")
#          return jsonify({"class_name": class_name})


@app.route("/imageCls", methods=["POST"])
def imagefunc():
    content = request.get_json(force=True, silent=True)

    if request.method != "POST":
        return "통신 오류!!"

    try:
        img = content["imageFile"]
        img = base64.b64decode(img)
        buf = io.BytesIO(img)
        img = Image.open(buf)

        class_name = image_predict(img)

        return jsonify({"class_name": class_name})

    except KeyError:
        return "이미지를 넣어주세요!!!"


@app.route("/contentbasedMovieRec", methods=["POST"])
def contentbasedMovieRec():
    content = request.get_json(force=True, silent=True)
    title = content["title"]
    year = content["year"]
    input = title + " (" + year + ")"
    if request.method == "POST":
        res = contentbased.moviepredict(input)
        print("result:", res)
        return jsonify(res)


import base64


@app.route("/styletransfer", methods=["POST"])
def styleTransfer():
    content = request.get_json(force=True, silent=True)
    print("content: ", content)
    print("images", content["image1"], content["image2"])
    img1 = content["image1"]
    img2 = content["image2"]
    if request.method == "POST":
        transfer.transfer(img1, img2)
        data = {}
        with open(
            "/root/tmp/deep-learning-project-platform-pythonserver/output123.png",
            mode="rb",
        ) as image_file:
            img_ = image_file.read()
        data["img_"] = base64.encodebytes(img_).decode("utf-8")
        return jsonify(data)


if (__name__) == "__main__":
    app.run(host="0.0.0.0", port=80)
