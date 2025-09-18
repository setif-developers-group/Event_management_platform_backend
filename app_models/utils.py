import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .models import Registration , Workshop, Partner, Speaker
import pandas as pd
import csv
import io
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
    except_headers = ['title', 'description', 'date', 'duration', 'speaker', 'partner']

    for row in read_values_from_file(file,except_headers):
        partner = Partner.objects.filter(name=row['partner']).first()
        if partner is None and row['partner'] is not None:
            partner = Partner.objects.create(name=row['partner'])
        speaker = Speaker.objects.filter(name=row['speaker']).first()
        if speaker is None and row['speaker'] is not None:
            speaker = Speaker.objects.create(name=row['speaker'])
        Workshop.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'description': row['description'],
                        'date': row['date'],
                        'duration': row['duration'],
                        'speaker': speaker,
                        'partner': partner,
                    }
                )


    return

def create_speakers_from_file(file):
    except_headers = ['name', 'bio','partner']

    for row in read_values_from_file(file,except_headers):
        partner = Partner.objects.filter(name=row['partner']).first()
        if partner is None and row['partner'] is not None:
            partner = Partner.objects.create(name=row['partner'])
        Speaker.objects.get_or_create(name=row['name'], bio=row['bio'], partner=partner)
    return

def create_partners_from_file(file):
    except_headers = ['name','short_description', 'website']
    for row in read_values_from_file(file,except_headers):
        Partner.objects.get_or_create(name=row['name'],
                                    defaults={'short_description': row['short_description'], 
                                              'website': row['website']})


    return