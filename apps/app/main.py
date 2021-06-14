from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from mangum import Mangum
from pydantic import BaseModel
import boto3
import io
import os
app = FastAPI()

class ImageParam(BaseModel):
    image: str

@app.post("/files/")
def create_file(file: UploadFile = File(...)):
    service_name = "sample-fastapi-2"
    bucket_name = service_name + "-resources-sls-imgageup-uploadimages"
    target_name = os.path.basename(file.filename)
    s3 = boto3.resource('s3')
    contents = file.file.read()
    s3.Bucket(bucket_name).upload_fileobj(io.BytesIO(contents), target_name)
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)

    url = f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{bucket_name}/{target_name}"
    return {"url": url}

@app.get("/form")
async def main():
    content = """
    <html>
    <head>
      <title>FastAPI Form Test</title>
    </head>
    <body>
      <div>files</div>
      <form action="/prod/files/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
      </form>
    </body>
    """
    return HTMLResponse(content=content)

handler = Mangum(app)