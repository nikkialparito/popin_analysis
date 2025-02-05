import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="PopIn Events Dashboard",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df = pd.read_csv('/mnt/data/MeetUp_PopIn_Events.csv')

df['Date & Time'] = pd.to_datetime(df['Date & Time'])
df['Year'] = df['Date & Time'].dt.year
df['Month'] = df['Date & Time'].dt.strftime('%Y-%m')

df.dropna(subset=['Attendees'], inplace=True)

df_category_counts = df['Category'].value_counts().reset_index()
df_category_counts.columns = ['Category', 'Event Count']

df_top_events = df.sort_values(by='Attendees', ascending=False).head(10)

df_monthly = df.groupby('Month').size().reset_index(name='Event Count')

def make_heatmap(input_df, x, y, color, color_theme):
    return alt.Chart(input_df).mark_rect().encode(
        x=alt.X(f'{x}:O', axis=alt.Axis(title="Month", labelAngle=0)),
        y=alt.Y(f'{y}:O', axis=alt.Axis(title="Category")),
        color=alt.Color(f'max({color}):Q', scale=alt.Scale(scheme=color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25)
    ).properties(width=900)

def make_bar_chart(input_df, x, y, color_theme):
    return alt.Chart(input_df).mark_bar().encode(
        x=alt.X(f'{x}:O', sort='-y'),
        y=alt.Y(f'{y}:Q'),
        color=alt.Color(f'{y}:Q', scale=alt.Scale(scheme=color_theme)),
        tooltip=[x, y]
    ).properties(width=900)

with st.sidebar:
    st.title("📅 PopIn Events Dashboard")
    years = list(df['Year'].unique())[::-1]
    selected_year = st.selectbox("Select a Year", years, index=0)
    df_filtered = df[df['Year'] == selected_year]
    color_themes = ['blues', 'cividis', 'greens', 'magma', 'plasma', 'reds', 'viridis']
    selected_color_theme = st.selectbox("Select a Color Theme", color_themes)

st.markdown("### Event Trends Over Time")
monthly_chart = make_bar_chart(df_monthly, 'Month', 'Event Count', selected_color_theme)
st.altair_chart(monthly_chart, use_container_width=True)

st.markdown("### Top Event Categories")
category_chart = make_bar_chart(df_category_counts, 'Category', 'Event Count', selected_color_theme)
st.altair_chart(category_chart, use_container_width=True)

st.markdown("### Most Attended Events")
st.dataframe(df_top_events[['Event Name', 'Location', 'Attendees']], hide_index=True)
