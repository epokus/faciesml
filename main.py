from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource,Toolbar, ToolbarBox
from bokeh.models.tools import WheelZoomTool, PanTool, HoverTool, BoxSelectTool
from bokeh.models.widgets import Button, RadioButtonGroup, MultiSelect, Div

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

import pandas as pd
import numpy as np
import timeit

import las

from script.log_maker import triple_maker, nd_plot_maker
from script.vars import facies_mapper, facies_pallete, tc_img

df = pd.DataFrame(las.LASReader('data\SEM0400.las').data).replace(-999.25, np.nan)
# df = pd.DataFrame(las.LASReader("data/Keller 'B' No_ 1.LAS").data).replace(-999.25, np.nan)
# df = pd.DataFrame(las.LASReader("data/NELSON #9-16.LAS").data).replace(-999.25, np.nan)

df = df.dropna(subset=df.columns[:-1])


df['FACIES_NAME'] = [np.nan if np.isnan(val)  else facies_mapper[val]  for val in df['FACIES']]


cds = ColumnDataSource(df)
fac      = ColumnDataSource(dict(image=[np.array(df['FACIES'].to_list())[-1::-1].reshape(-1,1)],
                            FACIES_NAME=[df['FACIES_NAME'].to_list()[-1::-1]]))
fac_pred = ColumnDataSource(dict(image=[np.array(df['FACIES'].to_list())[-1::-1].reshape(-1,1)],
                            FACIES_NAME=[df['FACIES_NAME'].to_list()[-1::-1]]))

clf = LogisticRegression()
default_data = fac.data['image'][-1::-1]

# image limits
a = min(df['DEPT'])
b = max(df['DEPT'])
c = b - a

# Facies Log buttons creation
log_fac_input = figure(**tc_img, title = "Input Facies")
log_fac_input.image(image='image',
         source=fac,
         x = 0,
         y = b,
         dw = 1,
         dh = c,
         color_mapper=facies_pallete())

log_fac_pred = figure(**tc_img, title = "Predicted Facies")
log_fac_pred.image(image='image',
         source=fac_pred,
         x = 0,
         y = b,
         dw = 1,
         dh = c,
         color_mapper=facies_pallete())

# Triple Combo  creation
logs = triple_maker(cds=cds, plot_data = [['GR'],['NPHI', 'RHOB'], ['RT']])

# ND Plot
nd_plot = nd_plot_maker(cds, 'GR')

# Toolbox Creation
wheel_zoom = WheelZoomTool(dimensions='height')
pan_tool = PanTool(dimensions='height')
box_tool = BoxSelectTool()

tooltips_fac = [("Code", "@image"),('facies_name','@FACIES_NAME')]
tooltips_log = [("DEPTH", "@DEPT"),
            ("GR", "@GR"),
            ("NPHI", "@NPHI"),
            ("RHOB", "@RHOB"),
            ("RT" ,"@RT") ,
            ("FACIES", "@FACIES")]


HoverTool_fac = HoverTool(tooltips=tooltips_fac)
HoverTool_log = HoverTool(tooltips=tooltips_log, point_policy = "snap_to_data", names=['line_plot0','nd_plot'], mode='hline')

tools1 = (wheel_zoom, pan_tool, HoverTool_fac)
tools2 = (wheel_zoom, pan_tool, box_tool, HoverTool_log)

toolbar = Toolbar(tools=[wheel_zoom, pan_tool, box_tool, HoverTool_log ])
toolbar_box = ToolbarBox(toolbar=toolbar, toolbar_location='left')

## assigning tools to plots
log_fac_input.add_tools(*tools1)
log_fac_pred.add_tools(*tools1)

for i in range(len(logs)):
    logs[i].add_tools(*tools2)
    logs[i].y_range = logs[0].y_range
    log_fac_input.y_range = logs[0].y_range
    log_fac_pred.y_range  = logs[0].y_range



# defining buttons
fac_assign  = MultiSelect(value=[], options=[('0', 'Coal'),
                                             ('1', 'Upper Delta Plain'),
                                             ('2', 'Lowe Delta Plain'),
                                             ('3', 'Prodelta shale'),
                                             ('4', 'Prodelta sand'),
                                             ('5', 'Channel Sand'),
                                             ('6', 'Overbank Shale'),
                                             ('7', 'Carbonate')],
                          size=8)

algo_select  = RadioButtonGroup(active=0, labels=['LogReg', 'RandFor', 'AdaBo', 'XGB'],width=350)
clear_button = Button(label = 'clear data',
                      button_type="default", width=120, height=30)
load_default = Button(label = 'load default data',
                      button_type="default", width=120, height=30)
