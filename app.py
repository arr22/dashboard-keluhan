import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === Load Data ===
df = pd.read_excel('Form IT Helpdesk.xlsx')

# Ubah nama kolom sesuai Excel kamu
df.columns = ["Start Time", "No Tiket", "Nama", "Email", "No HP", "Kategori", "NIK", "Keluhan"]
df["Start Time"] = pd.to_datetime(df["Start Time"])

# === Sidebar Filter ===
st.sidebar.title("Filter Data")
selected_date = st.sidebar.date_input("Pilih Tanggal", datetime.today())

# === Filter Data Berdasarkan Tanggal ===
filtered_df = df[df["Start Time"].dt.date == selected_date]

# === Header ===
st.title("📊 Dashboard Keluhan Harian")
st.write(f"Data untuk tanggal: {selected_date.strftime('%d %B %Y')}")
st.metric("Jumlah Keluhan Hari Ini", len(filtered_df))

# === Pie Chart Jenis Keluhan ===
st.subheader("Distribusi Jenis Keluhan")
jenis_counts = filtered_df["Kategori"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(jenis_counts, labels=jenis_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# === Tabel Detail ===
st.subheader("📋 Tabel Keluhan Hari Ini")
st.dataframe(filtered_df)

# === Grafik Jumlah Harian ===
st.subheader("📈 Grafik Jumlah Keluhan per Hari")
daily_counts = df.groupby(df["Start Time"].dt.date).size()
st.line_chart(daily_counts)
