#===============================================================================
#     This file is part of CIMA.
#
#     CIMA is a software designed to help the user in the manipulation
#     and analyses of genomic super resolution localisation data.
#
#      Copyright  2019-2023
#
#                Authors: Irene Farabella
#
#
#
#===============================================================================

from CIMA.segments.SegmentGaussian import TransformBlurrer
from CIMA.segments.SegmentInfo import Segment
from CIMA.maps import MapFeatures as MF
from CIMA.parsers import ParserCSV as Parser
import os
TB=TransformBlurrer()
from scipy.stats import linregress,ttest_ind,wilcoxon,mannwhitneyu,ks_2samp
from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np
import random

def statConvert(s):
	from decimal import Decimal
	P="{:.2E}".format(Decimal(s))
	if float(s) <=0.0001:
		stat="***"
	elif float(s) <=0.001:
		stat="***"
	elif float(s) <=0.01:
		stat="**"
	elif float(s) <=0.05:
		stat="*"
	else:
		stat=P
	return stat

def power_law(x, a, b):
    return a*np.power(x, b)

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c
#Y=ax**2+b
def func_sqrt(x, m, c, c0 ):
    return c0 + x** 1.0/m * c
#Y=a*x** 1.0/m

def func2(x, a, b, c):
    return a * np.exp(-b * x) + c

def func_inverse1(x, m, c, c0):
    return c0 + m* (1.0/x**2) * c

def func(x, a, b, c, d):
    return a*np.exp(-c*(x-b))+d

def welch_ttest(x, y):
    #https://pythonfordatascienceorg.wordpress.com/welch-t-test-python-pandas/
    ## Welch-Satterthwaite Degrees of Freedom ##
    dof = (x.var()/x.size + y.var()/y.size)**2 / ((x.var()/x.size)**2 / (x.size-1) + (y.var()/y.size)**2 / (y.size-1))

    t, p = stats.ttest_ind(x, y, equal_var = False)

    #print("""Welch's t-test= %.4f, p-value = %.4f, Degrees of Freedom= %.4f""" %(t,p,dof))
    return t, p,dof


def Create_Random_Hom_Ratio(featuresel_list,rdeed1=1,samplesize=1000):
	#greater vrs smaller

    ration_random=[]
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(featuresel_list,len(featuresel_list))
        for r in range(len(featuresel_list)):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]>Pf[1]:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)
                    else:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)

    if len(featuresel_list)>len(ration_random):
        print("Change random seed")
        print(len(featuresel_list),len(ration_random))
    else:
        return ration_random

def Create_Random_Hom_Ratio_smalloverlarger(featuresel_list,rdeed1=1,samplesize=1000):


    ration_random=[]
    LEN=len(list(featuresel_list))
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(list(featuresel_list),LEN)
        for r in range(LEN):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]>Pf[1]:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)
                    else:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)

    if LEN>len(ration_random):
        print("Change random seed")
        print(LEN,len(ration_random))
    else:
        return ration_random

def Create_Random_Hom_Ratio_largeroversmaller(featuresel_list,rdeed1=1,samplesize=1000):


    ration_random=[]
    LEN=len(list(featuresel_list))
    random.seed(rdeed1)
    for i in range(samplesize):
        random_2=random.sample(list(featuresel_list),LEN)
        for r in range(LEN):
            if len(random_2)>=2:
                Mf,Pf= random.sample(random_2, 2)
                if Mf[0]==Pf[0]:
                    pass
                else:
                    random_2.remove(Mf)
                    random_2.remove(Pf)
                    if Mf[1]<Pf[1]:
                        rat=Pf[1]/Mf[1]
                        ration_random.append(rat)
                    else:
                        rat=Mf[1]/Pf[1]
                        ration_random.append(rat)

    if LEN>len(ration_random):
        print("Change random seed")
        print(LEN,len(ration_random))
    else:
        return ration_random


def Create_Random_Hom_Ratio_Paternal_Origin(listhomfeature,rdeed1=16734,rdeed2=3535,samplesize=100,parentalnorm=False):
    ration_random=[]
    LEN=len(list(listhomfeature))
    for i in range(samplesize):
        m,p,n=zip(*listhomfeature)
        Matpool=list(zip(m,n))
        Patpool=list(zip(p,n))
        for r in range(LEN):
            random.seed(rdeed1)
            Mf= random.sample(Matpool, 1)[0]
            random.seed(rdeed2)
            Pf= random.sample(Patpool, 1)[0]    
            if Mf[1]==Pf[1]:
                pass
            else:
                #print (Mf)
                Matpool.remove(Mf)
                Patpool.remove(Pf)
                if parentalnorm:
                    ration_random.append(((Mf[0]/Pf[0])/Mf[0]))
                else:
                    ration_random.append((Mf[0]/Pf[0])) 
    if len(listhomfeature)>len(ration_random):
        print("Change random seed")
        print(len(listhomfeature),len(ration_random))
    else:
        return ration_random

def makeAxesLabelsLog():
    xlims = plt.gca().get_xlim()
    ylims = plt.gca().get_ylim()
    xticks1 = np.arange(np.ceil(xlims[0]),np.floor(xlims[1])+0.1,1.0)
    yticks1 = np.arange(np.ceil(ylims[0]),np.floor(ylims[1])+0.1,1.0)
    _ = plt.xticks(xticks1, [r"$10^{{ {:0.0f} }}$".format(int(xticks1[i])) for i in range(len(xticks1))])
    _ = plt.yticks(yticks1, [r"$10^{{ {:0.0f} }}$".format(int(yticks1[i])) for i in range(len(yticks1))])


def getLogLinearRegression(vals1, vals2):
    import scipy
    arr1 = np.log10(vals1)
    arr2 = np.log10(vals2)
    where_ok = (np.isfinite(arr1)*np.isfinite(arr2)).astype('bool')
    lr= scipy.stats.linregress(arr1[where_ok],arr2[where_ok])
    return lr.intercept, lr.slope

def plotLine(intercept, slope, xlim0, xlim1, num=10, **kwargs):
    xs = np.linspace(xlim0, xlim1, num)
    ys = intercept + xs*slope
    plt.plot(xs, ys, **kwargs)
    
def plotLogWithKdeColors(arr1,arr2,log=True, **kwargs):
    import scipy
    if log:
        arr1_log = np.log10(arr1)
        arr2_log = np.log10(arr2)
        where_ok = (np.isfinite(arr1_log)*np.isfinite(arr2_log)).astype('bool')
        arr1_log = arr1_log[where_ok]
        arr2_log = arr2_log[where_ok]
    else:
        arr1_log = arr1
        arr2_log = arr2
    sta = np.vstack([arr1_log,arr2_log])
    #z = scipy.stats.gaussian_kde(sta)(sta)
    g = sns.scatterplot(x=arr1_log, y=arr2_log, palette='plasma', s=20, legend=False)  # hue=z
    sns.despine()
    # _ = plt.legend(title='Density')
    # sns.move_legend(g, "upper left", bbox_to_anchor=(1, 1))
    # plt.colorbar(g)
    # g = sns.kdeplot(x=arr1, y=arr2, levels=5,fill=True,alpha=0.6,cut=2,)
    intercept, slope = getLogLinearRegression(arr1, arr2)
    print('pearson: ', scipy.stats.pearsonr(arr1_log,arr2_log).statistic)
    print('slope: ', slope)
    xlims = plt.gca().get_xlim()
    plotLine(intercept, slope, xlims[0], xlims[1], c='black', ls='--', **kwargs)
    makeAxesLabelsLog()