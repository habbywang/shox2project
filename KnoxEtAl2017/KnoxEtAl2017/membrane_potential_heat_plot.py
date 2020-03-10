#######################################
# membrane_potential_heat_plot.py
#
# Andrew Knox 2014
# 
# Python Script to make a heat plot from a data file created by Fspikewave.oc
# 
# The first value contains the number of time points, the next the number of cells
# Subsequent lines correspond to the list of membrane poteitnals for a given cell
########################################


from numpy import *
import numpy as np
from matplotlib import *
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec

#for 60x40inch image
#tf = 88 #title font
#stf = 44 #subtitle font
#af = 36 #axis font
#atf = 30 #tick font
#satf = 20 #small tick font (for color bar)

#for 18x12cm image
tf = 9 #title font
stf = 6 #subtitle font
af = 6 #axis font
atf = 6 #tick font
satf = 6 #small tick font (for color bar)


def compress_array(inarray,outarray,irows):
  subarrays = []
  for i in range(irows):
    s = slice(i,None,irows)
    subarrays.append(inarray[s,:])
  outarray = subarrays[0]
  for i in range(irows-1):
    outarray = maximum(outarray,subarrays[i+1])
  return outarray


data = open('membrane_data.txt','r')
ntimepoints = int(data.readline())
ncells = int(data.readline())

print "data:", ntimepoints,",", ncells

compress_factor = 1
mod_ntimepoints = ntimepoints - ntimepoints % compress_factor
 
tcvdata = np.zeros( (mod_ntimepoints,ncells) )
revdata = np.zeros( (mod_ntimepoints,ncells) )
pyvdata = np.zeros( (mod_ntimepoints,ncells) )
invdata = np.zeros( (mod_ntimepoints,ncells) )

for i in range(ncells):
  for j in range(ntimepoints):
    if j < mod_ntimepoints:
      tcvdata[j,i] = float(data.readline())
    else:
      data.readline()
  data.readline()

for i in range(ncells):
  for j in range(ntimepoints):
    if j < mod_ntimepoints:
      revdata[j,i] = float(data.readline())
    else:
      data.readline()
  data.readline()

for i in range(ncells):
  for j in range(ntimepoints):
    if j < mod_ntimepoints:
      pyvdata[j,i] = float(data.readline())
    else:
      data.readline()
  data.readline()

for i in range(ncells):
  for j in range(ntimepoints):
    if j < mod_ntimepoints:
      invdata[j,i] = float(data.readline())
    else:
      data.readline()
  data.readline()
    

data.close()

pyvdata = pyvdata[00000:30000,:]
#invdata = invdata[00000:30000,:]
tcvdata = tcvdata[00000:30000,:]
revdata = revdata[00000:30000,:]

#pyvdata = compress_array(pyvdata,pyvdata,compress_factor)
#invdata = compress_array(invdata,invdata,compress_factor)
#revdata = compress_array(revdata,revdata,compress_factor)
#tcvdata = compress_array(tcvdata,tcvdata,compress_factor)

pyvdata = transpose(pyvdata)
#invdata = transpose(invdata)
revdata = transpose(revdata)
tcvdata = transpose(tcvdata)

xaxis = linspace(0,ntimepoints/10000,num=ntimepoints/compress_factor)
yaxis = linspace(1,100,num=100)

#fig = plt.figure(figsize=[60,40])
fig = plt.figure(figsize=[6.7,4.47])
plt.suptitle("Raster Plot of Simulation with Baseline Parameters (Spindle Oscillation)",fontsize=tf)

#leaves space on right for colorbar
#gs = gridspec.GridSpec(1,3,width_ratios=[1,1,1.2])
gs = gridspec.GridSpec(3,2,width_ratios=[98,2])

plt.subplot(gs[0,0])
heatmap = plt.pcolormesh(xaxis,yaxis,pyvdata,cmap=mpl.cm.jet,vmin=-100,vmax=0)
plt.axis([0,ntimepoints/10000,1,100])
plt.title("Cortical Pyramidal Neurons (PY)", fontsize=stf, fontweight = 'bold')
#plt.xlabel("Time (s)",fontsize=af)
plt.ylabel("Neuron Index",fontsize=af)
plt.tick_params(labelsize=atf)

#plt.subplot(2,2,2)
#heatmap = plt.pcolormesh(invdata,cmap=mpl.cm.jet,vmin=-100,vmax=0)

plt.subplot(gs[1,0])
heatmap = plt.pcolormesh(xaxis,yaxis,revdata,cmap=mpl.cm.jet,vmin=-100,vmax=0)
plt.title("Thalamic Reticular Nucleus Neurons (RE)", fontsize=stf,fontweight='bold')
plt.axis([0,ntimepoints/10000,1,100])
#plt.xlabel("Time (s)",fontsize=af)
plt.ylabel("Neuron Index",fontsize=af)
plt.tick_params(labelsize=atf)

plt.subplot(gs[2,0])
heatmap = plt.pcolormesh(xaxis,yaxis,tcvdata,cmap=mpl.cm.jet,vmin=-100,vmax=0)
plt.title("Thalamocortical Neurons (TC)", fontsize=stf, fontweight='bold')
plt.axis([0,ntimepoints/10000,1,100])
plt.xlabel("Time (s)",fontsize=af)
plt.ylabel("Neuron Index",fontsize=af)
plt.tick_params(labelsize=atf)

#gives space for top title
gs.tight_layout(fig,rect=[0,0,1,0.97],h_pad=0.1)
#plt.subplots_adjust(top=0.85)

axes = plt.subplot(gs[:,1])
cb = plt.colorbar(cax=axes)
cb.set_label("mV",fontsize=satf,labelpad=-1)
cb.ax.tick_params(labelsize=satf)

gs.tight_layout(fig,rect=[0,0,1,0.97],h_pad=0.1)

plt.savefig('figure 2b',dpi=1200)




    
