import qrcode

file_names = ['esl1', 'esl2', 'esl3']

for file in file_names:
    qr_data = "http://10.200.15.40:5000/" + file

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # QR code version (controls the size and error correction level)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code
        border=4,  # Border size around the QR code
    )

    # Add data to the QR code instance
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image object from the QR code instance
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    qr_image.save("output_qr_codes/qr_code_" + file + ".png")
