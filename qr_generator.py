import qrcode
from PIL import Image, ImageDraw

# Configuration
qr_size_mm = 15  # Size of QR code in mm
margin_mm = 2  # Space between QR codes in mm
page_width_mm = 210  # A4 width in mm
page_height_mm = 297  # A4 height in mm
dpi = 300  # Print resolution (dots per inch)
base_url = "https://evangeliumheartmission.github.io/"  # Base URL for the QR codes

# Convert sizes to pixels
qr_size_px = int(qr_size_mm * dpi / 25.4)
margin_px = int(margin_mm * dpi / 25.4)
page_width_px = int(page_width_mm * dpi / 25.4)
page_height_px = int(page_height_mm * dpi / 25.4)

# Calculate grid dimensions (accounting for margins)
cols = (page_width_px + margin_px) // (qr_size_px + margin_px)
rows = (page_height_px + margin_px) // (qr_size_px + margin_px)

# Create a blank image for the sheet
sheet = Image.new("RGB", (page_width_px, page_height_px), "white")
draw = ImageDraw.Draw(sheet)

# Generate and place QR codes
for row in range(rows):
    for col in range(cols):
        # Generate unique URL for each QR code
        url = f"{base_url}"

        # Generate QR code
        qr = qrcode.QRCode(box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size_px, qr_size_px))

        # Calculate position with margin
        x = col * (qr_size_px + margin_px)
        y = row * (qr_size_px + margin_px)

        # Ensure the QR code fits within the page
        if x + qr_size_px <= page_width_px and y + qr_size_px <= page_height_px:
            sheet.paste(qr_img, (x, y))

# Save the result
output_file = "qr_codes_sheet_with_urls.png"
sheet.save(output_file)
print(f"QR codes sheet saved as {output_file}. Ready for printing.")
