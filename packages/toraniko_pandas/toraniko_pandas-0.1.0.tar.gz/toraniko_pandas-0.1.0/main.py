# %% [markdown]
# # Factor Analysis Notebook
# This notebook demonstrates factor analysis using SimFin financial data and custom factor models.

# %%
# %% Import Dependencies
import warnings

import matplotlib.pyplot as plt
import statsmodels.api as sm

from simfin_downloader import SimFin
from toraniko_pandas.model import estimate_factor_returns
from toraniko_pandas.styles import factor_mom, factor_sze, factor_val
from toraniko_pandas.utils import top_n_by_group

# Configure warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="invalid value encountered in log")
warnings.filterwarnings("ignore", message="divide by zero encountered in log")

# %% [markdown]
# ## Data Preparation
# Load and process financial data from SimFin API

# %%
# %% Load SimFin Data
simfin = SimFin()
df, sectors, industries = simfin.get_toraniko_data()

# Filter top 3000 companies by market cap
df = top_n_by_group(df.dropna(), 3000, "market_cap", ("date",), True)
df
# %% [markdown]
# ### Sector and Industry Data
# Sample views of processed sector/industry classifications

# %%
# Display sector data
sectors

# %%
# Display industry data
industries

# %% [markdown]
# ## Feature Engineering
# Calculate financial factors and prepare analysis datasets

# %%
# %% Calculate Market Factors
# Size factor calculation
size_df = factor_sze(df, lower_decile=0.2, upper_decile=0.8)

# Momentum factor calculation
mom_df = factor_mom(df, trailing_days=252, winsor_factor=0.01)

# Value factor calculation
value_df = factor_val(df, winsor_factor=0.05)

# %% [markdown]
# ### Factor Distributions
# Visual inspection of factor score distributions

# %%
# Momentum distribution
mom_df["mom_score"].hist(bins=100)
plt.title("Momentum Factor Distribution")
plt.show()

# Value distribution
value_df["val_score"].hist(bins=100)
plt.title("Value Factor Distribution")
plt.show()

# %% [markdown]
# ## Data Merging
# Combine processed datasets for analysis

# %%
# %% Merge Data Sources
style_scores = (
    value_df.merge(mom_df, on=["symbol", "date"])
    .merge(size_df, on=["symbol", "date"])
    .dropna()
)

ddf = (
    df[["symbol", "asset_returns", "market_cap"]]
    .merge(sectors, on="symbol")
    .merge(style_scores, on=["symbol", "date"])
    .dropna()
    .astype({"symbol": "category"})
)

# %% [markdown]
# ## Factor Return Estimation
# Calculate factor returns using Fama-MacBeth regression

# %%
# %% Calculate Factor Returns
returns_df = ddf[["symbol", "asset_returns"]]
mkt_cap_df = ddf[["symbol", "market_cap"]]
sector_df = ddf[sectors.columns.tolist() + ["symbol"]]
style_df = ddf[style_scores.columns]

fac_df, eps_df = estimate_factor_returns(
    returns_df,
    mkt_cap_df,
    sector_df,
    style_df,
    winsor_factor=0.1,
    residualize_styles=False,
)

# %% [markdown]
# ## Apple Factor Exposure Analysis
# Linear regression model for AAPL returns

# %%
# %% AAPL Factor Model
y = returns_df.query("symbol == 'AAPL'")["asset_returns"]
X = fac_df[["market", "sector_technology", "mom_score", "val_score", "sze_score"]]
X = sm.add_constant(X)

model = sm.OLS(y, X)
results = model.fit().get_robustcov_results()
results.summary()
