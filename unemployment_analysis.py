import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. قراءة ملف البيانات (اسم الملف مباشرة عشان يشتغل عند أي حد ينزل المشروع)
file_name = 'Unemployment_Rate_upto_11_2020.csv'

try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    # حل بديل لو المشرف بيجرب المسار الكامل بتاع جهازك
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else '.'
    df = pd.read_csv(os.path.join(current_dir, file_name))

# 2. تنظيف أسامي الأعمدة من أي مسافات زيادة
df.columns = df.columns.str.strip()

# 3. تحويل عمود التاريخ لنوع تاريخ حقيقي واستخراج اسم الشهر
df['Date'] = pd.to_datetime(df['Date'].str.strip(), format='%d-%m-%Y')
df = df.sort_values('Date')
df['Month_Name'] = df['Date'].dt.strftime('%B')

# 4. حساب متوسطات البطالة شهرياً وحسب المنطقة (باستخدام Region.1)
monthly_avg = df.groupby('Month_Name', sort=False)['Estimated Unemployment Rate (%)'].mean()
area_avg = df.groupby('Region.1')['Estimated Unemployment Rate (%)'].mean()

print("--- المتوسطات العامة للبطالة حسب المنطقة ---")
print(area_avg)

# --- الرسومات البيانية (Data Visualization) ---

# الرسمة الأولى: تأثير كورونا على مدار شهور سنة 2020 (Line Plot)
plt.figure(figsize=(10, 5))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', linestyle='-', color='red', linewidth=2)
plt.title('Unemployment Rate Trend in 2020 (Covid-19 Impact)', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Unemployment Rate (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# الرسمة الثانية: مقارنة معدل البطالة بين الأقاليم (Bar Plot)
plt.figure(figsize=(8, 5))
plt.bar(area_avg.index, area_avg.values, color=['#86bf91', '#a7c5eb', '#f9d5bb', '#f6a5c0'], width=0.5)
plt.title('Average Unemployment Rate by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Average Unemployment Rate (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
