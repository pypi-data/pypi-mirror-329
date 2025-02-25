from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class WebPImageField(models.ImageField):
    def __init__(self, *args, quality=90, **kwargs):
        self.quality = quality
        super().__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        super().save_form_data(instance, data)

        if data and not data.name.lower().endswith('.webp'):
            try:
                img = Image.open(data)

                img_io = BytesIO()

                # Preserve transparency if the image has an alpha channel
                if img.mode in ("RGBA", "P"):
                    img.save(img_io, format="WEBP", quality=self.quality, lossless=True)
                else:
                    img.save(img_io, format="WEBP", quality=self.quality)

                webp_filename = f'{data.name.rsplit(".", 1)[0]}.webp'
                webp_file = ContentFile(img_io.getvalue(), webp_filename)

                field = getattr(instance, self.attname)
                field.save(webp_filename, webp_file, save=False)

                setattr(instance, self.attname, webp_file)

            except Exception as e:
                print(f"Error processing image: {e}")
