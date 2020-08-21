from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource,Toolbar, ToolbarBox
from bokeh.models.tools import WheelZoomTool, PanTool, HoverTool, BoxSelectTool
from bokeh.models.widgets import Button, RadioButtonGroup, CheckboxButtonGroup, MultiSelect

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

import pandas as pd
import numpy as np

import las

from script.log_maker import log_maker
from script.vars import tc_200, facies_mapper, facies_pallete


df = pd.DataFrame(las.LASReader('data\SEM0400.las').data).replace(-999.25, np.nan)
# df = pd.DataFrame(las.LASReader("data/Keller 'B' No_ 1.LAS").data).replace(-999.25, np.nan)
df = df.dropna(subset=df.columns[:-1])


df['FACIES_NAME'] = [np.nan if np.isnan(val)  else facies_mapper[val]  for val in df['FACIES']]

# defining feed data for bokeh plot in CDS format

# facies_mapper = {1:'Upper Delta Front Mouthbar',
#                 2:'Lower Delta Front Mouthbar',
#                 3:'Prodelta sand',
#                 4:'Prodelta shale',
#                 5:'Channel',
#                 6:'Channel overbank',
#                 7:'Carbonate',
#                 np.nan:'Coal',}
#
#
#
# [facies_mapper[val] for val in df['FACIES']]


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
log_fac_input = figure(**tc_200, title = "Input Facies")
log_fac_input.image(image='image',
         source=fac,
         x = 0,
         y = b,
         dw = 1,
         dh = c,
         color_mapper=facies_pallete)

log_fac_pred = figure(**tc_200, title = "Predicted Facies")
log_fac_pred.image(image='image',
         source=fac_pred,
         x = 0,
         y = b,
         dw = 1,
         dh = c,
         color_mapper=facies_pallete)

# Triple Combo  creation
logs = log_maker(cds=cds, plot_data = [['GR'],['NPHI', 'RHOB'], ['RT']])

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
HoverTool_log = HoverTool(tooltips=tooltips_log, point_policy = "snap_to_data")

tools1 = (wheel_zoom, pan_tool, HoverTool_fac)
tools2 = (wheel_zoom, pan_tool, box_tool)

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
# fac_assign  = CheckboxButtonGroup(active=[], labels=['coal', 'udf', 'ldf', 'pd shale', 'pd sand', 'ch', 'ob', 'calc'])
fac_assign  = MultiSelect(value=[], options=[('0', 'Coal'),
                                             ('1', 'Upper Delta Plain'),
                                             ('2', 'Lowe Delta Plain'),
                                             ('3', 'Prodelta shale'),
                                             ('4', 'Prodelta sand'),
                                             ('5', 'Channel Sand'),
                                             ('6', 'Overbank Shale'),
                                             ('7', 'Carbonate')],
                          size=8)

algo_select  = RadioButtonGroup(active=0, labels=['LogReg', 'RandFor', 'AdaBo', 'XGB'])
clear_button = Button(label = 'clear data')
load_default = Button(label = 'load default data')
train_button = Button(label = 'train!')
button_group = column([fac_assign, algo_select, clear_button,load_default,train_button])


stack = row([log_fac_input, log_fac_pred, *logs ,toolbar_box,button_group])

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

        # temp = cds.data['FACIES_NAME']
        # print(new)
        # print(facies_mapper[new])
        # print(temp)
        # temp[selection] = facies_mapper[new]
        # cds.data['FACIES_NAME'] = temp

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

    # clf.fit(X[slicer], y[slicer])
    print('=============================================')
    print('training starting')
    print('algorithm used:')
    print(clf)
    clf.fit(X_train, y_train.flatten())
    print('training finished')
    print(f'train score: {clf.score(X_train, y_train)}')
    print(f'test score: {clf.score(X_test, y_test)}')
    print('=============================================')

    pred = clf.predict(X).reshape(-1 ,1)
    pred_name = [facies_mapper[val[0]] for val in pred]

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