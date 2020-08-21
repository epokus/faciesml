from bokeh.plotting import figure
from bokeh.layouts import row
from bokeh.models import Range1d, LinearAxis, LogAxis, PrintfTickFormatter


from script.vars import val_dict, tc_200, color_pallete

def log_maker(cds, plot_data = [['GR'],['NPHI', 'RHOB'], ['RT','RM']]):
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
                   x_range_name=val)

            p.scatter(val ,'DEPT' ,source = cds ,
                      fill_color = None ,
                      line_color = None ,
                      x_range_name = val,
                      selection_color = 'green')

            # log_gr.scatter(val ,'DEPT' ,source = cds ,fill_alpha = 0 ,line_color = None ,
            #                selection_color = 'green' ,nonselection_fill_alpha = 0 ,)


        p_container.append(p)
    return p_container