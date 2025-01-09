import logging
from pathlib import Path
from PIL import Image
from rembg import remove
from tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def resized_product_picture(self, path: str):
    try:
        im_path = Path(path)
        if not im_path.exists():
            raise FileNotFoundError(f"Файл {im_path} не найден!")

        im = Image.open(im_path)
        im_resized_477_477 = im.resize((477, 477))
        output_path = Path(f"static/images/resized_477_477_{im_path.name}")
        im_resized_477_477.save(output_path)
        logger.info(f"Файл успешно обработан: {output_path}")
    except Exception as exc:
        logger.error(f"Ошибка при обработке файла {path}: {exc}")
        self.retry(exc=exc)


@celery_app.task(bind=True)
def remove_background_of_picture(self, path: str):
    try:
        im_path = Path(path)
        if not im_path.exists():
            raise FileNotFoundError(f"Файл {im_path} не найден!")

        im = Image.open(im_path)
        im_removed_bg = remove(im)
        output_path = Path(f"static/images_without_bg/without_bg_{im_path.name}")
        im_removed_bg.save(output_path, format="WEBP")
        logger.info(f"Файл успешно обработан: {output_path}")
    except Exception as exc:
        logger.error(f"Ошибка при обработке файла {path}: {exc}")
        self.retry(exc=exc)
