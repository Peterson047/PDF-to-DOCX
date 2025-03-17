import streamlit as st
from pdf2docx import Converter
import os
import tempfile

st.title('Conversor de PDF para DOCX 📄➡️📘')

# Configurações da página
st.markdown("""
<style>
    .st-emotion-cache-18ni7ap {
        background-color: #2a2a2a;
    }
    h1 {
        color: #4a90e2;
        text-align: center;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #357abd;
    }
</style>
""", unsafe_allow_html=True)

def convert_pdf_to_docx(input_pdf, output_docx):
    try:
        cv = Converter(input_pdf)
        cv.convert(output_docx)
        cv.close()
        return True
    except Exception as e:
        st.error(f"Erro na conversão: {str(e)}")
        return False

def main():
    uploaded_file = st.file_uploader("Carregue seu arquivo PDF", type=['pdf'])
    
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Salvar PDF temporário
            pdf_path = os.path.join(temp_dir, "input.pdf")
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Preparar caminho para o DOCX
            docx_path = os.path.join(temp_dir, "output.docx")
            
            # Converter e mostrar progresso
            with st.spinner('Convertendo... Isso pode levar alguns segundos'):
                success = convert_pdf_to_docx(pdf_path, docx_path)
            
            if success:
                st.success("Conversão concluída com sucesso!")
                
                # Botão de download
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                
                st.download_button(
                    label="Baixar arquivo DOCX",
                    data=docx_bytes,
                    file_name="documento_convertido.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
                # Visualização rápida do conteúdo (opcional)
                if st.checkbox("Mostrar prévia do texto convertido"):
                    with open(docx_path, "rb") as f:
                        # Nota: Esta prévia é básica, para uma melhor visualização seria necessário parsear o DOCX
                        st.text(f.read().decode(errors='replace'))

if __name__ == "__main__":
    main()