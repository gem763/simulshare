from django.shortcuts import render
from quanty.model import backtester as q
#from quanty.model import backtester_base as q_base
#from quanty.model import db_manager as dm
#from quanty.model import plotter as pltr
from quanty.model import setting
from quanty.model.portfolio import Port
#from quanty.model.dual_momentum import DualMomentumSelector, DualMomentumPort

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
from IPython.core.debugger import set_trace


# Create your views here.

def view_simul(request):
    return render(request, 'view_simul.html')


def view_simul_result(request):
    result = run()

    start = result.start
    stats = result.get_stats().to_html()

    strats = ['BND_US_Long', 'ACWI', 'DualMomentum']
    names = ['US Treasury long', 'ACWI', 'Global multiasset']
    color = ['k', 'orange', 'r']
    fig_cum = result.plot_cum(strats, names=names, color=color, logy=False).get_figure()
    #set_trace()
    fig_stats = result.plot_stats(strats, names=names, color=color)#.get_figure()
    fig_weight = result.plot_weight([2015, 2018]).get_figure()

    #fig, ax = plt.subplots()
    #pd.DataFrame([1,2,3,4,3]).plot(ax=ax)
    html_fig_cum = mpld3.fig_to_html(fig_cum, template_type='general')
    html_fig_stats = mpld3.fig_to_html(fig_stats, template_type='general')
    html_fig_weight = mpld3.fig_to_html(fig_weight, template_type='general')

    context = {'start':start, 'fig_cum':html_fig_cum, 'fig_stats':html_fig_stats, 'fig_weight':html_fig_weight}
    return render(request, 'view_simul_result.html', context)


def run():
    #print(pd.read_pickle('db.pkl').tail())
    gmm = q.Backtester(
        setting.base_params(pd.read_pickle('db.pkl')),
        w_type='inv_ranky2',
        rebal_style='cum',
        n_picks=10,
        assets=setting.assets_global_multiasset,
        sig_w_base=[1,0,0,0,0,0,1,0,0,1,2,3], #[1,0,0,0,0,0,1,0,0,0.25*4,0.25*6,0.25*12], #
        sig_w_dynamic=True, #False,
        sig_dyn_fwd=21*np.array([1,2,3]),
        #sig_dyn_m_backs=24,
        follow_trend=None, #(20,60),
        follow_trend_market=(20,60),
        follow_trend_supporter=(60,250),
        strong_condition=True,
        market='BND_US_HY', #'ACWI',
        supporter='BND_US_Long',
        cash_equiv='BND_US_Tbill',
        start='2007-12-31',
        end='2018-09-30',
        losscut=0.05,
        profitake_sigma=3,
        rentry_sigma=2,
    )
    return gmm
