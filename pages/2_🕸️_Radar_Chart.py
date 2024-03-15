import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from Home import df, names, weights


c1, c2 = st.columns(2)
st.title("Galactic Grid")
st.text("Chavanette Advisor's CBDC Vendor & Solution Assessment")
# vendor_number = st.sidebar.selectbox("Choose a Vendor", df['vendor_id'].unique())

x=df[df['axis_id']==0]
y=df[df['axis_id']==1]

def get_graph1(df):
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

  fig = px.line_polar(full_df_1, r='Score', theta='Name', line_close=True, template='plotly_dark', color='Vendor')
  fig.update_traces(fill='toself')
  fig.update_layout(
      title={
          'text':'CBDC Technology - Solution Assessment',
          'x':0.5,
          'xanchor':'center',
          'yanchor':'top'
      },
      font=dict(
          family="Orbitron, monospace",
          size=10,
      )
  )
  fig.update_traces(textposition='middle center')
  fig.update_layout(legend=dict(
    yanchor="bottom",
    y=0.99,
    xanchor="right",
    x=0.99
))

  st.plotly_chart(fig, use_container_width=True)


def get_graph2(df):
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

  fig2 = px.line_polar(full_df_2, r='Score', theta='Name', line_close=True, template='plotly_dark', color='Vendor')
  fig2.update_traces(fill='toself')
  fig2.update_layout(
      title={
          'text':'CBDC Technology - Vendor Assessment',
          'x':0.5,
          'xanchor':'center',
          'yanchor':'top'
      },
      font=dict(
          family="Orbitron, monospace",
          size=10,
      )
  )
  fig2.update_traces(textposition='middle center')
  fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.25,
    xanchor="left",
    x=0.99
))

  st.plotly_chart(fig2, use_container_width=True)

with c1:
  graph_select = st.selectbox("Select which graph to display", ["CBDC Technology - Solution Assessment", "CBDC Technology - Vendor Assessment", "Both"])

with c2:
  def_num = ['1', '2']
  df['vendor_id'] = df['vendor_id'].apply(str)
  vendor_choice = st.multiselect("Select which Vendors to Compare", 
                               options=df['vendor_id'].unique(), default=def_num +[st.session_state['focus_vendor']] if st.session_state['focus_vendor'] not in def_num else def_num)

selected_df = df.query(f"vendor_id in @vendor_choice")



if graph_select == "CBDC Technology - Solution Assessment":
  get_graph1(selected_df)
elif graph_select == "CBDC Technology - Vendor Assessment":
  get_graph2(selected_df)
else:
  get_graph1(selected_df)
  st.write("---")
  get_graph2(selected_df)
  