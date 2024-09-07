import qrcode


def get_geo_info(request):
    geo_info = {
        "ip": request.META['REMOTE_ADDR'],
        "user_agent": request.META['HTTP_USER_AGENT'],
    }
    return geo_info


def generar_qr(certificado):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(certificado.short_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_with_favicon = superimpose_favicon(
        img)  # función que superpone el favicon
    return img_with_favicon


def superimpose_favicon(qr_img):
    # Código para superponer el favicon en el centro del QR en blanco y negro
    # Lógica para añadir el favicon aquí
    return qr_img
