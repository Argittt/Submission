import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

st.title("Analisis Penggunaan Layanan Bike Sharing Berdasarkan Jam dan Hari")

def create_usage_by_hour_df(df):
    if {'cnt_hours', 'casual_hours', 'registered_hours', 'hr'}.issubset(df.columns):
        usage_by_hour = df.groupby(by="hr").agg({
            "cnt_hours": "sum",
            "casual_hours": "sum",
            "registered_hours": "sum"
        }).reset_index()
        return usage_by_hour
    else:
        st.error("Kolom 'cnt_hours', 'casual_hours', 'registered_hours', atau 'hr' tidak ditemukan dalam dataset.")
        return pd.DataFrame()

def create_summary_df(df):
    if {'holiday_hours', 'cnt_hours'}.issubset(df.columns):
        summary = df.groupby('holiday_hours').agg(total_peminjaman=('cnt_hours', 'sum'),
                                                  rata_rata_peminjaman=('cnt_hours', 'mean')).reset_index()
        summary['holiday_hours'] = summary['holiday_hours'].replace({0: 'Hari Biasa', 1: 'Hari Libur'})
        return summary
    else:
        st.error("Kolom 'holiday_hours' atau 'cnt_hours' tidak ditemukan dalam dataset.")
        return pd.DataFrame()

all_data = pd.read_csv(r"D:\VisualCode\Bangkit\all_data.csv")

with st.sidebar:
    st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="https://img.freepik.com/free-vector/realistic-bicycle-isolated_1284-12994.jpg?t=st=1727521649~exp=1727525249~hmac=bd6caaf3fcf881c4f3241a56fbf9d047b3c7a566024c02d2b31e696b34204a13&w=740" 
        style="border-radius: 50%; width: 200px; height: 200px;">
    </div>
    """,
    unsafe_allow_html=True
)
    if 'dteday' in all_data.columns:
        min_date = pd.to_datetime(all_data['dteday']).min().date()
        max_date = pd.to_datetime(all_data['dteday']).max().date()
        
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        
        all_data['dteday'] = pd.to_datetime(all_data['dteday'])
        filtered_df = all_data[(all_data['dteday'] >= str(start_date)) & (all_data['dteday'] <= str(end_date))]
    else:
        st.error("Kolom 'dteday' tidak ditemukan dalam dataset.")
        filtered_df = pd.DataFrame()

usage_by_hour_df = create_usage_by_hour_df(filtered_df)

if not filtered_df.empty and {'casual_hours', 'registered_hours'}.issubset(filtered_df.columns):
    total_casual = filtered_df['casual_hours'].sum()
    total_registered = filtered_df['registered_hours'].sum()

    st.metric("Total Pengguna Casual", f"{total_casual:,}")
    st.metric("Total Pengguna Registered", f"{total_registered:,}")

if not usage_by_hour_df.empty:
    st.subheader('Distribusi Penggunaan Bike Sharing Berdasarkan Jam')

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.barplot(x='hr', y='cnt_hours', data=usage_by_hour_df, palette='coolwarm', ax=ax)
    ax.set_title('Distribusi Penggunaan Bike Sharing Berdasarkan Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Total Penggunaan')
    hour_labels = [f"{hour:02d}:00" for hour in usage_by_hour_df['hr']]
    ax.set_xticklabels(hour_labels)
    st.pyplot(fig)

summary_df = create_summary_df(filtered_df)

if not summary_df.empty:
    st.subheader('Perbandingan Peminjaman pada Hari Libur dan Hari Biasa')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(summary_df['holiday_hours'], summary_df['total_peminjaman'], color=['blue', 'orange'])

    for i, v in enumerate(summary_df['total_peminjaman']):
        ax.text(i, v + 1000, str(v), ha='center', fontsize=10)

    ax.set_xlabel('Tipe Hari', fontsize=12)
    ax.set_ylabel('Total Peminjaman', fontsize=12)
    ax.set_title('Perbandingan Peminjaman pada Hari Libur dan Hari Biasa', fontsize=14, pad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)