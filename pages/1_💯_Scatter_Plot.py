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
score_mean['Score1'] = np.round(score_mean['Score1'], 1)
score_mean['Score2'] = np.round(score_mean['Score2'], 1)
score_mean['Mag'] = np.round(score_mean['Mag'], 1)
score_mean['Vendor'] = score_mean['Vendor'].apply(str)

marker_size = score_mean["Mag"]
vendor_colors = ["#f2a154", "#c7f6ff", "#f25454", "#f7e25f", "#fffadb"]
def_num = ['Vendor 1', 'Vendor 2']
vendor_choice = st.multiselect("Select which Vendors to Compare", 
                               options=score_mean['Vendor'].unique(), default=def_num +[st.session_state['focus_vendor']] if st.session_state['focus_vendor'] not in def_num else def_num)
# st.session_state['focus_vendor'] = vendor_choice
selected_df = score_mean.query(f"Vendor in @vendor_choice")

data = go.Scatter(
    x=selected_df["Score1"],
    y=selected_df["Score2"],
    mode='markers',
    text=selected_df["Vendor"],
    marker=dict(
                  size=marker_size,
                  sizemode='diameter',
                  sizeref=max(marker_size)/20,
                  sizemin=1,
                  color=vendor_colors,
                  opacity=1
              ),
               legendgroup="vendors",
    showlegend=False,
    name='Vendor Score'
)
fig = go.Figure()
fig.add_trace(go.Scatter(x=[i for i in range(0,100)], y=np.ones(100)*50, 
                         line=dict(color='royalblue', width=1, dash='dot'), showlegend=False,
                         visible='legendonly'))
fig.add_trace(go.Scatter(x=np.ones(100)*50, y=[i for i in range(0,100)], 
                         line=dict(color='royalblue', width=1, dash='dot'), showlegend=False,
                         visible='legendonly'))
fig.add_trace(go.Scatter(x=[0, 50, 50, 0], y= [0, 0, 50, 50],
                         fill='toself', fillcolor='black', showlegend=False,
                         text="Blackhole", opacity=.5, legendgroup="quads", 
                         name="", mode='lines'))
fig.add_trace(go.Scatter(x=[0, 0, 50, 50], y= [50, 100, 100, 50],
                         fill='toself', fillcolor='yellow', showlegend=False,
                         text="Comets", opacity=.5, legendgroup="quads", 
                         name="", mode='lines'))
fig.add_trace(go.Scatter(x=[50, 50, 100, 100], y= [0, 50, 50, 0],
                         fill='toself', fillcolor='orange', showlegend=False,
                         text="Protostar", opacity=.5, legendgroup="quads", 
                         name="", mode='lines'))
fig.add_trace(go.Scatter(x=[50, 50, 100, 100], y= [50, 100, 100, 50],
                         fill='toself', fillcolor='lightblue', showlegend=False,
                         text="Supernova", opacity=.5, legendgroup="quads", 
                         name="", mode='lines'))
# fig = go.Figure(data)
fig.add_trace(data)

# fig = px.scatter(score_mean, x="Score1", y="Score2",
# 	         size="Mag", color="Vendor",
#                  hover_name="Vendor", size_max=10,
#                  text=score_mean["Vendor"],
#                  ,
#                  )
fig.update_traces(hovertemplate='%{text}<br>Score: %{marker.size}')
fig.update_layout(legend_title="Legend Title")


show_mean = st.checkbox("Show Mean Scores")
if show_mean:
  # fig.add_trace(go.Scatter(mode='markers', x=[np.mean(selected_df['Score1'])], y=[np.mean(selected_df['Score2'])], 
  #                         line=dict(color='red', width=10, dash='dot'), showlegend=True,
  #                         marker_symbol='hash-dot', 
  #                         hovertemplate='Selection Mean<br>Score: %{marker.size}',
  #                         marker=dict(
  #                           size=marker_size,
  #                           sizemode='diameter',
  #                           sizeref=max(marker_size)/15,
  #                           sizemin=1,
  #                           color=vendor_colors
  #                         ),
  #                         name="Selection Mean"
  #             ))
  fig.add_trace(go.Scatter(mode='markers', x=[np.mean(score_mean['Score1'])], y=[np.mean(score_mean['Score2'])], 
                          line=dict(color='white', shape='spline', dash='dot'), showlegend=True,
                          marker_symbol='asterisk', 
                           marker=dict(
                            size=marker_size,
                            sizemode='diameter',
                            sizeref=max(marker_size)/15,
                            sizemin=1,
                            color=vendor_colors
                            ),
                            hovertemplate='Overall Mean<br>Score: %{marker_size}<br>Score2: %{y}',
                            name="Overall Mean"
                          ))

fig.update_yaxes(range=[0,100])
fig.update_xaxes(range=[0,100])
fig.update_layout(title=("<b>Galactic Grid</b><br>" +
           "<i>Chavanette's CBDC Vendor Assessment</i>"),
                  autosize=False)

st.plotly_chart(fig, use_container_width=True)
