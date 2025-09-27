import qrcode
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .models import Registration , Workshop, Partner, Speaker
import pandas as pd
import csv
import io
import textwrap

def generate_qr_code(registration: Registration):
    data = {
        "registration_id": registration.id,
        "name": f"{registration.first_name} {registration.last_name}",
        "workshop": registration.workshop.title,
    }
    json_data = json.dumps(data)
    qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=4,
                
            )
    qr.add_data(json_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img = img.resize((350,350), Image.Resampling.LANCZOS)
            
    return img

def draw_multiline_text_centered(draw, text, center_pos, font, max_chars=51, fill='black'):
    """
    Draw text centered, with automatic line wrapping if text exceeds max_chars
    """
    # Split text if too long
    if len(text) > max_chars:
        lines = textwrap.wrap(text, width=max_chars)
    else:
        lines = [text]
    
    # Calculate positioning
    line_height = font.size + 5  # Add some spacing between lines
    total_height = len(lines) * line_height
    start_y = center_pos[1] - (total_height // 2)
    
    # Draw each line centered
    for i, line in enumerate(lines):
        line_width = draw.textlength(line, font=font)
        line_x = center_pos[0] - (line_width // 2)
        line_y = start_y + (i * line_height)
        draw.text((line_x, line_y), line, fill=fill, font=font)

def generate_registration_badge(instance: Registration):
    name_center = (540, 1085)
    name_text = instance.get_full_name()
    workshop_text = instance.workshop.title
    workshop_center = (540, 655)
    
    img = Image.open('email_inv.png')
    draw = ImageDraw.Draw(img)
    font_48 = ImageFont.truetype("Roboto-Medium.ttf", 48)
    font_32 = ImageFont.truetype("Roboto-Medium.ttf", 32)
    
    # Draw name (you might want to wrap long names too)
    name_width = draw.textlength(name_text, font=font_48)
    text_x = name_center[0] - (name_width // 2)
    text_y = name_center[1]
    draw.text((text_x, text_y), name_text, fill='black', font=font_48)
    
    # Draw workshop title with automatic wrapping
    draw_multiline_text_centered(
        draw=draw,
        text=workshop_text,
        center_pos=workshop_center,
        font=font_32,
        max_chars=51,  # Adjust this value as needed
        fill='black'
    )
    
    # Add QR code
    qr = generate_qr_code(instance)
    qr_position = (373, 1213)
    img.paste(qr, qr_position)
    
    badge_buffer = BytesIO()
    img.save(badge_buffer, format='PNG')
    badge_buffer.seek(0)  # Move to the beginning of the buffer
    return badge_buffer

def ckeck_headers(headers,expected_headers: list[str]):
    return all(header in headers for header in expected_headers)

def read_values_from_file(file,expected_headers: list[str]):
    file_bytes = file.read()
    filename = file.name.lower()
    if filename.endswith('.csv'):
        return yield_values_from_csv_file(file_bytes,expected_headers)
    elif filename.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb', '.ods')):
        return yield_values_from_xlsx_file(file_bytes,expected_headers)
    
def yield_values_from_csv_file(file_bytes, expected_headers: list[str]):
    ''' 
    Yields values from a file "
    '''
    file_obj = io.StringIO(file_bytes.decode('utf-8'))
    reader = csv.DictReader(file_obj)
    if ckeck_headers(reader.fieldnames,expected_headers):
        for row in reader:
            yield row
    else:
        raise ValueError("File headers do not match expected headers")
def yield_values_from_xlsx_file(file_bytes, expected_headers: list[str]):
    ''' 
    Yields values from a xlsx file binary
    '''
    df = pd.read_excel(file_bytes)
    df = df.where(pd.notnull(df), None)
    if ckeck_headers(df.columns,expected_headers):
        for index, row in df.iterrows():
            yield row.to_dict()
    else:
        raise ValueError("File headers do not match expected headers")

def create_workshops_from_file(file):
    except_headers = ['title', 'description', 'date', 'duration','week','sessions', 'speaker', 'partner']

    for row in read_values_from_file(file,except_headers):
        if row['partner']:
            partner = Partner.objects.filter(name=row['partner'].strip()).first()
        else:
            partner = None
        if partner is None and row['partner'] is not None:
            partner = Partner.objects.create(name=row['partner'].strip())
        speakers = row['speaker'].split(',') if row['speaker'] else []
        speaker = None
        speakers_ids = []
        for speaker_name in speakers:
            speaker = Speaker.objects.filter(name=speaker_name.strip()).first()
            if speaker is None:
                speaker = Speaker.objects.create(name=speaker_name.strip(), bio="Bio not provided", partner=partner)
            speakers_ids.append(speaker.id)
        workshop = Workshop.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'description': row['description'],
                        'date': row['date'],
                        'duration': row['duration'],
                        'partner': partner,
                        'week': row['week'] if row['week'] is not None else 1,
                        'sessions': row['sessions'] if row['sessions'] is not None else row['duration']
                    }
                )
        workshop[0].speakers.set(speakers_ids)

    return

def create_speakers_from_file(file):
    except_headers = ['name', 'bio','partner', 'contact']

    for row in read_values_from_file(file,except_headers):
        partner = Partner.objects.filter(name=row['partner']).first()
        if partner is None and row['partner'] is not None:
            partner = Partner.objects.create(name=row['partner'])
        Speaker.objects.get_or_create(name=row['name'], bio=row['bio'], partner=partner, contact=row['contact'])
    return

def create_partners_from_file(file):
    except_headers = ['name','short_description', 'website']
    for row in read_values_from_file(file,except_headers):
        Partner.objects.get_or_create(name=row['name'],
                                    defaults={'short_description': row['short_description'], 
                                              'website': row['website']})


    return

def create_certificate(registration: Registration):
    ...

def create_certificates(workshop: Workshop):
    regisrtations:list[Registration] = workshop.registrations.all()
    for registration in regisrtations:
        if not registration.certificate and registration.is_confirmed and (registration.attendances.count() >= (workshop.sessions * 0.8)):
            yield registration

def create_workshop_certificates(workshop: Workshop):
    for registration in create_certificates(workshop):
        create_certificate(registration)    

