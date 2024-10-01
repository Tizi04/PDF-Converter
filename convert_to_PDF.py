from docx2pdf import convert
from PIL import Image
from fpdf import FPDF
from io import BytesIO
import os
import tempfile

def convertir_a_PDF(file_in_memory, filename):
    try:

        output = BytesIO()

        if filename.endswith('.docx'):

            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
                temp_docx.write(file_in_memory.getvalue())
                temp_docx_path = temp_docx.name

            temp_pdf_path = temp_docx_path.replace(".docx", ".pdf")

            convert(temp_docx_path, temp_pdf_path)

            with open(temp_pdf_path, "rb") as temp_pdf:
                output.write(temp_pdf.read())

            os.remove(temp_docx_path)
            os.remove(temp_pdf_path)

        elif filename.endswith(('.jpg', '.jpeg', '.png')):  

            image = Image.open(file_in_memory)
            image.save(output, "PDF")

        elif filename.endswith('.txt'):

            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_txt:
                temp_txt.write(file_in_memory.getvalue())
                temp_txt_path = temp_txt.name

            pdf = FPDF()
            pdf.add_page()

            with open(temp_txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()  

                    if len(line) <= 10:
                        pdf.set_font("Arial", "B", size=19)
                        pdf.multi_cell(w=0, h=10, txt=line, align="L")
                    else:
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(w=0, h=10, txt=line, align="L")

            
            temp_pdf_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            pdf.output(temp_pdf_path.name)  

            temp_pdf_path.close()

            
            with open(temp_pdf_path.name, "rb") as temp_pdf:
                output.write(temp_pdf.read())  

            os.remove(temp_txt_path)  
            os.remove(temp_pdf_path.name)  

        else:
            print("Unsupported file type")
            return False

        output.seek(0)   
        return output    
    
    except Exception as e:
        print(f"Error during conversion: {e}")  
        return False  
