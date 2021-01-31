from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from PIL import Image
import numpy
import cv2
import requests
import re

app = FastAPI()

apiKeyRegex = r"^dyNotifyApi_([0-9][A-Za-z0-9 -]+)$"
urlRegex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    e = str(exc)
    start, end = e.find("query ->")+len("query ->"), e.find("(type")
    msgErr = e[start:end].strip()
    return JSONResponse(status_code=400, content={"detial": msgErr})


@app.get("/compare-images")
def compare_images(firstImgUrl: str, secondImgUrl: str, apiKey: str = Query(..., max_length=15, regex=apiKeyRegex)):

    try:

        givenImg1 = firstImgUrl
        givenImg2 = secondImgUrl

        # --- Read URLs ---
        if re.match(urlRegex, givenImg1):
            givenImg1 = requests.get(givenImg1, stream=True).raw

        if re.match(urlRegex, givenImg2):
            givenImg2 = requests.get(givenImg2, stream=True).raw

        # --- open images ---
        img1 = Image.open(givenImg1)
        img2 = Image.open(givenImg2)

        # --- make the given images have the same color level and size ---
        img1 = img1.convert("L").resize((400, 400))
        img2 = img2.convert("L").resize((400, 400))

        # --- convert given images to arrays ---
        image1 = numpy.array(img1)
        image2 = numpy.array(img2)

        # --- measure similarity percentage ---
        percentage = cv2.matchTemplate(
            image1, image2, cv2.TM_CCORR_NORMED)[0][0] * 100
        similarityPercentage = round(percentage, 2)
        return {"Similarity Percentage": str(similarityPercentage) + "%"}

    except Exception as err:
        msgErr = str(err)
        if 'cannot identify image' in msgErr:
            msgErr = 'Cannot identify an image at the given URL(s)'
        elif 'No such file' in msgErr:
            msgErr = 'Cannot identify an image at the given local file(s)'
        raise HTTPException(status_code=404, detail=msgErr)
