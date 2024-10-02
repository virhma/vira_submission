import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Load Data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')


# DataFrame
# 1 - DataFrame pencarian jumlah pengguna pada tahun dan bulan tertentu
month_hour = hour_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
month_hour_df = pd.DataFrame(month_hour)

month_day = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
month_day_df = pd.DataFrame(month_day)

month_2011_day_df = month_day_df[month_day_df['yr'] == 0]
month_2012_day_df = month_day_df[month_day_df['yr'] == 1]

# 2 - DataFrame jumlah pengguna berdasarkan hari
weekday_hour_total = hour_df.groupby(['weekday'])['cnt'].sum().reset_index()
weekday_hour_total_df = pd.DataFrame(weekday_hour_total)

weekday_hour_casual = hour_df.groupby(['weekday'])['casual'].sum().reset_index()
weekday_hour_casual_df = pd.DataFrame(weekday_hour_casual)

weekday_hour_registered = hour_df.groupby(['weekday'])['registered'].sum().reset_index()
weekday_hour_registered_df = pd.DataFrame(weekday_hour_registered)

# 3 - DataFrame jumlah pengguna berdasarkan season (musim)
season_total = day_df.groupby(['season'])['cnt'].sum().reset_index()
season_total_df = pd.DataFrame(season_total)
season_total_df_sorted = season_total_df.sort_values(by='cnt', ascending=False)

# 4 - DataFrame jumlah pengguna berdasarkan waktu
hour_total = hour_df.groupby(['hr'])['cnt'].sum().reset_index()
hour_total_df = pd.DataFrame(hour_total)
hour_total_df_sorted = hour_total_df.sort_values(by='cnt', ascending=False)

top_5_hour_total = hour_total_df_sorted.head(4)

#Header
st.header('The Gowest Bike Sharing :sparkles:')

# Data pengguna berdasarkan tahun dan bulan
st.title("Jumlah Pengguna")

# Mengganti label pada tahun dan bulan
year_labels = {0: 2011, 1: 2012}
month_labels = {1: 'Jan', 2: 'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

# Pilih tahun
years_box = month_hour_df['yr'].unique()
labeled_years = [year_labels[year] for year in years_box]
selected_year = st.selectbox("Pilih Tahun", years_box, format_func=lambda x: year_labels[x])

# Pilih bulan
months_box = month_hour_df['mnth'].unique()
labeled_months = [month_labels[month] for month in months_box]
selected_month = st.selectbox("Pilih Bulan", months_box, format_func=lambda x: month_labels[x])

# Mencari data
result = month_hour_df.loc[(month_hour_df['yr'] == selected_year) & (month_hour_df['mnth'] == selected_month)]

# Menampilkan hasil
if not result.empty:
    cnt_value = result['cnt'].values[0]
    st.write(f"Jumlah pengguna pada tahun {year_labels[selected_year]} dan bulan {month_labels[selected_month]} adalah: {cnt_value}")
else:
    st.write(f"Tidak ditemukan data pada tahun {year_labels[selected_year]} dan bulan {month_labels[selected_month]}.")

# Tampilan Data Grafis hasil analisis
st.title("Data Grafis")

# --Grafik Analisis 1
x_var = month_2011_day_df['mnth']
y_2011 = month_2011_day_df['cnt']
y_2012 = month_2012_day_df['cnt']

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(x_var, y_2011, label='2011', color='teal')
ax.plot(x_var, y_2012, label='2012', color='salmon')
ax.set_xlabel('Month', size=12)
ax.set_ylabel('Total User', size=12)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax.set_xticks(ticks=range(1, 13), labels=months)
ax.legend()
ax.set_title('Total Users of Bike Sharing per Month', size=16)
st.pyplot(fig)

# --Grafik Analisis 2
casual_user = {'day': weekday_hour_casual_df['weekday'], 'count_user': weekday_hour_casual_df['casual']}

registered_user = {'day': weekday_hour_registered_df['weekday'], 'count_user': weekday_hour_registered_df['registered']}

total_user = {'day': weekday_hour_total_df['weekday'], 'count_user': weekday_hour_total_df['cnt']}

casual = pd.DataFrame(casual_user)
casual['status'] = 'casual'

registered = pd.DataFrame(registered_user)
registered['status'] = 'registered'

total = pd.DataFrame(total_user)
total['status'] = 'total'

combined = pd.concat([casual, registered, total], ignore_index=True)
colors_bar = {'casual': 'salmon', 'registered': 'teal', 'total': 'yellowgreen'}

fig, ax = plt.subplots(figsize=(12,5))
sns.barplot(x='day', y='count_user', hue='status', data=combined, palette=colors_bar)

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
ax.set_xticks(ticks=range(0, 7), labels=days)
ax.set_xlabel('Day', size=12)
ax.set_ylabel('User', size=12)
ax.set_title('Users per Day', size=16)
st.pyplot(fig)

# --Grafik Analisis 3
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,8))

colors_bar2 = ["mistyrose", "mistyrose", "salmon", "mistyrose"]
seasons = ['Springer', 'Summer', 'Fall', 'Winter']

sns.barplot(x="season", y="cnt", data=season_total_df_sorted, palette=colors_bar2 , ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Best Season for Ride a Bike", loc="center", fontsize=27)
ax[0].set_xticks(ticks=range(0,4), labels=seasons)
ax[0].tick_params(axis ='x', labelsize=18)

sns.barplot(x='hr', y='cnt', data=top_5_hour_total, palette=colors_bar2 , ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Best Hour for Ride a Bike", loc="center", fontsize=27)
ax[1].tick_params(axis ='x', labelsize=18)
st.pyplot(fig)
