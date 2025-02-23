import streamlit as st
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
import os

# Ensure the temp directory exists
TEMP_DIR = "temp_dir"
os.makedirs(TEMP_DIR, exist_ok=True)  # Create directory if it doesn't exist

def classify_pages(pdf_path):
    """Classify pages as text-only or image-containing."""
    doc = fitz.open(pdf_path)
    text_pages, image_pages = [], []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)  # Extract images

        if images:  
            image_pages.append(page_num)
        else:  
            text_pages.append(page_num)

    return text_pages, image_pages

def split_pdf(pdf_path, text_pages, image_pages, text_output, image_output):
    """Split PDF into text-only and image-containing PDFs."""
    pdf_reader = PdfReader(pdf_path)
    
    text_writer = PdfWriter()
    image_writer = PdfWriter()

    for page_num in text_pages:
        text_writer.add_page(pdf_reader.pages[page_num])

    for page_num in image_pages:
        image_writer.add_page(pdf_reader.pages[page_num])

    # Save new PDFs
    with open(text_output, 'wb') as text_file:
        text_writer.write(text_file)

    with open(image_output, 'wb') as image_file:
        image_writer.write(image_file)

def main():
    st.set_page_config(page_title="PDF Page Separator", layout="centered")
    st.title("📄 PDF Page Separator: Color vs B&W Pages")

    uploaded_file = st.file_uploader("📂 Upload your PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_path = os.path.join(TEMP_DIR, "uploaded.pdf")  # Save in temp directory

        # Save the uploaded file correctly
        try:
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✅ PDF uploaded successfully!")
        except Exception as e:
            st.error(f"🚨 Error saving file: {e}")
            return

        if st.button("🔄 Process PDF"):
            with st.spinner("Processing... Please wait."):
                text_output = os.path.join(TEMP_DIR, "text_pages.pdf")
                image_output = os.path.join(TEMP_DIR, "color_pages.pdf")

                text_pages, image_pages = classify_pages(pdf_path)
                split_pdf(pdf_path, text_pages, image_pages, text_output, image_output)

                st.success(f"✅ Process completed! Found {len(text_pages)} text pages & {len(image_pages)} image pages.")

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="⬇️ Download Black & White PDF",
                        data=open(text_output, "rb"),
                        file_name="text_pages.pdf",
                        mime="application/pdf",
                    )

                with col2:
                    st.download_button(
                        label="⬇️ Download Color PDF",
                        data=open(image_output, "rb"),
                        file_name="color_pages.pdf",
                        mime="application/pdf",
                    )

if __name__ == "__main__":
    main()
