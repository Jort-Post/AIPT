import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_excel('AIPT_A2_data.xls')
print(df.head())

MRV_heuristic = df[df['heuristic'] == 'Minimum Remaining Value']
degree_heuristic = df[df['heuristic'] == 'Degree']
default = df[df['heuristic'] == 'Default']
MCN_heuristic = df[df['heuristic'] == 'Maximum Constraining Neighbour']
heuristics = [default, MRV_heuristic, degree_heuristic, MCN_heuristic]

sudoku1 = df[df['sudoku_id']==1]
sudoku2 = df[df['sudoku_id']==2]
sudoku3 = df[df['sudoku_id']==3]
sudoku4 = df[df['sudoku_id']==4]
sudoku5 = df[df['sudoku_id']==5]

sudokus = [sudoku1, sudoku2, sudoku3, sudoku4, sudoku5]
# Overall:
fig = px.box(df,
             x='heuristic',
             y='arc_revisions',
             title='Arc Revisions of all Heuristics',
             labels={'arc_revisions': 'Arc Revisions',
                     'heuristic': 'Heuristic'})
#fig.show()

# Default barplot:
#median_data = default.groupby('sudoku_id', as_index=False)['arc_revisions'].median()
for s in range(len(sudokus)):
    fig = px.box(sudokus[s],
             x='heuristic',
             y='arc_revisions',
             title=f'Arc Revisions of all Heuristics on Sudoku {s+1}',
             labels={'heuristic': 'Heuristic',
                     'arc_revisions': 'Median of Arc Revisions'})
    fig.show()
