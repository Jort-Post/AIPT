import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_excel('AIPT_A2_data.xls')
print(df.head())

MRV_heuristic = df[df['heuristic'] == 'Minimum Remaining Value']
degree_heuristic = df[df['heuristic'] == 'Degree']
default = df[df['heuristic'] == 'Default']
MCN_heuristic = df[df['heuristic'] == 'Maximum Constraining Neighbour']

# Overall:
fig = px.box(df,
             x='heuristic',
             y='arc_revisions',
             title='Arc Revisions of all Heuristics',
             labels={'arc_revisions': 'Arc Revisions',
                     'heuristic': 'Heuristic'})
fig.show()

# Default barplot:
median_data = default.groupby('sudoku_id', as_index=False)['arc_revisions'].median()
fig = px.bar(median_data,
             x='sudoku_id',
             y='arc_revisions',
             title='Arc Revisions of Default Heuristic',
             labels={'sudoku_id': 'Sudoku Puzzle ID',
                     'arc_revisions': 'Median of Arc Revisions'})
fig.show()

# MRV_heuristic barplot:
median_data = MRV_heuristic.groupby('sudoku_id', as_index=False)['arc_revisions'].median()
fig = px.bar(median_data,
             x='sudoku_id',
             y='arc_revisions',
             title='Arc Revisions of MRV Heuristic',
             labels={'sudoku_id': 'Sudoku Puzzle ID',
                     'arc_revisions': 'Median of Arc Revisions'})
fig.show()

# Degree heuristic barplot:
median_data = degree_heuristic.groupby('sudoku_id', as_index=False)['arc_revisions'].median()
fig = px.bar(median_data,
             x='sudoku_id',
             y='arc_revisions',
             title='Arc Revisions of Degree Heuristic',
             labels={'sudoku_id': 'Sudoku Puzzle ID',
                     'arc_revisions': 'Median of Arc Revisions'})
fig.show()

# MCN_heuristic barplot:
median_data = MCN_heuristic.groupby('sudoku_id', as_index=False)['arc_revisions'].median()
fig = px.bar(median_data,
             x='sudoku_id',
             y='arc_revisions',
             title='Arc Revisions of MCN Heuristic',
             labels={'sudoku_id': 'Sudoku Puzzle ID',
                     'arc_revisions': 'Median of Arc Revisions'})
fig.show()