color_pallete  =  {'black'   : ['#F3F3F3', '#1E1F1F', '#626564', '#C5C5C5', '#FEFEFE', '#F7F8F8'],
                   'brown'   : ['#F3F4F2', '#BAAFA0', '#382824', '#EBE1D3', '#F0EEE7', '#FBFAF7'],
                   'dk-green': ['#098B86', '#F5F4F3', '#A1D7C2', '#EEF5F0', '#E0EFE5', '#DCFDFC'],
                   'blue'    : ['#F3F4F2', '#0E4662', '#5EBECE', '#CEEBE8', '#ACDDDD', '#E8F8F9'],
                   'purple'  : ['#733875', '#F2F4F2', '#A29ABF', '#C9B7C7', '#FAF4FC', '#E2D3E5'],
                   'br-green': ['#F3F5F1', '#D9D865', '#6B985F', '#D4D9A0', '#08644B', '#E9EEC6'],
                   'orange'  : ['#F2F4F3', '#E87F43', '#F7CD5D', '#F8E3A7', '#FAF3E1', '#FAEBC0'],
                   'red'     : ['#F3F5F3', '#D10F33', '#F37360', '#F7C2A3', '#FCEDE5', '#F8D2C2'],
                   'pink'    : ['#F1F5F3', '#AD1550', '#F7C5D0', '#FBEFF2', '#EC637A', '#F197A9']}


color_list = ['#011627', '#2EC4B6', '#E71D36', '#FF9F1C',
              '#BCE784', '#513B56', '#5DD39E', '#348AA7', '#525174',
              '#E2C044', '#2E5266', '#D3D0CB', '#6E8898', '#9FB1BC',
              '#ED6A5A', '#F4F1BB', '#9BC1BC', '#5CA4A9', '#E6EBE0',
              '#F20095', '#4F0A48', '#FFB400', '#FFFE01']

from bokeh.models.mappers import LinearColorMapper

def facies_pallete():
    palete = LinearColorMapper(palette = [color_pallete['black'][1],
                                                  color_pallete['red'][1],
                                                  color_pallete['orange'][3],
                                                  color_pallete['br-green'][4] ,
                                                  color_pallete['br-green'][1],
                                                  color_pallete['orange'][2],
                                                    color_pallete['black'][3],
                                                    color_pallete['blue'][2],
                                                    ],
                                                    low=0, high=8, nan_color = (255, 255, 255, 0))
    return palete
facies_mapper = {0:'Coal',
                 1:'Upper Delta Front/ Mouthbar',
                 2:'Lower Delta Front/ Mouthbar',
                 3:'Prodelta sand',
                 4:'Prodelta shale',
                 5:'Channel',
                 6:'Channel overbank',
                 7:'Carbonate',}

screen_multiplier = 1.3


tc_200 = {'plot_width': 150,
            'plot_height': 600,
            'toolbar_location': None,
            'x_axis_location': None}

tc_img = {'plot_width': 120,
            'plot_height': 600,
            'toolbar_location': None,
            'x_axis_location': None,
            'y_axis_location': None}

nd_plot_size = {'plot_width': 400,
                'plot_height': 350,}

val_dict = {'GR' :{'lim':[0,150],
                   'color':color_pallete['br-green'][4],
                   'linedash':'solid',
                   'scale':'linear'},
           'RHOB':{'lim':[1.95,2.95],
                   'color':color_pallete['red'][1],
                   'linedash':'solid',
                   'scale':'linear'},
           'NPHI':{'lim':[ 0.45, -0.15],
                   'color':color_pallete['br-green'][4],
                   'linedash':'dashed',
                   'scale':'linear'},
           'RT'  :{'lim':[0.2, 2000],
                   'color':color_pallete['red'][1],
                   'linedash':'dashed',
                   'scale':'log'},
           'RM':  {'lim':[0.2, 2000],
                   'color':color_pallete['blue'][2],
                   'linedash':'dashed',
                   'scale':'log'}}
