#!/usr/bin/python3
import math
import numpy as np
import matplotlib.pyplot as plt



class LFSpeaker:
    def __init__(self):
        self.Vas = 0
        self.Fs = 0
        self.Qts = 0
        self.SA = 0
        self.Sd = 0
        self.Xmax = 0

    def setter(self, Vas, Fs, Qts, Sd, Xmax):
        self.Vas = float(Vas)
        self.Fs = float(Fs)
        self.Qts = float(Qts)
        self.Sd = float(Sd)
        self.Xmax = float(Xmax)
        self.SA = float(math.pi*((0.5*self.Sd)**2))

    def recommend_order(self):
        if self.Qts <= 0.4:
            return 'Vented' 
        if self.Qts <= 0.5:
            return 'Vented/Sealed'
        if self.Qts <= 0.7:
            return 'Sealed'
        if self.Qts < 1:
            return 'Transmission Line'
        else:
            return 'Open Baffle'
        
    def clear(self):    
        self.Vas = 0
        self.Fs = 0
        self.Qts = 0
        self.SA = 0
        
class SealedEnclosure:
    def __init__(self):
        self.Qtc = 0
        self.Vb = 0
        self.Fc = 0
        self.F3 = 0
        self.tf_list = []
        self.figure = plt.figure(figsize=(8.15, 2.9))
        self.xticks = np.arange(0, 200, 10)
        self.yticks = np.arange(-18, 18, 3)
        

    def qtc_setter(self, value):
        self.Qtc = float(value)

    def volume_calculate(self, speaker):
        vas = speaker.Vas
        qts = speaker.Qts
        fs = speaker.Fs
        alpha = (self.Qtc/qts)**2 - 1
        self.Vb = float(vas/alpha)
        self.Fc = int((self.Qtc*fs)/qts)
        return self.Vb, self.Fc
    
    def tf_values(self, speaker):
        for f in range(1, 200):
            value = 10*(math.log10(((f/speaker.Fs)**4)/(((1 + speaker.Vas/self.Vb) - 
                    ((f/speaker.Fs)**2))**2 + ((1/speaker.Qts)*(f/speaker.Fs))**2)))
            self.tf_list.append(value)
        for item in self.tf_list[::-1]:
            if int(item) == -3:
                self.F3 = self.tf_list.index(item) + 1
                break

    def tf_draw_axis(self):
        self.axis = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.axis.set_xticks(self.xticks)
        self.axis.set_yticks(self.yticks)
        self.axis.set_xticklabels(self.xticks)
        self.axis.set_yticklabels(self.yticks)
        self.axis.set_xlim(xmin=10, xmax=200)
        self.axis.set_ylim(ymin=-18, ymax=20)
        self.axis.grid()

    def tf_plot(self):    
        self.axis.plot(np.arange(1, 200), self.tf_list)
        

    def clear(self):
        self.Qtc = 0
        self.Vb = 0
        self.Fc = 0
        self.F3 = 0
        self.isobaric = False
        self.tf_list.clear()
        self.figure.clf()
        
class VentedEnclosure:
    def __init__(self):
        self.Ql = 7
        self.Vb = 0
        self.F3 = 0
        self.Fb = 0
        self.Pd = 0
        self.tf_list = []
        self.figure = plt.figure(figsize=(8.15, 2.8))
        self.xticks = np.arange(0, 200, 10)
        self.yticks = np.arange(-18, 18, 3)
        

    def volume_calculate(self, speaker):
        self.Vb = 20*((speaker.Qts**3.3)*speaker.Vas)
        self.Fb = int(((speaker.Vas/self.Vb)**0.31)*speaker.Fs)
        self.Pd = (((speaker.SA*(speaker.Xmax/1000000))*self.Fb)**0.5)*39.37
        self.F3 = int(((speaker.Vas/self.Vb)**0.44)*speaker.Fs)
        
    
    def tf_values(self, speaker):
        for f in range(1, 200):
            value = 10*math.log10((f**8/(((self.Fb**4)*(speaker.Fs**4)))) / (((f**4/((self.Fb**2)*(speaker.Fs**2))) - (f**2*(1/(speaker.Fs**2) + ((1+speaker.Vas/self.Vb)/self.Fb**2) + 1/(self.Fb*speaker.Fs*self.Ql*speaker.Qts))) + 1)**2 
            + ((((-f)**3)*(1/((speaker.Fs**2)*self.Fb*self.Ql) + 1/((self.Fb**2)*speaker.Fs*speaker.Qts)) + f*(1/(speaker.Fs*speaker.Qts) + 1/(self.Fb*self.Ql)))**2)))
            self.tf_list.append(value)
        return self.tf_list
    
    def tf_draw_axis(self):
        self.axis = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.axis.set_xticks(self.xticks)
        self.axis.set_yticks(self.yticks)
        self.axis.set_xticklabels(self.xticks)
        self.axis.set_yticklabels(self.yticks)
        self.axis.set_xlim(xmin=10, xmax=200)
        self.axis.set_ylim(ymin=-18, ymax=20)
        self.axis.grid()

    def tf_plot(self):
        self.axis.plot(np.arange(1, 200), self.tf_list)
        

    def clear(self):
        self.Vb = 0
        self.F3 = 0
        self.Fp = 0
        self.tf_list.clear()
        self.figure.clf()
        
