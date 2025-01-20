import streamlit as st
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def convert_image_to_pdf(uploaded_file):
    # Create a bytes buffer for the PDF
    pdf_buffer = io.BytesIO()
    
    # Create the PDF object using reportlab
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Get the width and height of the letter page size
    width, height = letter
    
    # Create PIL Image from uploaded file
    image_data = uploaded_file.getvalue()
    img = Image.open(io.BytesIO(image_data))
    
    # Convert image to RGB if it's in RGBA mode
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Save as temporary PNG in memory
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Get image aspect ratio
    aspect = img.width / img.height
    
    # Calculate new dimensions to fit on the page while maintaining aspect ratio
    if aspect > 1:
        new_width = width - 40  # Leave 20px margin on each side
        new_height = new_width / aspect
    else:
        new_height = height - 40  # Leave 20px margin on top and bottom
        new_width = new_height * aspect
    
    # Calculate positioning to center the image
    x = (width - new_width) / 2
    y = (height - new_height) / 2
    
    # Draw the image on the PDF
    try:
        file_path = os.path.join(os.getcwd(), "temp_image.png")
        with open(file_path, 'wb') as f:
            f.write(img_buffer.getvalue())
        
        c.drawImage(file_path, x, y, new_width, new_height)
        c.save()
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        
    except Exception as e:
        # Make sure to clean up even if an error occurs
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e
    
    # Get the value of the BytesIO buffer
    pdf_buffer.seek(0)
    return pdf_buffer

def health_check():
    return {"status": "healthy"}

def main():
    st.title("Image to PDF Converter")
    st.write("Upload an image to convert it to PDF")
    if st.sidebar.button('Health Check'):
        st.json(health_check())
    
    # Add a container for error messages
    error_container = st.empty()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Convert button
            if st.button("Convert to PDF"):
                with st.spinner("Converting image to PDF..."):
                    pdf_buffer = convert_image_to_pdf(uploaded_file)
                    
                    # Create download button
                    st.success("Conversion successful!")
                    st.download_button(
                        label="Download PDF",
                        data=pdf_buffer,
                        file_name="converted.pdf",
                        mime="application/pdf"
                    )
                    
        except Exception as e:
            error_container.error(f"An error occurred: {str(e)}")
#test change
# Add this route to your app.py

#comments added now
if __name__ == '__main__':
    main()