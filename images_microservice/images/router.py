import shutil
import os
from pathlib import Path

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from rembg import remove

from tasks.tasks import resized_product_picture, remove_background_of_picture
from tasks.celery_app import celery_app


os.environ["FORCE_CELERYD_POOL"] = "threads"
Path("static/images").mkdir(parents=True, exist_ok=True)
Path("static/images_without_bg").mkdir(parents=True, exist_ok=True)


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)


@router.post("/resize_image")
async def resize_image(name: int, file: UploadFile):
    im_path = f"static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    resized_product_picture.delay(im_path)
    return {"message": "Файл успешно загружен и передан на обработку."}


@router.post("/remove_bg_image")
async def remove_bg_image(name: int, file: UploadFile):
    im_path = f"static/images_without_bg/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    remove_background_of_picture.delay(im_path)
    return {"message": "Файл успешно загружен и передан на обработку."}


@router.get("/download_resized_image/{name}")
async def download_resized_image(name: str):
    file_path = Path(f"static/images/resized_477_477_{name}.webp")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(file_path, media_type="image/webp", filename=f"resized_477_477_{name}.webp")


@router.get("/download_removed_bg_image/{name}")
async def download_removed_bg_image(name: str):
    file_path = Path(f"static/images_without_bg/without_bg_{name}.webp")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(file_path, media_type="image/webp", filename=f"without_bg_{name}.webp")
