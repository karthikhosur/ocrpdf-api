import base64
from fastapi.param_functions import Path
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from subprocess import  Popen
from base64 import b64decode,b64encode

def pdf_ocr(input_pdf, output_pdf):
    p = Popen(["ocrmypdf",input_pdf,output_pdf])
    p.communicate()


class Item(BaseModel):
    base64file: str
    file_name: str

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://185.85.241.50:5500",
    "http://185.85.241.50:8080",
    "https://api.parsinga.com",
    "http://185.85.241.50"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/parsinga_ocr")
async def create_item(item: Item):
    file_data = item.base64file
    filename = item.file_name
    temp_filename = filename
    new_filename = temp_filename
    bytes = b64decode(file_data, validate=True)
    f = open(new_filename, 'wb')
    f.write(bytes)
    f.close()
    input_pdf = new_filename
    output_pdf = "ocr_"+new_filename
    pdf_ocr(input_pdf,output_pdf)
    with open(output_pdf, "rb") as image_file:
        res = (b64encode(image_file.read()))

    return {"response":res}