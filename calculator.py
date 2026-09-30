import streamlit as st

st.title("🧮 เครื่องคิดเลขอย่างง่าย")

col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("ใส่ตัวเลขที่ 1", value=0.0, format="%.2f")
with col2:
    num2 = st.number_input("ใส่ตัวเลขที่ 2", value=0.0, format="%.2f")

operation = st.selectbox("เลือกเครื่องหมาย", ["+", "-", "× (คูณ)", "÷ (หาร)"])

if st.button("คำนวณ"):
    if operation == "+":
        res = num1 + num2
    elif operation == "-":
        res = num1 - num2
    elif operation == "× (คูณ)":
        res = num1 * num2
    elif operation == "÷ (หาร)":
        if num2 != 0:
            res = num1 / num2
        else:
            res = "ไม่สามารถหารด้วยศูนย์ได้"

    st.success(f"ผลลัพธ์: {res}")