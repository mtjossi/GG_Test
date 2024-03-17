# imports
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import sqlite3


st.set_page_config(page_title="Galactic Grid", layout="wide")


st.title("Galactic Grid")
st.text("Chavanette Advisor's CBDC Vendor & Solution Assessment")

# st.sidebar.title("Different Charts")
vendor_synopsis = {'Vendor 1':"A German multinational specializing in security technology. Vendor 1 is a world leader in physical and digital security solutions, including banknotes, secure documents, identification cards, and secure printing technologies. They play a vital role in safeguarding sensitive information and valuables.",
                   'Vendor 2':"This Vendor specializes in Central Bank Digital Currencies (CBDCs). They offer a proprietary blockchain technology called Vendor 2 Aureum designed to facilitate the creation and integration of national CBDC networks. Their solution aims to bridge the gap between traditional financial systems and digital currencies.",
                   'Vendor 3':"A company providing blockchain technology solutions for the finance industry. Vendor 3's core product, Vendor3Net, is a global network that facilitates secure and faster international payments. They aim to revolutionize how financial institutions work together by leveraging blockchain technology.",
                   'Vendor 4':"A Japanese blockchain technology company focused on enterprise solutions. Vendor 4 is known for developing Hyperledger Iroha, a business-friendly blockchain platform used for various applications, such as supply chain management, identity management, and loyalty programs. They help businesses leverage the power of blockchain technology for real-world use cases.",
                   'Vendor 5':"A fintech company based in Barbados, specializing in central bank digital currencies (CBDCs). Vendor 5 played a key role in developing the Eastern Caribbean Central Bank Digital Currency (ECDC) pilot program. They offer expertise in designing and implementing CBDC solutions for governments and financial institutions."}

con = sqlite3.connect('./data/gg_scoring.db')
cur = con.cursor()

# df = pd.read_csv('data/scores.csv')
# names = pd.read_csv('data/score_names.csv')
# weights = pd.read_csv('data/weights.csv')
df = pd.read_sql_query("SELECT * FROM scores", con)
names = pd.read_sql_query("SELECT * FROM score_names", con)
weights = pd.read_sql_query("SELECT * FROM weights", con)


df['vendor_id'] = df['vendor_id'].apply(str)

st.success("⬇️ Step 1: Please choose a Vendor to Focus on :smiley:")
if 'focus_vendor' not in st.session_state:
    st.session_state['focus_vendor'] = st.selectbox("Choose a Vendor", df['vendor_id'].unique())
else:
    st.session_state['focus_vendor'] = st.selectbox("Choose a Vendor", df['vendor_id'].unique())   

st.subheader("Quick Vendor Synopsis")    
st.write(vendor_synopsis[st.session_state['focus_vendor']])

st.write('---')
st.warning("⬅️ Step 2: Please choose a graph type from the sidebar :smiley:")



st.write("---")


# df['vendor_id'] = df['vendor_id'].apply(lambda x: f"Vendor {x}")
# df.to_sql('scores', con, if_exists='replace')
