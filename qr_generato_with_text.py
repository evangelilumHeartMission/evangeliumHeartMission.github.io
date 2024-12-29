import qrcode
from PIL import Image, ImageDraw, ImageFont

# Configuration
qr_size_mm = 15  # Size of QR code in mm
margin_mm = 2  # Space between QR codes in mm
page_width_mm = 210  # A4 width in mm
page_height_mm = 297  # A4 height in mm
dpi = 300  # Print resolution (dots per inch)
base_url = "https://evangeliumheartmission.github.io/"  # Base URL for the QR codes
text_above = "Scan Me"  # Text to display above each QR code
font_size_mm = 3  # Font size in mm

# Convert sizes to pixels
qr_size_px = int(qr_size_mm * dpi / 25.4)
margin_px = int(margin_mm * dpi / 25.4)
font_size_px = int(font_size_mm * dpi / 25.4)
page_width_px = int(page_width_mm * dpi / 25.4)
page_height_px = int(page_height_mm * dpi / 25.4)

# Calculate grid dimensions (accounting for margins and text space)
cols = (page_width_px + margin_px) // (qr_size_px + margin_px)
rows = (page_height_px + margin_px) // (qr_size_px + margin_px + font_size_px)

# Create a blank image for the sheet
sheet = Image.new("RGB", (page_width_px, page_height_px), "white")
draw = ImageDraw.Draw(sheet)

# Load a font (default system font if specific TTF is not provided)
try:
    font = ImageFont.truetype("arial.ttf", font_size_px)
except IOError:
    font = ImageFont.load_default()

# Generate and place QR codes with text
for row in range(rows):
    for col in range(cols):
        # Generate unique URL for each QR code
        url = f"{base_url}/qr-{row}-{col}"

        # Generate QR code
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size_px, qr_size_px))

        # Calculate positions
        x = col * (qr_size_px + margin_px)
        y = row * (qr_size_px + margin_px + font_size_px)

        # Add text above the QR code
        text_bbox = draw.textbbox((0, 0), text_above, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x + (qr_size_px - text_width) // 2  # Center text above QR code
        text_y = y - text_height - 15  # Position above the QR code with a small gap

        # Draw the text
        draw.text((text_x, text_y), text_above, fill="black", font=font)

        # Paste the QR code
        sheet.paste(qr_img, (x, y))

# Save the result
output_file = "qr_codes_with_text.png"
sheet.save(output_file)
print(f"QR codes sheet with text saved as {output_file}. Ready for printing.")
