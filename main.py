import os
import sys
import time
import tkinter as tk
from tkinter import simpledialog

import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.backend_tools import ToolBase, ToolToggleBase

plt.rcParams['toolbar'] = 'toolmanager'

marks = []
traces = {}
traces_active = {}
f_unit = "MHz"


def main():
    global traces

    plt.style.use('default')

    fig = plt.figure()
    data_file = tk.filedialog.askopenfilename(
        filetypes=[('.SnP Touchstone File', '.S*P')])

    if not data_file:
        tk.simpledialog.messagebox._show("PyRF", "No file selected.")
        return
    try:
        data = rf.Network(data_file, f_unit=f_unit)
    except Exception:
        simpledialog.messagebox.showerror("PyRF", str(sys.exc_info()[1]))
        return

    traces.update({'S11': data.s11})
    traces.update({'S12': data.s12})
    traces.update({'S21': data.s21})
    traces.update({'S22': data.s22})

    plt.grid('both', 'both')

    fig.canvas.manager.toolmanager.add_tool('Add Marker', MarkButton)
    fig.canvas.manager.toolbar.add_tool('Add Marker', 'marker', MarkButton)
    fig.canvas.manager.toolmanager.add_tool('Remove Markers', RemoveButton)
    fig.canvas.manager.toolbar.add_tool('Remove Markers', 'marker',
                                        RemoveButton)
    for trace in traces.keys():
        fig.canvas.manager.toolmanager.add_tool(trace,
                                                GroupHideTool,
                                                gid=trace)
        fig.canvas.manager.toolbar.add_tool(trace, 'trace')

    fig.text(0.99, 0.01, str(data.frequency), fontsize=8, ha='right')

    fig.text(0.01, 0.035, time.ctime(os.path.getctime(data_file)), fontsize=8)

    fig.text(0.01, 0.01, data_file, fontsize=8)

    mark("S21", "1000mhz")
    plt.show()


class mark():
    def __init__(self, trace, frequency):
        self.frequency = frequency
        self.trace = trace
        self.y = y = float(traces[trace][frequency].s_db)
        self.x = x = float(traces[trace][frequency].frequency.f)
        self.plot = plt.plot(x, y, marker="|", color='black')
        self.text1 = plt.annotate(round(y, 4),
                                  xy=(x, y),
                                  textcoords="offset points",
                                  xytext=(0, 16),
                                  fontsize=10)

        f = str(traces[trace][frequency].frequency.center_scaled) + \
            " " + traces[trace].frequency.unit
        self.text2 = plt.annotate(f,
                                  xy=(x, y),
                                  textcoords="offset points",
                                  xytext=(0, 8),
                                  fontsize=8)
        marks.append(self)
        plt.draw()

    def remove(self):
        self.plot[0].remove()
        self.text1.remove()
        self.text2.remove()


class RemoveButton(ToolBase):
    def trigger(self, *args):
        for m in marks:
            m.remove()
        plt.draw()


class MarkButton(ToolBase):
    description = 'Place marker'
    default_keymap = 'm, M'

    def trigger(self, *args, **kwargs):
        res = markbox(traces_active, f_unit).show()
        if res is False:
            pass
        else:
            mark(res[1], str(res[0] + str.lower(f_unit)))


class GroupHideTool(ToolToggleBase):
    '''Show lines with a given gid'''
    description = 'Show by gid'
    default_toggled = True

    def __init__(self, *args, gid, **kwargs):
        self.gid = gid
        super().__init__(*args, **kwargs)

    def enable(self, *args):

        traces[self.gid].plot_s_db(label=self.gid, gid=self.gid)
        traces_active.update({self.gid: True})
        self.redraw()

    def disable(self, *args):
        for ax in self.figure.get_axes():
            for line in ax.get_lines():
                if line.get_gid() == self.gid:
                    line.remove()
        for mk in marks:
            if mk.trace == self.gid:
                mk.remove()
        del [traces_active[self.gid]]
        self.redraw()

    def redraw(self, *args):
        plt.tight_layout()
        ax = plt.gca()
        ax.relim()
        ax.autoscale()
        ax.legend(loc=1)
        self.figure.canvas.draw()


class markbox(simpledialog.Dialog):
    result = False

    def __init__(self, traces, fscale):
        tktop = self.top = tk.Toplevel()
        tktop.grid()
        tktop.grid_columnconfigure(0, pad=10)
        tktop.grid_columnconfigure(1, pad=10)

        self.textbox1 = tk.Entry(tktop)
        self.listbox1 = tk.Listbox(tktop, height=4)
        self.button_ok = tk.Button(
            tktop,
            command=lambda: self.ok_click(self.textbox1.get(),
                                          self.listbox1.get(tk.ACTIVE)),
            text='OK',
            width=10)
        self.button_cancel = tk.Button(tktop,
                                       command=lambda: self.cancel_click(),
                                       text='Cancel',
                                       width=10)

        self.button_ok.grid(row=3, column=2, padx=5, pady=5)
        self.button_cancel.grid(row=3, column=1, padx=5, pady=5)

        self.textbox1.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.listbox1.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        for trace in traces:
            self.listbox1.insert(tk.END, trace)

        self.label0 = tk.Label(tktop, text='Enter values to add trace:')
        self.label1 = tk.Label(tktop, text='Trace: ')
        self.label2 = tk.Label(tktop, text='Frequency (' + fscale + "):")
        self.label0.grid(row=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        self.label1.grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.label2.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.textbox1.focus()

    def ok_click(self, freq, trac):
        self.result = [freq, trac]
        self.top.destroy()

    def show(self):
        self.top.wait_window()
        return self.result

    def cancel_click(self, event=None):
        self.top.destroy()
        pass


if __name__ == "__main__":
    main()
    pass
