"""
Default script for the plotting the results of a single ProDiMo model.

A script called `pplot`, which can directly by called from the command line,
will be installed automatically during the installation process.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
import numpy as np
import time as time



import prodimopy.plot as pplot
import prodimopy.read as pread


# the above two statement are for phyton2 pyhton3 compatibility.
# With this statmens you can write python3 code and it should also work
# in python2 (depends on your code)
# this is for the argument parser included in python
# this is for the PDF output
# Thats the prodimpy modules
# The first one is for reading a ProDiMo Model
# The second one is for plotting
# The main routine is require to have an entry point.
# It is not necessary if you want to write your own script.
def main(args=None):
  ###############################################################################
  # Command line parsing
  # this is optional you do not have to do it this way.
  # You can use the prodimopy module in any way you want
  parser=argparse.ArgumentParser(description='prodimopy simple example for plotting ')
  parser.add_argument('-dir',required=False,default=".",help='The directory of the input files DEFAULT: "."')
  parser.add_argument('-output',required=False,default="./out.pdf",help='The output filename, DEFAULT: "./out.pdf"')
  parser.add_argument('-td_fileIdx',required=False,default=None,help='The index for the time dependent output file e.g. "01", DEFAULT: None')
  parser.add_argument('-mplstyle',required=False,default="prodimopy",help='Use a mpl style file, DEFAULT: prodimopy')
  args=parser.parse_args()

  start_time = time.time()

  print("-dir: ",args.dir)
  print("-output: ",args.output)
  print("-td_fileIdx: ",args.td_fileIdx)

  # thats for time dependent models, also optional
  outfile=args.output
  if args.td_fileIdx!=None:
    outfile=outfile.replace(".pdf","_"+args.td_fileIdx+".pdf")

  # This reads the output of a ProDiMo model
  # there are more optional arguments
  model=pread.read_prodimo(args.dir,td_fileIdx=args.td_fileIdx)

  # loads the prodimopy style
  pplot.load_style(args.mplstyle)

  # some new feature ....   
  # mpl.style.use(['fast'])
  # mpl.rcParams['path.simplify'] = True
  # mpl.rcParams['path.simplify_threshold'] = 1.0

  # Here the plotting happens. This produces one pdf file
  with PdfPages(outfile) as pdf:
    # Init the prodimo plotting module for one model and an optional title
    # it is required to pass a PdfPages object
    pp=pplot.Plot(pdf,title=model.name)

    # make some contours we need later on
    contAV=pplot.Contour(model.AV,[1.0,10],showlabels=True,label_fmt=r" $A_V$=%.0f ",colors=pp.pcolors["red"])
    # some style for the contour plots. This uses zr for height, and log for x 
    contstyle={"zr" : True, "xlog" : True, "ylog" : False}

    pp.plot_starspec(model)
    pp.plot_grid(model)
    pp.plot_grid(model,**contstyle)
    # This plots the Stellar spectrum
    pp.plot_dust_opac(model)

    # pp.plot_NH(model,sdscale=True,ylim=[5.e27,5.e29])
    pp.plot_NH(model,sdscale=True,ylim=[1.e20,None],xlog=True)

    pp.plot_cont(model,model.nHtot,"nHtot",oconts=[contAV],zlim=[1.e4,None],extend="min",**contstyle)
    pp.plot_cont(model,model.rhod,"rhog",zlim=[1.e-25,None],extend="both",**contstyle)
    pp.plot_cont(model,model.rhod,"rhod",zlim=[1.e-25,None],extend="both",**contstyle)

    pp.plot_cont(model,model.d2g,"d2g",zlim=[1.e-6,0.9],extend="both",**contstyle)

    levels=[10,20,50,100,300,1000]
    pp.plot_cont(model,model.td,"td",zlim=[10,3500],extend="both",clevels=levels,clabels=map(str,levels),**contstyle)

    levels=[10,20,50,100,300,1000,3000]
    pp.plot_cont(model,model.tg,"tg",zlim=[10,3500],extend="both",clevels=levels,clabels=map(str,levels),**contstyle)

    pp.plot_cont(model,model.chiRT,"chiRT",contour=True,zlim=[1.e-6,1.e6],extend="both",cb_format="%.0f",oconts=[contAV],**contstyle)

    if np.max(model.zetaX)>1.e-99:
      contCR=pplot.Contour(model.zetaCR,[1.e-17],showlabels=True,label_fmt=r" $\zeta_{CR}$=%.0e ",colors="white",linestyles="dashed")
      pp.plot_cont(model,model.zetaX,"zetaX",contour=True,zlim=[1.e-19,1.e-13],extend="both",oconts=[contCR],**contstyle)

    pp.plot_heat_cool(model)
    pp.plot_cont(model,model.taucool,"taucool",zlim=[1.e-2,None],extend="min",**contstyle)
    pp.plot_cont(model,model.tauchem,"tauchem",zlim=[1.e-2,1.e7],extend="both",**contstyle)


    # Maybe make this a command line parameter, or some option to plot all of them
    splist=["e-","H","H+","H-","H2", "C+","C","CO","CO2","CH3OH","O","O+","O2","H2O","N","N+","N2","HCN","HCO+","HN2+",
            "CO#","CO2#","H2O#","N2#"]

    for spname in splist:
      if spname in model.spnames:
        maxabun=np.max(model.getAbun(spname))
        zlim=[maxabun/1.e6,maxabun]
        pp.plot_abuncont(model,spname,zlim=zlim ,extend="both",rasterized=True,nbins=40,**contstyle)

    # observables if available
    if model.sed is not None:
      pp.plot_sed(model,sedObs=model.sedObs)
      # model.rhod, r"$\mathsf{\rho_{dust} [g\;cm^{-3}]}$
      pp.plot_sedAna(model,zr=True,xlog=True,ylog=False)

    # line fluxes stuff
    if model.lines is not None:
      nplot=int(len(model.lines)/20)+1
      for i in range(nplot):
        lineidents=[[line.ident,line.wl] for line in model.lines[i*20:(i+1)*20]]
        pp.plot_lines(model,lineidents,showBoxes=False,lineObs=model.lineObs,useLineEstimate=False)

      for line in model.lines:
        pp.plot_lineprofile(model,line.wl,line.ident,lineObs=model.lineObs)

      for line in model.lines:
        ident=line.ident
        # this is likely not complete
        if ident=="OI": ident="O"
        if ident=="CII": ident="C+"

        if line.species in model.spnames:
          nspmol=model.nmol[:,:,model.spnames[line.species]]
          label=line.species
        else:
          nspmol=model.nmol[:,:,model.spnames["H2"]]
          label="H2"
        max=np.max(nspmol)
        zlim=[max/1.e11,max/1000]
        pp.plot_line_origin(model,[[ident,line.wl]],nspmol,
                        label=r"log $n_{"+pplot.spnToLatex(label)+r"}\,[cm^{-3}]$",
                        zlim=zlim,extend="both",showContOrigin=True,rasterized=True)

    # Provide information on the 5 strongest lines in ALMA band 6
    # Get the 10 strongest waterlines in the MIRI wavelength range.
    # Here we have to deal with ortho and para.
    lines=model.selectLineEstimates(None,wlrange=[1100,1400])
    lines=sorted(lines,key=lambda x: x.flux,reverse=True)[:5]
    print()
    print("Strongest lines in ALMA band 6 (from line estimate)")
    print(*lines, sep="\n")

    lines=model.selectLineEstimates(None,wlrange=[5,15])
    lines=sorted(lines,key=lambda x: x.flux,reverse=True)[:20]
    print()
    print("Strongest lines in part of the MIRI range (5 to 15, from line estimate)")
    print(*lines, sep="\n")

    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
    # Plot radiation field at certain wavelengths (here simply done with the index)
    # pp.plot_cont(model,model.radFields[:,:,0],zr=False,xlog=False,label="lam="+str(model.lams[0]))
    # pp.plot_cont(model,model.radFields[:,:,5],zr=False,xlog=False,label="lam="+str(model.lams[5]))
