import PyPDF2
import ocrmypdf
import openai
import hide
import ast


openai.api_key = hide.api_key
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

def generate_response(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Попробуй распознать фичи товара из этого текста, текст был распознан OCR, некоторые символы могли быть повреждены или пропущены, попробуй их восстановить. Представь ответ ввиде dict python {'фича': 'знчение', и т.д } Дай ответ только в виде словаря"},
                  {"role": "assistant", "content": "Конечно, вы можете предоставить мне текст, и я постараюсь помочь вам распознать фичи товара и восстановить возможно поврежденные символы."},
                  {"role": "user", "content": text}
                  ]
    )
    return completion.choices[0].message.content


def extract_dict_from_text(text):
    cleaned_text = text.strip()
    dictionary = ast.literal_eval(cleaned_text)
    return dictionary



file_name = "ТП_13М.pdf"
file_path = f"D:\\DATASET\\Хакатон_v2.0\\Паспорта\\{file_name}"
output_patch = f"D:\\DATASET\\Хакатон_v2.0\\Результат{file_name}"

# text = extract_text(file_path, output_patch)
text = extract_text_from_pdf(file_path)

output = generate_response(text)

result = extract_dict_from_text(output)

print(result)



