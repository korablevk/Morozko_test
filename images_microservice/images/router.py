import shutil

from fastapi import APIRouter, UploadFile

from tasks.tasks import resized_product_picture, remove_background_of_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)


@router.post("/resize_image")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    resized_product_picture.delay(im_path)


@router.post("/remove_bg_image")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"static/images_without_bg/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    remove_background_of_picture.delay(im_path)