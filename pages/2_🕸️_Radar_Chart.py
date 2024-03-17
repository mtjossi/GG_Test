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
score_mean['Mag'] = np.round(score_mean['Mag'])

def_num = ['Vendor 1', 'Vendor 2']
vendor_choice = st.multiselect("Select which Vendors to Compare", 
                               options=score_mean['Vendor'].unique(), default=def_num +[st.session_state['focus_vendor']] if st.session_state['focus_vendor'] not in def_num else def_num)
selected_df = score_mean.query(f"Vendor in @vendor_choice")
data = score_mean.query(f"Vendor in @vendor_choice")[["Vendor", "Mag"]]



fig = px.bar(data, x='Vendor', y='Mag', hover_data=["Mag"], color="Vendor",
             labels={"Mag":"Vendor Overall Score"})
fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.update_yaxes(range=[0,100])
fig.update_layout(title_text=("<b>CBDC Technology Overall Score</b>"))
fig.update_layout(showlegend=False)
add_mean = st.checkbox("Display mean?")
if add_mean:
  fig.add_hline(y=score_mean["Mag"].mean(), line_dash="dash", line_color="white", annotation_text="Overall Mean")
  # fig.add_hline(y=data["Mag"].mean(), line_dash="dash", line_color="lightseagreen")
  # fig.add_hline(y=data["Mag"].mean(), line_dash="dash", line_color="yellow", annotation_text="Selection Mean")
  # fig.add_annotation(text="Selection Mean", x=data['Vendor'].max(), y=data["Mag"].mean())
  fig.update_annotations(x=0, xanchor='auto')
  fig.update_layout(title_text=("<b>CBDC Technology Overall Score</b>"))
st.plotly_chart(fig, use_container_width=True)
