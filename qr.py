from flask import render_template, redirect, request, flash
import qrcode
from datetime import datetime

#@app.route('/generate-codes/<table_id>')
def generate_qr_code(table_id):
    if is_valid_table(table_id):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(table_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('static/qr_codes/{}.png'.format(table_id))
        return render_template('qr_code.html', table_name=table_identifiers[table_id])
    else:
        flash('Invalid table identifier. Please try again.', 'danger')
        return redirect('/')