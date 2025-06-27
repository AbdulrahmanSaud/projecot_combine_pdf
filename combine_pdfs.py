import os
from PyPDF2 import PdfMerger

# Get all PDF files in the current directory, sorted alphabetically
pdf_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.pdf')])

if not pdf_files:
    print("No PDF files found in the current directory.")
else:
    merger = PdfMerger()
    for pdf in pdf_files:
        print(f"Adding: {pdf}")
        merger.append(pdf)
    output_filename = 'combined_output.pdf'
    merger.write(output_filename)
    merger.close()
    print(f"All PDFs combined into {output_filename}") 