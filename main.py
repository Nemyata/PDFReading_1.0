import PyPDF2
import ocrmypdf

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text(file_path, output_patch):
    text = extract_text_from_pdf(file_path)
    if text == '':
        ocrmypdf.ocr(file_path, output_patch, language='rus')
        extracted_text = extract_text_from_pdf(output_patch)
        return extracted_text
    else:
        extracted_text = extract_text_from_pdf(file_path)
        return extracted_text


file_name = "ОЛ-004.pdf"
file_path = f"D:\\DATASET\\Хакатон_v2.0\\Паспорта\\{file_name}"
output_patch = f"D:\\DATASET\\Хакатон_v2.0\\Результат{file_name}"

print(extract_text(file_path, output_patch))