train_button = Button(label = 'train!!',
                      button_type="warning", width=100, height=30)


header_div = Div(width = 600,text = """<h1>Facies Machine Learning Dashboard</h1>
                        <p>This website meant to demonstrate the use of machine learning for supervised facies classification using several general algorithm. This web is developed by Epo P Kusumah - Dept of Geology, Universitas Pertamina (<a href="https://gl.universitaspertamina.ac.id/?page_id=8573" target="_blank" rel="noopener">link</a>). Sedstrat.com (<a href="https://www.sedstrat.com/" target="_blank" rel="noopener">link</a>).</p>
                        """)
debug_div = Div(width = 300, text = 'Test and Training Score Goes here:')
footer_div = Div(width = 1000, text = """<p>The data being used in this Web provided by Kansas Geological Survey, well id: <a href="https://chasm.kgs.ku.edu/ords/qualified.well_page.DisplayWell?f_kid=1044241592">NELSON #9-16</a></p>
""")
facies_assign_div = Div(text = "<p><strong>Facies Assignment</strong></p>")
button_group_div = Div(text = "<p><strong>Algorithm Selection and Training Button</strong></p>")

button_group = column([facies_assign_div, fac_assign, button_group_div,algo_select, row([clear_button,load_default,train_button])])


stack = column([header_div,row([log_fac_input, log_fac_pred, *logs ,toolbar_box,
                column([row([button_group, debug_div]), nd_plot,])]),footer_div])

# button callbacks
selection = [1]
temp = []
def selection_cb(attr, old, new):
    global selection
    selection = new

def facies_select_cb(attr, old, new):
    if fac_assign.value != []:
        temp = cds.data['FACIES']
        print(int(fac_assign.value[0]))
        temp[selection] = int(fac_assign.value[0])
        cds.data['FACIES'] = temp

        temp = temp.reshape(-1 ,1)
        fac.data['image'] = [temp[-1::-1]]
        fac_assign.value = []
    else:
        pass

def train_cb():
    X = np.c_[cds.data['GR'], cds.data['NPHI'], cds.data['RHOB']]
    y = fac.data['image'][0][-1::-1]

    slicer = np.where(~np.isnan(y.flatten()))

    X_train, X_test, y_train, y_test = train_test_split(X[slicer], y[slicer], test_size=0.33, random_state=42)

    global clf

    print('=============================================')
    print('training starting')
    print('algorithm used:')
    print(clf)
    tic = timeit.default_timer()
    clf.fit(X_train, y_train.flatten())
    toc1 = np.round((timeit.default_timer() - tic), 4)

    print(f'training finished')
    print(f'time for training: {toc1} sec')
    print(f'train score: {clf.score(X_train, y_train)}')
    print(f'test score: {clf.score(X_test, y_test)}')
    print('=============================================')


    tic = timeit.default_timer()
    pred = clf.predict(X).reshape(-1 ,1)
    toc2 =  np.round((timeit.default_timer() - tic), 4)
    print(f'time for prediction: {toc2} sec')
    pred_name = [facies_mapper[val[0]] for val in pred]

    debug_div.text = f"""<p>======================= <br /><strong>algorithm used: <br />{clf}</strong></p>
                        <p><strong><br />training starting ...</strong><br /><strong>training finished ... :))</strong></p>
                        <p>time for training: {toc1} sec</p>
                        <p>time for prediction: {toc2} sec</p>
                        <p><br />train score: {round(clf.score(X_train, y_train),3)}<br />test score: {round(clf.score(X_test, y_test),3)}<br />=======================</p>"""


    fac_pred.data['image'] = [pred[-1::-1]]
    fac_pred.data['FACIES_NAME'] = [pred_name[-1::-1]]

def clean_cb():
    temp = cds.data['FACIES']
    temp[:] = np.nan
    temp = temp.reshape(-1 ,1)
    fac.data['image'] = [temp[-1::-1]]


def algo_sel_cb(attr, old, new):
    global clf
    if algo_select.active == 0:
        clf = LogisticRegression()
    elif  algo_select.active == 1:
        clf = RandomForestClassifier()
    elif algo_select.active == 2:
        clf = AdaBoostClassifier()
    else:
        clf = XGBClassifier()

def load_default_cb():
    fac.data['image'] = default_data

# button triggers
cds.selected.on_change('indices', selection_cb)
# fac_assign.on_change('active', facies_select_cb)
fac_assign.on_change('value', facies_select_cb)

train_button.on_click(train_cb)
clear_button.on_click(clean_cb)
load_default.on_click(load_default_cb)
algo_select.on_change('active', algo_sel_cb)

curdoc().add_root(stack)
curdoc().title = 'Simple Facies Prediction with ML'
