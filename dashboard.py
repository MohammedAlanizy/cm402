import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cyber Security Project", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("cybersecurity_intrusion_data.csv")
    df['encryption_used'] = df['encryption_used'].fillna('Unencrypted')
    df['Attack Status'] = df['attack_detected'].replace({0: 'Normal Traffic', 1: 'Attack'})
    return df

df_original = load_data()

st.sidebar.title("Dashboard")
selected_protocol = st.sidebar.selectbox("Filter Data by Network Protocol", ["Show All Data"] + list(df_original['protocol_type'].unique()))

df = df_original if selected_protocol == "Show All Data" else df_original[df_original['protocol_type'] == selected_protocol]

st.title("Protecting Data")
st.markdown("**By: Mohammed Alanizy**")
st.markdown("---")

st.markdown("### Introduction & Objectives")
st.markdown("We live in a digital world where data is everything. The goal of this research is to find exact patterns of computer attacks on our network. By looking at this data, I will prove that we must invest money into better cloud security to keep a company safe.")

st.markdown("### Research & Methodology")
st.markdown("I used a synthetically generated Cybersecurity Intrusion Detection dataset to safely look at network attacks without sharing private user information. The data tracks browser types, failed logins, encryption, and IP reputation. **You can use the menu on the left to filter all the charts below by specific network protocols.**")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sessions Displayed", f"{len(df):,}"); col2.metric("Attacks Detected", f"{df['attack_detected'].sum():,}", delta_color="inverse"); col3.metric("Current Attack Rate", f"{(df['attack_detected'].sum() / len(df)) * 100:.1f}%" if len(df) > 0 else "0%")

st.markdown("---")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Question 1: How do attackers access the system?**")
    browser_rates = df.groupby('browser_type')['attack_detected'].mean().mul(100).reset_index(name='Attack Rate (%)').sort_values('Attack Rate (%)', ascending=False)
    st.plotly_chart(px.bar(browser_rates, x='browser_type', y='Attack Rate (%)', color='browser_type', color_discrete_map={'Unknown': '#d73027'}, color_discrete_sequence=['#74add1'], labels={'browser_type': 'Browser Type'}).update_layout(showlegend=False), use_container_width=True)

with chart_col2:
    st.markdown("**Question 2: What are the early warning signs?**")
    df['Failed Logins Group'] = df['failed_logins'].clip(upper=5)
    login_rates = df.groupby('Failed Logins Group')['attack_detected'].mean().mul(100).reset_index(name='Attack Rate (%)')
    st.plotly_chart(px.bar(login_rates, x='Failed Logins Group', y='Attack Rate (%)', color='Failed Logins Group', color_continuous_scale=['#74add1', '#74add1', '#d73027', '#d73027']).add_hline(y=100, line_dash="dash", line_color="red", annotation_text="100% Danger Zone"), use_container_width=True)

st.markdown("---")
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("**Question 3: Does encryption keep us safe?**")
    enc_rates = df.groupby('encryption_used')['attack_detected'].mean().mul(100).reset_index(name='Attack Rate (%)').sort_values('Attack Rate (%)', ascending=False)
    st.plotly_chart(px.bar(enc_rates, x='encryption_used', y='Attack Rate (%)', color='encryption_used', color_discrete_map={'DES': '#d73027'}, color_discrete_sequence=['#74add1'], labels={'encryption_used': 'Encryption Algorithm'}).update_layout(showlegend=False), use_container_width=True)

with chart_col4:
    st.markdown("**Question 4: Can we predict an attack?**")
    st.plotly_chart(px.violin(df, y="ip_reputation_score", x="Attack Status", color="Attack Status", box=True, points="all", color_discrete_map={'Normal Traffic': '#74add1', 'Attack': '#d73027'}, labels={'ip_reputation_score': 'IP Reputation Score'}), use_container_width=True)

st.markdown("---")
st.markdown("### Conclusion & Recommendations")
st.success("**To fix these security holes immediately, we must invest money to do the following:**\n\n1. Block all traffic coming from \"Unknown\" web browsers.\n2. Lock user accounts instantly after 3 failed login attempts.\n3. Stop using older DES encryption and upgrade the whole system to AES.")


# my answers for the questions
#1. As we can see in this first chart the attackers mostly hide behind 'Unknown' browsers. That is our highest risk
#2. as we can see in the chart, if a login fails 3 times, it enters the red danger zone, meaning it is almost certainly an attack
#3. as we can see in the chart, we can see old encryption methods like DES fail to keep us safe and have the highest attack rates
#4. this violin plot shows we can predict attacks. A higher IP reputation score means the traffic is really bad!!