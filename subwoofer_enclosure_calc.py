#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox
from data_calculations import SealedEnclosure, VentedEnclosure, LFSpeaker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import db_get, db_add, db_remove
import ttkthemes

speaker_inst = LFSpeaker()
senclosure_inst = SealedEnclosure()
venclosure_inst = VentedEnclosure()    

def tv_insert():
    index = 0
    for speaker in db_get():
        tv.insert('', index, iid=None, 
                  values=(speaker[0], speaker[1], speaker[2], 
                          speaker[3], speaker[4], speaker[5]))
        index += 1

def inserter(widget, text):
    try:
        text = round(float(text), 2)
    except:
        pass
    widget.configure(state=NORMAL)
    widget.insert(0, text)
    widget.configure(state=DISABLED)

def clearer():
    tabs = [speaker, sealed, vented]
    speaker_inst.clear()
    senclosure_inst.clear()
    venclosure_inst.clear()
    senclosure_inst.tf_draw_axis()
    venclosure_inst.tf_draw_axis()
    se_canvas.draw()
    ve_canvas.draw()
    for item in tabs:
        for child in item.winfo_children():
            if child.winfo_class() == 'TEntry':
                if child.state():
                    child.configure(state=NORMAL)
                    child.delete(0, END)
                    child.configure(state=DISABLED)
                else:
                    child.delete(0, END)

def add_speaker():
    name, vas, qts, fs, Sd, Xmax = name_e.get(), vas_e.get(), qts_e.get(), \
                fs_e.get(), Sd_e.get(), xmax_e.get()
    db_add(name, vas, qts, fs, Sd, Xmax)
    for entry in tv.get_children():
        tv.delete(entry)
    tv_insert()
    clearer()

def remove_speaker():
    name = tv.item(tv.focus())['values'][0]
    db_remove(name)
    for entry in tv.get_children():
        tv.delete(entry)
    tv_insert()
    clearer()

def calculations():
    if ve_vb_e.get():
        messagebox.showerror('Values not cleared.', 'Clear all values before making another calculation.')
        return
    vas, qts, fs, Sd, qtc, Xmax = vas_e.get(), qts_e.get(), \
                fs_e.get(), Sd_e.get(), qtc_e.get(), xmax_e.get()
    try:
        if float(vas) <= 0 or float(qts) <= 0 or int(fs) <= 0 or float(Sd) <= 0 or float(qts) <= 0 or float(Xmax) == 0:
            messagebox.showerror('Invalid Values', 'Values must be greater than zero.')
            return
    except ValueError:
        messagebox.showerror('Invalid Values', 
                             'All values must be positive integers or floating point numbers separated by a dot.')
        return
    if float(qts) >= float(qtc):
        messagebox.showerror('Invalid Values', 'Qtc must be greater than Qts.')
        return
    
    speaker_inst.setter(vas, fs, qts, Sd, Xmax)
    inserter(rc_e, speaker_inst.recommend_order())
    senclosure_inst.qtc_setter(qtc)
    senclosure_inst.volume_calculate(speaker_inst)
    senclosure_inst.tf_values(speaker_inst)
    senclosure_inst.tf_draw_axis()
    senclosure_inst.tf_plot()
    se_canvas.draw()
    inserter(se_vb_e, senclosure_inst.Vb)
    inserter(se_fc_e, senclosure_inst.Fc)
    inserter(se_f3_e, senclosure_inst.F3)
    venclosure_inst.volume_calculate(speaker_inst)
    venclosure_inst.tf_values(speaker_inst)
    venclosure_inst.tf_draw_axis()
    venclosure_inst.tf_plot()
    ve_canvas.draw()
    inserter(ve_vb_e, venclosure_inst.Vb)
    inserter(ve_fb_e, venclosure_inst.Fb)
    inserter(ve_f3_e, venclosure_inst.F3)
    inserter(pd_e, venclosure_inst.Pd)
       


main_window = Tk()
main_window.title('Subwoofer Enclosure Calculator')
main_window.geometry('820x376')
main_window.resizable(False, False)
main_window.configure(background='white')

ttkthemes.ThemedStyle(main_window, theme='clam')


nb = ttk.Notebook(main_window)
nb.pack(side=TOP, fill=BOTH)
speaker = ttk.Frame(nb)
sealed = ttk.Frame(nb)
vented = ttk.Frame(nb)
nb.add(speaker, text='Speaker')
nb.add(sealed, text='Sealed Enclosure')
nb.add(vented, text='Vented Enclosure')


