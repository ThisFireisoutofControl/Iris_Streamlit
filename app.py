import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบจำแนกสายพันธุ์ดอก Iris",
    page_icon="🌸",
    layout="wide"
)

# ----------------- ส่วนหัว -----------------
st.title("🌸 แอปพลิเคชันจำแนกสายพันธุ์ดอก Iris ด้วย Machine Learning")
st.markdown("เว็บแอปพลิเคชันสำหรับสำรวจชุดข้อมูล Iris และทำนายสายพันธุ์ดอกไม้โดยใช้โมเดล **Random Forest**")

# ----------------- โหลดข้อมูล & เทรนโมเดล -----------------
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df["target"] = iris.target
    df["species"] = df["target"].map({0: "Setosa", 1: "Versicolor", 2: "Virginica"})
    return df, iris

df, iris_raw = load_data()

@st.cache_resource
def get_model():
    # เทรนโมเดล RandomForest ด้วยพารามิเตอร์ตาม dataset ที่กำหนด
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(iris_raw.data, iris_raw.target)
    return clf

model = get_model()

# ----------------- แถบเมนูด้านข้าง (Sidebar) สำหรับป้อนค่า -----------------
st.sidebar.header("⚙️ กำหนดคุณลักษณะของดอกไม้")
st.sidebar.write("ปรับค่าขนาดของกลีบเพื่อทดสอบทำนาย:")

sepal_length = st.sidebar.slider("Sepal Length (cm)", min_value=4.0, max_value=8.0, value=5.8, step=0.1)
sepal_width = st.sidebar.slider("Sepal Width (cm)", min_value=2.0, max_value=4.5, value=3.0, step=0.1)
petal_length = st.sidebar.slider("Petal Length (cm)", min_value=1.0, max_value=7.0, value=4.3, step=0.1)
petal_width = st.sidebar.slider("Petal Width (cm)", min_value=0.1, max_value=2.6, value=1.3, step=0.1)

user_features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

# ----------------- ส่วนเนื้อหาหลัก -----------------
tab1, tab2, tab3 = st.tabs(["🔮 ทำนายผล (Prediction)", "📊 สำรวจข้อมูล (Data Exploration)", "📋 ดูตารางข้อมูล (Dataset)"])

with tab1:
    st.subheader("ผลการทำนายสายพันธุ์")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**ค่าที่คุณกำหนด:**")
        preview_df = pd.DataFrame(
            user_features,
            columns=["Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"]
        )
        st.dataframe(preview_df, hide_index=True)

        # การทำนายผล
        prediction = model.predict(user_features)[0]
        prediction_proba = model.predict_proba(user_features)[0]
        target_name = iris_raw.target_names[prediction].capitalize()
        
        st.success(f"### ผลการทำนาย: **Iris {target_name}** 🌺")

    with col2:
        st.write("**ความน่าจะเป็นของแต่ละสายพันธุ์:**")
        proba_df = pd.DataFrame({
            "สายพันธุ์": [name.capitalize() for name in iris_raw.target_names],
            "ความน่าจะเป็น (%)": [round(p * 100, 2) for p in prediction_proba]
        })
        st.bar_chart(proba_df.set_index("สายพันธุ์"))

with tab2:
    st.subheader("การกระจายตัวของข้อมูล (Scatter Chart)")
    st.markdown("เปรียบเทียบความสัมพันธ์ระหว่าง **Petal Length** กับ **Petal Width** แยกตามสายพันธุ์:")
    st.scatter_chart(
        data=df,
        x="petal length (cm)",
        y="petal width (cm)",
        color="species"
    )

with tab3:
    st.subheader("ตารางชุดข้อมูล Iris Dataset")
    st.dataframe(df, use_container_width=True)
    st.write(f"จำนวนข้อมูลทั้งหมด: **{len(df)} แถว**")