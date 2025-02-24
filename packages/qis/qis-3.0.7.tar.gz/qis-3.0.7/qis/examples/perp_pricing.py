import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import qis as qis
from bbg_fetch import fetch_field_timeseries_per_tickers, fetch_index_members_weights, fetch_bonds_info


index_ticker = 'I31415US Index'

end_dates = ['20180101', '20190101', '20200101', '20210101', '20220101', '20230101', '20240101', '20250101', '20250106']

data_out = {}
weighted_resets = []
for idx, end_date in enumerate(end_dates):
    if idx > 0:
        members = fetch_index_members_weights(index_ticker, END_DATE_OVERRIDE=end_dates[idx-1])
        corp_index = [f"{x} corp" for x in members.index]
        members.index = corp_index
        """
        amt_outstanding = fetch_bonds_info(isins=members.index.to_list(), fields=['amt_outstanding'],
                                           END_DATE_OVERRIDE=end_dates[idx-1])['amt_outstanding']
        amt_outstanding = amt_outstanding.loc[members.index]
        amt_outstanding.index = corp_index
        """
        prices = fetch_field_timeseries_per_tickers(tickers=corp_index,
                                                    start_date=pd.Timestamp(end_dates[idx-1]),
                                                    end_date=pd.Timestamp(end_date),
                                                    freq='B')
        prices = prices.resample('W-WED').last()
        # market_value = prices.multiply(amt_outstanding, axis=1)
        #market_value.divide(np.nansum(market_value, axis=1, keepdims=True), axis=1)
        is_reset = (prices > 100).astype(float)
        market_weights = members.iloc[:, 0]
        weighted_reset = is_reset.multiply(market_weights, axis=1)
        weighted_reset = weighted_reset.sum(1)
        weighted_resets.append(weighted_reset)
        data_out[f"{end_dates[idx-1]} members"] = members
        data_out[f"{end_date} prices"] = prices
        data_out[f"{end_date} is_reset"] = is_reset

weighted_resets = pd.concat(weighted_resets)
weighted_resets = weighted_resets.loc[~weighted_resets.index.duplicated(keep='first')]
weighted_resets = weighted_resets.to_frame('weighted_par_reset %')
print(weighted_resets)

data_out['weighted_resets'] = weighted_resets
qis.save_df_to_excel(data=data_out, file_name='perp_pricing')

with sns.axes_style("darkgrid"):
    fig, ax = plt.subplots(1, 1, figsize=(15, 8), tight_layout=True)
    qis.plot_time_series(weighted_resets,
                         title='weighted_par_reset',
                         ax=ax)

plt.show()
