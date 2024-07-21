import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

# Retrieve API key from environment variable
API_KEY = os.getenv('AIzaSyB6AEvWfOh4c7-HpwD3QwPrklDG2snPhPg')
if not API_KEY:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    # Configure the API key
    genai.configure(api_key=API_KEY)

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    elif file.name.endswith('.json'):
        return pd.read_json(file)
    else:
        st.error("Unsupported file format. Please upload a CSV, Excel, or JSON file.")
        return None

def analyze_column(df, column):
    col_type = df[column].dtype
    unique_count = df[column].nunique()
    missing_count = df[column].isnull().sum()
    
    analysis = {
        "type": str(col_type),
        "unique_count": unique_count,
        "missing_count": missing_count,
    }
    
    if pd.api.types.is_numeric_dtype(col_type):
        analysis["mean"] = df[column].mean()
        analysis["median"] = df[column].median()
        analysis["std"] = df[column].std()
        analysis["min"] = df[column].min()
        analysis["max"] = df[column].max()
        analysis["outliers"] = df[column][np.abs(df[column] - df[column].mean()) > 3 * df[column].std()].count()
    elif pd.api.types.is_string_dtype(col_type):
        analysis["most_common"] = df[column].value_counts().index[0]
    elif pd.api.types.is_datetime64_any_dtype(col_type):
        analysis["min_date"] = df[column].min()
        analysis["max_date"] = df[column].max()
    
    return analysis

def suggest_analysis(column_name, analysis):
    suggestions = []
    
    if analysis["type"].startswith("int") or analysis["type"].startswith("float"):
        suggestions.append("Histogram แสดงการกระจายตัวของข้อมูล")
        suggestions.append("Box plot เพื่อดู outliers")
        if analysis["unique_count"] < 10:
            suggestions.append("Bar plot แสดงความถี่ของแต่ละค่า")
    
    elif analysis["type"] == "object":
        if analysis["unique_count"] < 10:
            suggestions.append("Bar plot แสดงความถี่ของแต่ละหมวดหมู่")
        else:
            suggestions.append("Word cloud สำหรับข้อมูลประเภทข้อความ")
    
    elif analysis["type"].startswith("datetime"):
        suggestions.append("Time series plot เพื่อดูแนวโน้มตามเวลา")
        suggestions.append("Heatmap แสดงความถี่ตามวัน/เดือน/ปี")
    
    if "id" in column_name.lower():
        suggestions.append("ตรวจสอบความซ้ำซ้อนของ ID")
    
    if "date" in column_name.lower() or "time" in column_name.lower():
        suggestions.append("วิเคราะห์ความถี่ตามช่วงเวลา (รายวัน/สัปดาห์/เดือน)")
    
    if "price" in column_name.lower() or "cost" in column_name.lower() or "revenue" in column_name.lower():
        suggestions.append("วิเคราะห์แนวโน้มและการเปลี่ยนแปลงของราคา/ต้นทุน/รายได้")
    
    return suggestions

def generate_summary(text):
    # Create a GenerativeModel instance
    model = genai.GenerativeModel(name='gemini-pro')
    response = model.generate_content(prompt=text)
    return response.text

def main():
    st.title("Automated EDA Tool")
    
    uploaded_file = st.file_uploader("Choose a CSV, Excel, or JSON file", type=["csv", "xlsx", "xls", "json"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            st.success("Data loaded successfully!")
            
            st.header("Data Overview")
            st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            st.write(df.head())
            
            st.header("Data Types")
            st.write(df.dtypes)
            
            st.header("Missing Values")
            missing_data = df.isnull().sum()
            st.write(missing_data[missing_data > 0])
            
            st.header("Duplicate Rows")
            duplicate_data = df.duplicated().sum()
            st.write(f"Number of duplicate rows: {duplicate_data}")
            
            st.header("Column Analysis")
            for column in df.columns:
                st.subheader(f"Column: {column}")
                analysis = analyze_column(df, column)
                st.write(analysis)
                
                suggestions = suggest_analysis(column, analysis)
                st.write("Suggested analyses:")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
                
                if pd.api.types.is_numeric_dtype(df[column].dtype):
                    fig, ax = plt.subplots()
                    df[column].hist(ax=ax)
                    plt.title(f"Histogram of {column}")
                    st.pyplot(fig)
                
                elif pd.api.types.is_string_dtype(df[column].dtype) and analysis["unique_count"] < 10:
                    fig, ax = plt.subplots()
                    df[column].value_counts().plot(kind='bar', ax=ax)
                    plt.title(f"Bar plot of {column}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                
                st.write("---")
            
            st.header("Correlation Analysis")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
                plt.title("Correlation Heatmap")
                st.pyplot(fig)
            else:
                st.write("ไม่มีคอลัมน์ตัวเลขเพียงพอสำหรับการวิเคราะห์สหสัมพันธ์")
            
            st.header("Additional Analysis Suggestions")
            st.write("1. ตรวจสอบความสัมพันธ์ระหว่างคอลัมน์ที่น่าสนใจ")
            st.write("2. วิเคราะห์แนวโน้มตามเวลาสำหรับคอลัมน์ที่เกี่ยวข้องกับวันที่")
            st.write("3. สร้าง scatter plot ระหว่างคอลัมน์ตัวเลขที่อาจมีความสัมพันธ์กัน")
            st.write("4. ใช้เทคนิค dimensionality reduction เช่น PCA เพื่อหาความสัมพันธ์ที่ซ่อนอยู่")
            st.write("5. ทำการ clustering เพื่อหากลุ่มข้อมูลที่มีลักษณะคล้ายกัน")

            # Generate and display summary
            st.header("Summary")
            summary_text = generate_summary("Summarize the EDA analysis results of the dataset.")
            st.write(summary_text)

if __name__ == "__main__":
    main()
