import sys
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import tkinter as tk
plt.rcParams['toolbar'] = 'toolmanager'
#.rcParams['font.family'] = 'monospace'
plt.rcParams['figure.figsize'] = 9.6, 7.2
dark = True
traces = {}
colors = {}
def main():
    global traces
    global colors
    if dark:
        plt.style.use('dark_background')
        colors = {'S11': 'yellow','S12': 'cyan','S21': 'magenta','S22': 'lime'}
    else:
        plt.style.use('default')
        colors = {'S11':'#1f77b4', 'S12': '#ff7f0e', 'S21': '#2ca02c','S22': '#d62728'}
    fig = plt.figure()
    data_file = tk.filedialog.askopenfilename()
    if not data_file:
        print("No file selected")
        return
    data = rf.Network(data_file, f_unit='mhz')
    traces.update({'S11': data.s11})
    traces.update({'S12': data.s12})
    traces.update({'S21': data.s21})
    traces.update({'S22': data.s22})
    
    
    plt.grid('both','both')
    
    fig.canvas.manager.toolmanager.add_tool('Mark', MarkButton)
    fig.canvas.manager.toolbar.add_tool('Mark', MarkButton)
    
    for trace in traces.keys():
        fig.canvas.manager.toolmanager.add_tool(trace, GroupHideTool, gid=trace)    
        fig.canvas.manager.toolbar.add_tool(trace, 'trace')
    
    mark('S11', '1500mhz')
    plt.show()

    

def mark(trace, frequency):
    '''mark(trace as str, frequency as str 'Xyhz')'''
    #mark('S11', '1ghz')
    y=float(traces[trace][frequency].s_db)
    x=traces[trace][frequency].frequency.f
    plt.plot(x,y,marker='|',color='black')
    plt.annotate(round(y,4),xy=(x,y+2), fontsize=10)
    f = str(traces[trace][frequency].frequency.center_scaled) + " " +traces[trace].frequency.unit
    plt.annotate(f,xy=(x,y+0.5), fontsize=8)

class MarkButton(ToolBase):
    description = 'Place marker'
    default_keymap = 'm, M'
    def trigger(self, *args, **kwargs):
        pass

class GroupHideTool(ToolToggleBase):
    '''Show lines with a given gid'''
    description = 'Show by gid'
    default_toggled = True
    

    def __init__(self, *args, gid, **kwargs):
        self.gid = gid
        super().__init__(*args, **kwargs)

    def enable(self, *args):
    
        traces[self.gid].plot_s_db(label=self.gid, gid=self.gid, color=colors[self.gid])
        self.redraw()

    def disable(self, *args):
        for ax in self.figure.get_axes():
            for line in ax.get_lines():
                if line.get_gid() == self.gid:
                    line.remove()
        self.redraw()

    def redraw(self, *args):
        plt.tight_layout()
        ax = plt.gca()
        ax.relim()
        ax.autoscale()
        ax.legend(loc=1)
        self.figure.canvas.draw()
        

if __name__ == "__main__":
    main()
    pass