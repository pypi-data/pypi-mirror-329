import numpy as np
import pandas as pd
from collections import Counter

from bdpn.bd_model import REPRODUCTIVE_NUMBER, INFECTIOUS_TIME
from bdpn.bdpn_model import REMOVAL_TIME_AFTER_NOTIFICATION
from bdpn.dl import MODELS, BD, BDCT1, BDCT2, BDCT2000, BDCT, MODEL_FINDER
from bdpn.dl.bdct_estimator import predict_parameters
from bdpn.dl.bdct_model_finder import predict_model
from bdpn.dl.tree_encoder import compute_extra_targets
from bdpn.dl.tree_encoder import forest2sumstat_df
from bdpn.tree_manager import read_forest
from bdpn_model import UPSILON
from dl.bdct_sumstat_checker import check_sumstats

N = 100



def subforest(forest):
    m = len(forest)
    permutation = np.random.choice(np.arange(m), size=m, replace=False)
    new_forest = []
    n = 0
    num = 200 + np.random.random() * (2000 - 200)
    for i in range(m):
        tree = forest[permutation[i]]
        if n + len(tree) < 2000:
            new_forest.append(tree)
            n += len(tree)
        if n >= num:
            break
    # print(f'Kept {len(new_forest)} trees with {n} tips')
    return new_forest, n

N = 10

R0s = []
ds = []
prts = []
ups = []
weights = []
models = []

for i in range(10):

    NWK = f'/home/azhukova/projects/bdpn/hiv_b_uk/data/forest.2012_2015.{i}.nwk'
    forest = read_forest(NWK)
    print(f'Read forest of {len(forest)} trees')
    forest = [_ for _ in forest if len(_) > 1 or _.dist]
    m = len(forest)
    print(f'Kept {m} non-trivial trees')

    sumstat_df = forest2sumstat_df(forest, rho=0.58)
    model_df = predict_model(sumstat_df)

    for model, w in zip(model_df.columns, model_df.loc[0, :]):
        weights.append(w)
        models.append(model)

        # check_sumstats(sumstat_df, model)

        Y_pred = predict_parameters(sumstat_df, model, ci=True)
        compute_extra_targets(Y_pred)
        R0s.append(Y_pred.loc[0, REPRODUCTIVE_NUMBER])
        ds.append(Y_pred.loc[0, INFECTIOUS_TIME])
        prts.append(Y_pred.loc[0, REMOVAL_TIME_AFTER_NOTIFICATION if REMOVAL_TIME_AFTER_NOTIFICATION in Y_pred else INFECTIOUS_TIME])
        ups.append(Y_pred.loc[0, UPSILON] if UPSILON in Y_pred else 0)


    # sumstat_df = forest2sumstat_df(forest, rho=0.58)
    #
    # model_df = predict_model(sumstat_df)
    #
    # best_i = np.argmax(model_df.loc[0, :])
    # model = MODELS[best_i]
    # print(f'The best model is {model} with probability {model_df.iloc[0, best_i]}')

    # check_sumstats(sumstat_df, BDCT)
    # for m in (BDCT, BDCT1, BDCT2, model):
    #     Y_pred = predict_parameters(sumstat_df, m)
    #     compute_extra_targets(Y_pred)
    #     print(m, ':')
    #     print(Y_pred.loc[0, :])
    #     print()

    #
    # for i in range(10):
    #     new_forest, n_tips = subforest()
    #     sub_sumstat_df = forest2sumstat_df(new_forest, rho=0.58)
    #     Y_pred = predict_parameters(sub_sumstat_df, BDCT)
    #     compute_extra_targets(Y_pred)
    #     print(Y_pred.loc[0, :])

    # for model in (BDCT, BD, BDCT1, BDCT2, BDCT2000):
    #     print(f'\n===========Predictions with model {model}:')
    #     # check_sumstats(sumstat_df, model)
    #
    #     Y_pred = predict_parameters(sumstat_df, model)
    #     compute_extra_targets(Y_pred)
    #     print(Y_pred.loc[0, :])
    #     Y_pred.to_csv(NWK.replace('.nwk', f'.est_{model}'), header=True)


    # for i in range(N):
    #     while True:
    #         try:
    #             new_forest, n_tips = subforest(forest)
    #             weights[i] = 2 * n_tips - len(new_forest)
    #             sumstat_df = forest2sumstat_df(new_forest, rho=0.58)
    #
    #             model_df = predict_model(sumstat_df)
    #
    #             best_i = np.argmax(model_df.loc[0, :])
    #             model = MODELS[best_i]
    #             models.append(model)
    #             # print(f'The best model if {model} with probability {model_df.iloc[0, best_i]}')
    #
    #             # check_sumstats(sumstat_df, model)
    #
    #             Y_pred = predict_parameters(sumstat_df, model)
    #             compute_extra_targets(Y_pred)
    #             R0s[i] = Y_pred.loc[0, REPRODUCTIVE_NUMBER]
    #             ds[i] = Y_pred.loc[0, INFECTIOUS_TIME]
    #             prts[i] = Y_pred.loc[0, REMOVAL_TIME_AFTER_NOTIFICATION] if REMOVAL_TIME_AFTER_NOTIFICATION in Y_pred else Y_pred.loc[0, INFECTIOUS_TIME]
    #             ups[i] = Y_pred.loc[0, UPSILON] if UPSILON in Y_pred else 0
    #             break
    #         except:
    #             pass
        # print(Y_pred.loc[0, :])
        # Y_pred.to_csv(NWK.replace('.nwk', f'.est_{model}'), header=True)


weights = np.array(weights)
weights /= weights.sum()

model_counter = Counter()
for model, w in zip(models, weights):
    model_counter[model] += w

print(model_counter)

prts = np.array(prts) * 365

print(len(weights), len(prts), len(ups))

print(f'R0:\t{np.quantile(R0s, 0.5, weights=weights, method='inverted_cdf'):.2f}\t[{np.quantile(R0s, 0.025, weights=weights, method='inverted_cdf'):.2f}, {np.quantile(R0s, 0.975, weights=weights, method='inverted_cdf'):.2f}]')
print(f'd:\t{np.quantile(ds, 0.5, weights=weights, method='inverted_cdf'):.2f}\t[{np.quantile(ds, 0.025, weights=weights, method='inverted_cdf'):.2f}, {np.quantile(ds, 0.975, weights=weights, method='inverted_cdf'):.2f}]')
print(f'prt:\t{np.quantile(prts, 0.5, weights=weights, method='inverted_cdf'):.2f}\t[{np.quantile(prts, 0.025, weights=weights, method='inverted_cdf'):.2f}, {np.quantile(prts, 0.975, weights=weights, method='inverted_cdf'):.2f}]')
print(f'ups:\t{np.quantile(ups, 0.5, weights=weights, method='inverted_cdf'):.2f}\t[{np.quantile(ups, 0.025, weights=weights, method='inverted_cdf'):.2f}, {np.quantile(ups, 0.975, weights=weights, method='inverted_cdf'):.2f}]')