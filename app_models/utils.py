import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .models import Registration
def generate_qr_code(registration: Registration):
    qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=4,
                
            )
    qr.add_data(f'Registration ID: {registration.id}, Name: {registration.first_name} {registration.last_name}, Workshop: {registration.workshop.title}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img = img.resize((350,350), Image.Resampling.LANCZOS)
            
    return img

def generate_registration_badge(instance: Registration):
    name_center = (540, 1085)
    name_text = instance.get_full_name()
    workshop_text = instance.workshop.title
    workshop_center = (540, 650)
    img = Image.open('email_inv.png')
    draw = ImageDraw.Draw(img)

    font_48 = ImageFont.truetype("Roboto-Medium.ttf", 48)
    font_32 = ImageFont.truetype("Roboto-Medium.ttf", 32)

    # Get text width to center it
    name_width = draw.textlength(name_text, font=font_48)

    # Calculate where to start drawing (left edge)
    text_x = name_center[0] - (name_width // 2)
    text_y = name_center[1]
    # Draw the text
    draw.text((text_x, text_y), name_text, fill='black', font=font_48)

    # Draw workshop title
    workshop_width = draw.textlength(workshop_text, font=font_32)
    workshop_x = workshop_center[0] - (workshop_width // 2)
    workshop_y = workshop_center[1]
    draw.text((workshop_x, workshop_y), workshop_text, fill='black', font=font_32)

    qr = generate_qr_code(instance)

    qr_position = (373,1213)
    img.paste(qr, qr_position)
    badge_buffer = BytesIO()
    img.save(badge_buffer, format='PNG')
    badge_buffer.seek(0)  # Move to the beginning of the buffer
    return badge_buffer