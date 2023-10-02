import qrcode
import os
from io import BytesIO

qr_codes_directory = os.path.join(os.path.dirname(__file__), "qr-codes")

def generate_qr_code(table_id):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(table_id)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    image.save(img_bytes_io, format="PNG") # Save as binary data
    os.makedirs(qr_codes_directory, exist_ok=True)
    image.save(f"{qr_codes_directory}/{table_id}.png") # Save to disk

    return img_bytes_io.getvalue()