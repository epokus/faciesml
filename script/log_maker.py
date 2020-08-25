from bokeh.plotting import figure

from bokeh.models import Range1d, LinearAxis, LogAxis, PrintfTickFormatter, LinearColorMapper, ColorBar
import numpy as np


from script.vars import val_dict, tc_200, color_pallete, nd_plot_size

def triple_maker(cds, plot_data = [['GR'],['NPHI', 'RHOB'], ['RT','RM']]):
    p_container = []
    for log_group in plot_data:
        y_scale = val_dict[log_group[0]]['scale']
        p = figure(**tc_200, x_axis_type = y_scale)
        p.y_range.flipped = True
        p.extra_x_ranges[''] = Range1d(start=0, end=1)

        p.add_layout(LinearAxis(x_range_name='', axis_label='',
                                axis_line_color=None,
                                major_tick_line_color=None,
                                minor_tick_line_color=None,
                                major_label_text_color=None,
                                axis_label_text_line_height=0), 'above')

        for num, val in enumerate(log_group):
            p.extra_x_ranges[val] = Range1d(start=val_dict[val]['lim'][0], end=val_dict[val]['lim'][1])

            if y_scale =='log':
                p.add_layout(LogAxis(axis_line_width=3,
                                        axis_line_color=val_dict[val]['color'],
                                        axis_line_dash=val_dict[val]['linedash'],
                                        x_range_name=val,
                                        axis_label=val), 'above')
                p.xaxis[num+1].formatter = PrintfTickFormatter(format="%5f")


            else:
                p.add_layout(LinearAxis(axis_line_width=3,
                                        axis_line_color=val_dict[val]['color'],
                                        axis_line_dash=val_dict[val]['linedash'],
                                        x_range_name=val,
                                        axis_label=val), 'above')

            p.line(val, 'DEPT', source=cds,
                   color = val_dict[val]['color'],
                   line_dash=val_dict[val]['linedash'],
                   line_width=1,
                   x_range_name=val,
                   name='line_plot'+str(num))

            p.scatter(val ,'DEPT' ,source = cds ,
                      fill_color = None ,
                      line_color = None ,
                      x_range_name = val,
                      selection_color = 'green')

        p_container.append(p)
    return p_container



def nd_plot_maker(cds, column):

    mapper = LinearColorMapper(palette = 'Viridis256' ,
                               low  = np.percentile(cds.data[column], q = 5) ,
                               high = np.percentile(cds.data[column], q = 95))

    color_bar = ColorBar(color_mapper = mapper,
                         title = column,
                         location=(0,0))

    p = figure(**nd_plot_size, title = "ND Plot",
               tools=["pan,wheel_zoom,box_zoom,reset,box_select"])

    p.scatter('NPHI' ,'RHOB' ,
              fill_color = {'field': column ,'transform': mapper} ,
              line_color = None , fill_alpha= 0.5,
              source = cds, name='nd_plot')


    p.line([-0.028,1],[2.65,1],line_color= color_pallete['orange'][2], line_dash='dashed', line_width = 3)
    p.line([0,1],[2.71,1],line_color=color_pallete['blue'][2], line_dash='dashed', line_width = 3)
    p.line([0.05,1],[2.83,1],line_color=color_pallete['purple'][0], line_dash='dashed', line_width = 3)

    p.add_layout(color_bar, 'right')

    p.xaxis.axis_label = 'NPHI'
    p.yaxis.axis_label = 'RHOB'
    p.y_range = Range1d(3, 1.6)
    p.x_range = Range1d(-0.15, 0.6,)

    return p