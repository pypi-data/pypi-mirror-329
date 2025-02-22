import os
import base64
import re
import argparse
import shutil
import json
import time
import random
import boto3
from dotenv import load_dotenv
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from datetime import datetime
import re
import string

load_dotenv()

bedrock_client = boto3.client("bedrock-runtime", region_name="ap-south-1")

def encode_image(image_path):
    """Encodes image to base64 format"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ Error encoding image {image_path}: {str(e)}")
        return None

def convert_pdf_to_image(pdf_path, output_folder="temp"):
    """Converts the first two pages of a PDF into images"""
    os.makedirs(output_folder, exist_ok=True)
    

    
    try:
        pdf_reader = PdfReader(pdf_path)
        num_pages = len(pdf_reader.pages)
    except Exception as e:
        print(f"❌ Error reading PDF {pdf_path}: {str(e)}")
        return pdf_path

    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=min(2, num_pages), dpi=150, thread_count=1)
        if not images:
            raise ValueError("No images generated")
        
        image_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(".pdf", ".jpg"))
        images[0].save(image_path, "JPEG")
        return image_path
    except Exception as e:
        print(f"❌ Error converting {pdf_path} to images: {str(e)}")
        return None

def call_bedrock_api(image_path):
    """Calls the Bedrock API to extract invoice details from image"""
    base64_image = encode_image(image_path)
    if not base64_image:
        return None

    prompt = (
        "You are an extremely strict and efficient Invoice Details Extractor. "
        "You will receive an image of an invoice. Your task is to extract exactly three fields: "
        "1. 'Invoice No' - the exact invoice number as it appears; "
        "2. 'Invoice Dt' - the invoice date in the format DD.MM.YYYY (convert it if necessary); "
        "3. 'Supplier Name' - the supplier's name, which must never be 'Safari Exim House Pvt Ltd'.\n\n"
        "Follow these rules strictly:\n"
        "- Output only a JSON object with exactly three keys: 'Invoice No', 'Invoice Dt', and 'Supplier Name'.\n"
        "- Do not include any additional text, explanations, or keys.\n"
        "- Strictly Make sure that you don't add the address in the 'Supplier Name'. It usually starts with FLOOR or FLOOR2 or FLOOR3 strictly make sure u stop extracting 'Supplier Name ' once u encounter these words\n"
        "- Strictly make sure that the 'Invoice No' always starts with actual invoice number and not anything else the actual 'Invoice no' is usually appended by Invoice No: "
        "-Always keep the 'Supplier Name' in capital letters even if it was extracted in small letters"
        "- If any required field is missing or uncertain, return an empty JSON object {}.\n"
        "Respond only with the JSON object without any markdown formatting or extra text."
    )

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }

    retries = 3
    for attempt in range(retries):
        try:
            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            response_body = json.loads(response["body"].read())
            # print("LLM response: ", response_body["content"][0]["text"].strip())
            return response_body["content"][0]["text"].strip()
        except Exception as e:
            print(f"⚠️ Bedrock API error: {str(e)}. Retrying ({attempt+1}/{retries})...")
            time.sleep(2 ** attempt + random.uniform(0, 1))
    
    return None

def extract_invoice_details(extracted_text):
    """Extracts invoice details from JSON response"""
    try:
        data = json.loads(extracted_text)
        if not all(key in data for key in ["Invoice No", "Invoice Dt", "Supplier Name"]):
            return {}
        return data
    except:
        return {}

def get_year_and_month(invoice_date):
    """Extracts year and month from the invoice date"""
    try:
        date_obj = datetime.strptime(invoice_date.strip(), "%d.%m.%Y")
        return date_obj.year, date_obj.strftime("%B").upper()
    except:
        return None, None

# def sanitize_filename(filename):
  
#     filename = re.sub(r'([a-z])([A-Z])', r'\1 \2', filename)
#     filename = re.sub(r'[<>:"/\\|?*]', ' ', filename)
#     filename = filename.replace('-', ' ')
#     return ' '.join(filename.split()).strip()

def sanitize_filename(filename):

    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, ' ', filename)
    filename = re.sub(r'([a-z])([A-Z])', r'\1 \2', filename)
    filename = filename.replace('-', ' ')
    return ' '.join(filename.split()).strip()

def process_subfolder(subfolder_path):
    """Processes all PDFs in a given subfolder"""
    pdf_files = [f for f in os.listdir(subfolder_path) if f.endswith(".pdf")]
    print(f"🔍 Processing {len(pdf_files)} PDFs in {subfolder_path}...")
    error_pdfs = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(subfolder_path, pdf_file)
        try:
            # Convert PDF to image
            image_path = convert_pdf_to_image(pdf_path)
            error_pdfs.append(image_path)
            # print("Error PDFs: ", error_pdfs)
            extracted_text = call_bedrock_api(image_path) if image_path else None
            invoice_details = extract_invoice_details(extracted_text) if extracted_text else {}

            # Extract invoice details
            invoice_no = invoice_details.get("Invoice No", "ERROR")
            invoice_dt = invoice_details.get("Invoice Dt", "01.01.2000")
            supplier_name = invoice_details.get("Supplier Name", "ERROR")

            # Format extracted details
            # formatted_invoice_no = invoice_no.replace("/", "-").replace('"', '').replace(',', '')
            # formatted_supplier = sanitize_filename(supplier_name)
            formatted_invoice_no = sanitize_filename(invoice_no.replace("/", "-").replace('"', '').replace(',', ''))
            formatted_supplier = sanitize_filename(supplier_name)


            # Ensure filenames are within OS limits (truncate long supplier names)
            if len(formatted_supplier) > 50:
                formatted_supplier = formatted_supplier[:50]  # Trim to 50 characters

            # Extract year and month
            year, month = get_year_and_month(invoice_dt)
            if not year or not month:
                year, month = 2000, "UNKNOWN"

            # Define output paths
            output_parent_dir = os.path.join(subfolder_path, "Named")
            os.makedirs(output_parent_dir, exist_ok=True)
            output_dir = os.path.join(output_parent_dir, str(year), month)
            os.makedirs(output_dir, exist_ok=True)

            # Define new PDF file name
            # new_file_name = f"{formatted_invoice_no} {formatted_supplier}.pdf" if "ERROR" not in formatted_invoice_no else "error.pdf"
            # new_pdf_path = os.path.join(output_dir, new_file_name)
            base_name = f"{formatted_invoice_no} {formatted_supplier}"
            new_file_name = f"{base_name}.pdf"
            new_pdf_path = os.path.join(output_dir, new_file_name)

            # Check for duplicates and rename if needed
            counter = 1
            while os.path.exists(new_pdf_path):
                new_file_name = f"{base_name} ({counter}).pdf"
                new_pdf_path = os.path.join(output_dir, new_file_name)
                counter += 1

            # Copy original PDF to the new location
            shutil.copy(pdf_path, new_pdf_path)
            print(f"📂 Saved as {new_file_name} in {output_dir}")

            # Cleanup temporary image file
            if image_path:
                os.remove(image_path)

        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {str(e)}")
            
            # Log the error
            # with open("error_log.txt", "a") as log_file:
            with open("error_log.txt", "a", newline="") as log_file:

                log_file.write(f"{pdf_file}: {str(e)}\n")

            # Ensure the error file is saved no matter what
            year, month = 2000, "UNKNOWN"
            output_parent_dir = os.path.join(subfolder_path, "Named")
            os.makedirs(output_parent_dir, exist_ok=True)
            # output_dir = os.path.join(output_parent_dir, str(year), month)
            from pathlib import Path

            output_dir = Path(output_parent_dir) / str(year) / month
            output_dir.mkdir(parents=True, exist_ok=True)  # Ensures directory creation

            os.makedirs(output_dir, exist_ok=True)

            # Generate unique error filename to prevent overwriting
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            error_pdf_path = os.path.join(output_dir, f"error_{timestamp}.pdf")

            try:
                shutil.copy(pdf_path, error_pdf_path)
                print(f"⚠️ Error file saved as {error_pdf_path}")
            except Exception as e:
                print(f"❌ Failed to save error file for {pdf_file}: {str(e)}")


def process_main_folder(main_folder):
    """Processes all subfolders in the main folder"""
    subfolders = [os.path.join(main_folder, f) for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]
    for subfolder in subfolders:
        print("hello")
        print(f"📂 Processing subfolder: {subfolder}")
        process_subfolder(subfolder)
    print("Processing complete.")

def main():
    parser = argparse.ArgumentParser(description="Extract invoice details from PDFs and organize them.")
    parser.add_argument("main_folder", type=str, nargs="?", default=os.getcwd(), help="Main folder containing subfolders with PDFs")
    args = parser.parse_args()
    process_main_folder(args.main_folder)

if __name__ == "__main__":
    main()