vas_l = ttk.Label(speaker, text='Speaker Vas (liter):', width=24)
vas_e = ttk.Entry(speaker, justify=LEFT, width=24)
vas_l.grid(row=0, column=0, pady=3, padx=3)
vas_e.grid(row=0, column=1, pady=3, padx=3)
qts_l = ttk.Label(speaker, text='Speaker Qts (unitless):', width=24)
qts_e = ttk.Entry(speaker,  justify=LEFT, width=24)
qts_l.grid(row=0, column=2, pady=3, padx=3)
qts_e.grid(row=0, column=3, pady=3, padx=3)
fs_l = ttk.Label(speaker, text='Speaker Fs (Hz):', width=24)
fs_e = ttk.Entry(speaker,  justify=LEFT, width=24)
fs_l.grid(row=1, column=0, pady=3, padx=3)
fs_e.grid(row=1, column=1, pady=3, padx=3)
Sd_l = ttk.Label(speaker, text='Speaker Diameter (cm):', width=24)
Sd_e = ttk.Entry(speaker,justify=LEFT, width=24)
Sd_l.grid(row=1, column=2, pady=3, padx=3)
Sd_e.grid(row=1, column=3, pady=3, padx=3)
xmax_l = ttk.Label(speaker, text='Xmax (mm):', width=24)
xmax_e = ttk.Entry(speaker,  justify=LEFT, width=24)
xmax_l.grid(row=2, column=0, pady=3, padx=3)
xmax_e.grid(row=2, column=1, pady=3, padx=3)
qtc_l = ttk.Label(speaker, text='Sealed Qtc (unitless):', width=24)
qtc_e = ttk.Entry(speaker, justify=LEFT, width=24)
qtc_l.grid(row=2, column=2, pady=3, padx=3)
qtc_e.grid(row=2, column=3, pady=3, padx=3)
name_l = ttk.Label(speaker, text='Speaker Name (DB):', width=24)
name_e = ttk.Entry(speaker, justify=LEFT, width=24)
name_l.grid(row=3, column=0, pady=3, padx=3)
name_e.grid(row=3, column=1, pady=3, padx=3)
rc_l = ttk.Label(speaker, text='Best configuration:', width=24)
rc_e = ttk.Entry(speaker, state=DISABLED, justify=LEFT, foreground='black', width=24)
rc_l.grid(row=3, column=2, pady=3, padx=3)
rc_e.grid(row=3, column=3, pady=3, padx=3)


calc_button = ttk.Button(speaker, text='Calculate', command=calculations, width=48)
calc_button.grid(row=5, column=0, columnspan=2, pady=3, padx=3)
clear_button = ttk.Button(speaker, text='Clear', command=clearer, width=48, style='rem.TButton')
clear_button.grid(row=5, column=2, columnspan=2, pady=3, padx=3)

se_vb_l = ttk.Label(sealed, text='Enclosure Volume (liter):', width=24)
se_vb_e = ttk.Entry(sealed, state=DISABLED, justify=LEFT, foreground='black', width=24)
se_vb_l.grid(row=0, column=0, pady=3, padx=3)
se_vb_e.grid(row=0, column=1, pady=3, padx=3)
se_fc_l = ttk.Label(sealed, text='Tuning Frequency (Hz):', width=24)
se_fc_e = ttk.Entry(sealed, state=DISABLED, justify=LEFT, foreground='black', width=24)
se_fc_l.grid(row=1, column=0, pady=3, padx=3)
se_fc_e.grid(row=1, column=1, pady=3, padx=3)
se_f3_l = ttk.Label(sealed, text='F3 Frequency (Hz):', width=24)
se_f3_e = ttk.Entry(sealed, state=DISABLED, justify=LEFT, foreground='black', width=24)
se_f3_l.grid(row=0, column=2, pady=3, padx=3)
se_f3_e.grid(row=0, column=3, pady=3, padx=3)

ve_vb_l = ttk.Label(vented, text='Enclosure Volume (liter):', width=24)
ve_vb_e = ttk.Entry(vented, state=DISABLED, justify=LEFT, foreground='black', width=24)
ve_vb_l.grid(row=0, column=0,pady=3, padx=3)
ve_vb_e.grid(row=0, column=1,pady=3, padx=3)
ve_fb_l = ttk.Label(vented, text='Tuning Frequency (Hz):', width=24)
ve_fb_e = ttk.Entry(vented, state=DISABLED, justify=LEFT, foreground='black', width=24)
ve_fb_l.grid(row=1, column=0,pady=3, padx=3)
ve_fb_e.grid(row=1, column=1,pady=3, padx=3)
ve_f3_l = ttk.Label(vented, text='F3 Frequency (Hz):', width=24)
ve_f3_e = ttk.Entry(vented, state=DISABLED, justify=LEFT, foreground='black', width=24)
ve_f3_l.grid(row=0, column=2,pady=3, padx=3)
ve_f3_e.grid(row=0, column=3,pady=3, padx=3)
pd_l = ttk.Label(vented, text='Minimum Port Diameter (cm): ', width=24)
pd_e = ttk.Entry(vented, state=DISABLED, justify=LEFT, foreground='black', width=24)
pd_l.grid(row=1, column=2,pady=3, padx=3)
pd_e.grid(row=1, column=3,pady=3, padx=3)

senclosure_inst.tf_draw_axis()
venclosure_inst.tf_draw_axis()
ve_canvas = FigureCanvasTkAgg(venclosure_inst.figure, master=vented)
ve_canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)
se_canvas = FigureCanvasTkAgg(senclosure_inst.figure, master=sealed)
se_canvas.get_tk_widget().grid(row=3, column=0, columnspan=4)

tv_columns = ['Name', 'Vas', 'Qts', 'Fs', 'Sd', 'Xmax']

tv = ttk.Treeview(speaker, selectmode='browse', columns=tv_columns, show='headings', height=6)
for col in tv['columns']:
    tv.heading(col, text=col)
    tv.column(col, width=132)
tv.grid(row=6, column=0, columnspan=4,pady=3, padx=3)
tv_insert()
tv_sc = Scrollbar(tv, orient=VERTICAL, command=tv.yview)
tv_sc.place(relx=0.98, rely=0.18, relheight=0.82)
tv.configure(yscrollcommand=tv_sc.set)

add_button = ttk.Button(speaker, text='Add Speaker', width=48, command=add_speaker)
add_button.grid(row=7, column=0, columnspan=2)
remove_button = ttk.Button(speaker, text='Remove Speaker', width=48, command=remove_speaker, style='rem.TButton')
remove_button.grid(row=7, column=2, columnspan=2)

main_window.mainloop()