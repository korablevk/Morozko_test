from pathlib import Path

from PIL import Image
from rembg import remove

from tasks.celery_app import celery_app


@celery_app.task
def resized_product_picture(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((477, 477))
    im_resized_1000_500.save(f"static/images/resized_477_477_{im_path.name}")


@celery_app.task
def remove_background_of_picture(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_removed_bg = remove(im)
    im_removed_bg.save(f"static/images_without_bg/without_bg_{im_path.name}")


