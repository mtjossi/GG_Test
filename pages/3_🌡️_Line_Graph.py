import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from Home import df, names, weights

st.title("Galactic Grid")
st.text("Chavanette Advisor's CBDC Vendor & Solution Assessment")
# vendor_number = st.sidebar.selectbox("Choose a Vendor", df['vendor_id'].unique())

full_df_1 = pd.DataFrame(columns=['Name', 'Score', 'Vendor'])

for v in df['vendor_id'].unique():
  df_v = df[df['vendor_id']==v]
  x=df_v[df_v['axis_id']==0]

  score_name = []
  weighted_score = []
  for i in x['matrix_id'].unique():
    score_name.append(names[names['matrix_id']==i]['score_name'][i-1])
    weighted_score.append(x[x['matrix_id']==i]['score_value'].reset_index(drop=True).dot(weights[weights['matrix_id']==i]['weight_value'].reset_index(drop=True)))
    # print(f"{names[names['matrix_id']==i]['score_name'][i-1]}. weighted score: {x[x['matrix_id']==i]['score_value'].dot(weights[weights['matrix_id']==i]['weight_value'])}")

  score_dict1 = dict(zip(score_name, weighted_score))
  score_df1 = pd.DataFrame.from_dict(data=score_dict1, orient='index').reset_index()
  score_df1.columns = ['Name', 'Score']
  score_df1['Vendor'] = v

  full_df_1 = pd.concat([full_df_1, score_df1])

full_df_2 = pd.DataFrame(columns=['Name', 'Score', 'Vendor'])

for v in df['vendor_id'].unique():
  df_v = df[df['vendor_id']==v]
  y=df_v[df_v['axis_id']==1]

  score_name = []
  weighted_score = []
  for i in y['matrix_id'].unique():
    score_name.append(names[names['matrix_id']==i]['score_name'][i-1])
    weighted_score.append(y[y['matrix_id']==i]['score_value'].reset_index(drop=True).dot(weights[weights['matrix_id']==i]['weight_value'].reset_index(drop=True)))
    # print(f"{names[names['matrix_id']==i]['score_name'][i-1]}. weighted score: {x[x['matrix_id']==i]['score_value'].dot(weights[weights['matrix_id']==i]['weight_value'])}")

  score_dict2 = dict(zip(score_name, weighted_score))
  score_df2 = pd.DataFrame.from_dict(data=score_dict2, orient='index').reset_index()
  score_df2.columns = ['Name', 'Score']
  score_df2['Vendor'] = v

  full_df_2 = pd.concat([full_df_2, score_df2])

  score_mean = pd.DataFrame(columns=['Vendor', 'Score1', 'Score2'])

vendor = []
score1 = []
score2 = []
for v in full_df_1['Vendor'].unique():
  df = full_df_1[full_df_1['Vendor']==v]
  vendor.append(v)
  score1.append(df.loc[:,'Score'].mean())

score_mean['Vendor'] = vendor
score_mean['Score1'] = score1



for v in full_df_2['Vendor'].unique():

  df = full_df_2[full_df_2['Vendor']==v]
  score2.append(df.loc[:,'Score'].mean())

score_mean['Vendor'] = vendor
score_mean['Score1'] = score1
score_mean['Score2'] = score2

score_mean['Mag'] = np.sqrt(np.square(score_mean['Score1']) + np.square(score_mean['Score2']))
score_mean['Vendor'] = score_mean['Vendor'].apply(str)

def_num = ['1', '2']
vendor_choice = st.multiselect("Select which Vendors to Compare", 
                               options=score_mean['Vendor'].unique(), default=def_num +[st.session_state['focus_vendor']] if st.session_state['focus_vendor'] not in def_num else def_num)
selected_df = score_mean.query(f"Vendor in @vendor_choice")

fig = go.Figure()
# vendor_colors = ["#f25454", "#f2a154", "#f7e25f", "#fffadb", "#c7f6ff"]
vendor_colors = ["#f2a154", "#c7f6ff", "#f25454", "#f7e25f", "#fffadb"]
fig.add_trace(go.Scatter(
    x=score_mean['Mag'], y=np.zeros(selected_df.shape[0]), mode='markers', marker_size=20,
    marker_color=vendor_colors, opacity=.9
))
fig.update_xaxes(showgrid=False, range=[0,100])
fig.update_yaxes(showgrid=False, 
                 zeroline=True, zerolinecolor='white', zerolinewidth=5,
                 showticklabels=False)
# fig.update_layout(height=200, plot_bgcolor='black', 
#                   title=("<b>Galactic Grid</b><br>"+"<i>Chavanette's CBDC Vendor Assessment</i>"))

fig.update_layout(height=200, plot_bgcolor='black')
st.plotly_chart(fig)