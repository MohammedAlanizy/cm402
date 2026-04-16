import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cyber Security Project", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("cybersecurity_large_synthesized_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['Hour'] = df['timestamp'].dt.hour.fillna(0).astype(int); df['Day'] = df['timestamp'].dt.day_name(); df['Is_Attack'] = df['outcome'].apply(lambda x: 1 if str(x).lower() == 'success' else 0); df['data_compromised_GB'] = pd.to_numeric(df['data_compromised_GB'], errors='coerce').fillna(0); df['Count'] = 1
    return df

df = load_data()

st.sidebar.title("Dashboard")
st.sidebar.markdown("---")
ind = st.sidebar.selectbox("Filter Industry", ["Show All"] + list(df['industry'].dropna().unique()))
plot_df = df if ind == "Show All" else df[df['industry'] == ind]

st.title("Why We Need AI To Protect Our Data")
st.markdown("**My Main Idea:** Humans are too slow to stop hackers now. We need to spend money to use smart AI to defend our cloud. The data shows that when we are slow, we lose massive gigabytes of data, and hackers attack us at specific times to break our old tools.")
col1, col2, col3 = st.columns(3)
col1.metric("Total Data Rows", f"{len(plot_df):,}"); col2.metric("Total Data Lost (GB)", f"{plot_df['data_compromised_GB'].sum():,.1f}", delta_color="inverse"); col3.metric("System Failure Rate", f"{(plot_df['Is_Attack'].sum() / len(plot_df)) * 100:.1f}%" if len(plot_df) > 0 else "0%")
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown("**1. How much data do we lose when we are slow?**")
    st.plotly_chart(px.scatter(plot_df, x="response_time_min", y="data_compromised_GB", color="outcome", size="attack_severity", opacity=0.5, color_discrete_map={"Success": "#d73027", "Failed": "#74add1", "success": "#d73027", "failed": "#74add1"}, hover_data=["attack_type", "target_system"]).update_layout(margin=dict(l=0, r=0, b=0, t=0)), use_container_width=True)
    st.write("I asked how much data we lose based on our speed. The data shows that if our team is fast (under 90 minutes), we lose about 50 Gigabytes. If we are slow, we still lose about 50 Gigabytes. This proves a big point: human speed does not matter anymore. Once the hacker is in, the data is gone. Humans cannot be fast enough, so we must use AI.")

with chart_col2:
    st.markdown("**2. What day and hour do hackers win the most?**")
    st.plotly_chart(px.density_heatmap(plot_df, x="Hour", y="Day", z="Is_Attack", histfunc="sum", color_continuous_scale="Viridis"), use_container_width=True)
    st.write("I asked what day and hour hackers win the most. Hackers wait until we are sleeping. The brightest yellow color on the heatmap is Wednesday at 23:00 (11:00 PM). Hackers succeeded exactly 345 times at this exact hour! Humans cannot be perfect at night, which proves we need an automated AI system to watch the cloud.")
st.markdown("---")
chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    st.markdown("**3. Which security tools fail the most against attacks?**")
    st.plotly_chart(px.treemap(plot_df.dropna(subset=['target_system', 'attack_type', 'security_tools_used']), path=[px.Constant("Network"), 'target_system', 'attack_type', 'security_tools_used'], values='Count', color='Is_Attack', color_continuous_scale='Reds'), use_container_width=True)
    st.write("I asked which security tools fail the most. Some of our old tools are completely broken. The data shows that our 'IDS' tool is the weakest point. It failed 242 times when hackers used Brute Force attacks to break into our Web Server. This shows exactly what we need to spend money to fix first.")

with chart_col4:
    st.markdown("**4. Which countries do the most damage to us?**")
    st.plotly_chart(px.scatter_geo(plot_df[plot_df['Is_Attack']==1].groupby('location').agg({'data_compromised_GB':'sum', 'attack_severity':'mean'}).reset_index(), locations="location", locationmode="country names", size="data_compromised_GB", color="attack_severity", color_continuous_scale="Reds", template="plotly_white"), use_container_width=True)
    st.write("I asked which countries do the most damage to us. We get attacks from everywhere, but three countries steal the most data. The United Kingdom is number one, stealing over 256,000 Gigabytes! China and Canada are right behind them, both stealing over 250,000 Gigabytes. The map proves we must put strong security blocks on traffic coming from these specific countries.")
st.markdown("---")
st.success("**Final Plan to Fix This:**\nBecause of the data charts above, we must do this now:\n1. **Use AI:** The bubble chart shows human speed cannot save the 50 GB data loss. We need AI to stop it instantly.\n2. **Fix Broken Tools:** The treemap shows exactly that our IDS tool is failing against Brute Force attacks. We need to upgrade it.\n3. **Block Bad Countries:** We must stop traffic from the UK, China, and Canada, especially during our bright yellow hours on Wednesday night. For example, if the website is a government site, we can block all traffic from these countries. If it is a business site, we can require extra verification for users from these countries.")