import requests
import streamlit as st
from utils.exporters import make_txt, make_docx, make_pdf

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
    .main-title { text-align:center; font-size:42px; font-weight:700; }
    .subtitle { text-align:center; color:#777; margin-bottom:25px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)

API_URL = "http://127.0.0.1:8000"

if "document" not in st.session_state:
    st.session_state.document = ""

left, right = st.columns(2)

with left:
    document_type = st.text_input(
        "Document Type",
        placeholder="Employment Contract / NDA / Lease Agreement"
    )
    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Employee), ABC Technologies (Employer)"
    )

with right:
    effective_date = st.text_input(
        "Effective Date",
        placeholder="29 September 2026"
    )
    terms = st.text_area(
        "Terms & Conditions",
        height=150,
        placeholder="Payment within 30 days; Confidentiality must be maintained"
    )

st.caption("Separate multiple terms with semicolons (;).")

if st.button("✨ Generate Document", type="primary", use_container_width=True):
    if not all([document_type.strip(), parties.strip(), terms.strip(), effective_date.strip()]):
        st.warning("Please fill all fields.")
    else:
        with st.spinner("Generating document..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "effective_date": effective_date,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                st.session_state.document = response.json()["document"]
                st.success("Document generated successfully.")
            except requests.exceptions.ConnectionError:
                st.error(
                    "Backend is not running. Run: "
                    "uvicorn backend.main:app --reload"
                )
            except Exception as exc:
                st.error(f"Generation failed: {exc}")

if st.session_state.document:
    st.divider()
    st.subheader("Document Preview")

    edited = st.text_area(
        "Edit the generated document",
        value=st.session_state.document,
        height=500
    )
    st.session_state.document = edited

    st.subheader("Download")
    d1, d2, d3 = st.columns(3)

    d1.download_button(
        "⬇️ Download TXT",
        data=make_txt(edited),
        file_name="legalease_document.txt",
        mime="text/plain",
        use_container_width=True
    )
    d2.download_button(
        "⬇️ Download DOCX",
        data=make_docx(edited, document_type or "Legal Document"),
        file_name="legalease_document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    d3.download_button(
        "⬇️ Download PDF",
        data=make_pdf(edited, document_type or "Legal Document"),
        file_name="legalease_document.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.divider()
st.caption(
    "LegalEase generates drafts for assistance and education. "
    "It is not a substitute for advice from a qualified legal professional."
)
