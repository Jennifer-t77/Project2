""" zid_project2_main.py
"""
# ----------------------------------------------------------------------------
# Part 1: Read the documentation for the following methods:
#   – pandas.DataFrame.mean
#   - pandas.Series.concat
#   – pandas.Series.count
#   – pandas.Series.dropna
#   - pandas.Series.index.to_period
#   – pandas.Series.prod
#   – pandas.Series.resample
#   - ......
# Hint: you can utilize modules covered in our lectures, listed above and any others.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Part 2: import modules inside the project2 package
# ----------------------------------------------------------------------------
# Create import statements so that the module config.py and util.py (inside the project2 package)
# are imported as "cfg", and "util"
#
from project2 import util
from project2 import config as cfg


# We've imported other needed scripts and defined aliases. Please keep using the same aliases for them in this project.
from project2 import zid_project2_etl as etl
from project2 import zid_project2_characteristics as cha
from project2 import zid_project2_portfolio as pf

import pandas as pd


# -----------------------------------------------------------------------------------------------
# Part 3: Follow the workflow in portfolio_main function
#         to understand how this project construct total volatility long-short portfolio
# -----------------------------------------------------------------------------------------------
def portfolio_main(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Constructs equal-weighted portfolios based on the specified characteristic and quantile threshold.
    We focus on total volatility investment strategy in this project 2.
    We name the characteristic as 'vol'

    This function performs several steps to construct portfolios:
    1. Call `aj_ret_dict` function from etl script to generate a dictionary containing daily and
       monthly returns.
    2. Call `cha_main` function from cha script to generate a DataFrame containing stocks' monthly return
       and characteristic, i.e., total volatility, info.
    3. Call `pf_main` function from pf script to construct a DataFrame with
       equal-weighted quantile and long-short portfolio return series.

    Parameters
    ----------
    tickers : list
        A list including all tickers (can include lowercase and/or uppercase characters) in the investment universe

    start  :  str
        The inclusive start date for the date range of the price table imported from data folder
        For example: if you enter '2010-09-02', function in etl script will include price
        data of stocks from this date onwards.
        And make sure the provided start date is a valid calendar date.

    end  :  str
        The inclusive end date for the date range, which determines the final date
        included in the price table imported from data folder
        For example: if you enter '2010-12-20', function in etl script will encompass data
        up to and including December 20, 2010.
        And make sure the provided start date is a valid calendar date.

    cha_name : str
        The name of the characteristic. Here, it should be 'vol'

    ret_freq_use  :  list
        It identifies that which frequency returns you will use to construct the `cha_name`
        in zid_project2_characteristics.py.
        Set it as ['Daily',] when calculating stock total volatility here.

    q : int
        The number of quantiles to divide the stocks into based on their characteristic values.


    Returns
    -------
    dict_ret : dict
        A dictionary with two items, each containing a dataframe of daily and monthly returns
        for all stocks listed in the 'tickers' list.
        This dictionary is the output of `aj_ret_dict` in etl script.
        See the docstring there for a description of it.

    df_cha : df
        A DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month
        that include the stocks' monthly returns for that period and the characteristics,
        i.e., total volatility, from the previous year-month.
        This df is the output of `cha_main` function in cha script.
        See the docstring there for a description of it.

    df_portfolios : df
        A DataFrame containing the constructed equal-weighted quantile and long-short portfolios.
        This df is the output of `pf_cal` function in pf script.
        See the docstring there for a description of it.

    """

    # --------------------------------------------------------------------------------------------------------
    # Part 4: Complete etl scaffold to generate returns dictionary and to make ad_ret_dic function works
    # --------------------------------------------------------------------------------------------------------
    dict_ret = etl.aj_ret_dict(tickers, start, end)

    # ---------------------------------------------------------------------------------------------------------
    # Part 5: Complete cha scaffold to generate dataframe containing monthly total volatility for each stock
    #         and to make char_main function work
    # ---------------------------------------------------------------------------------------------------------
    df_cha = cha.cha_main(dict_ret, cha_name,  ret_freq_use)

    # -----------------------------------------------------------------------------------------------------------
    # Part 6: Read and understand functions in pf scaffold. You will need to utilize functions there to
    #         complete some of the questions in Part 7
    # -----------------------------------------------------------------------------------------------------------
    df_portfolios = pf.pf_main(df_cha, cha_name, q)

    util.color_print('Portfolio Construction All Done!')

    return dict_ret, df_cha, df_portfolios


# ----------------------------------------------------------------------------
# Part 7: Complete the auxiliary functions
# ----------------------------------------------------------------------------
def get_avg(df: pd.DataFrame, year):
    """ Returns the average value of all columns in the given df for a specified year.

    This function will calculate the column average for all columns
    from a data frame `df`, for a given year `year`.
    The data frame `df` must have a DatetimeIndex or PeriodIndex index.

    Missing values will not be included in the calculation.

    Parameters
    ----------
    df : data frame
        A Pandas data frame with a DatetimeIndex or PeriodIndex index.

    year : int
        The year as a 4-digit integer.

    Returns
    -------
    ser
        A series with the average value of columns for the year `year`.

    Example
    -------
    For a data frame `df` containing the following information:

        |            | tic1 | tic2  |
        |------------+------+-------|
        | 1999-10-13 | -1   | NaN   |
        | 1999-10-14 | 1    | 0.032 |
        | 2020-10-15 | 0    | -0.02 |
        | 2020-10-16 | 1    | -0.02 |

        >> res = get_avg(df, 1999)
        >> print(res)
        tic1      0.000
        tic2      0.032
        dtype: float64

    """
    # <COMPLETE THIS PART>

    # Ensure the index is a PeriodIndex or DatetimeIndex
    if not isinstance(df.index, (pd.PeriodIndex, pd.DatetimeIndex)):
        raise ValueError("The DataFrame index must be a PeriodIndex or DatetimeIndex")

    # Convert to PeriodIndex if it is not already
    if not isinstance(df.index, pd.PeriodIndex):
        df = df.to_period('M')

    # Filter the DataFrame for the specified year
    df_year = df[df.index.year == year]

    # Calculate the mean for each column, ignoring NaNs
    return df_year.mean()

def get_cumulative_ret(df):
    """ Returns cumulative returns for input DataFrame.

    Given a df with return series, this function will return the
    buy-and-hold return over the entire period.

    Parameters
    ----------
    df : DataFrame
        A Pandas DataFrame containing monthly portfolio returns
        with a PeriodIndex index.
        - df.columns: portfolio names

    Returns
    -------
    ser : Series
        A series containing portfolios' buy-and-hold return over the entire period.
        - ser.index: portfolio names

    Notes
    -----
    The buy and hold cumulative return will be computed as follows:

        (1 + r1) * (1 + r2) *....* (1 + rN) - 1
        where r1, ..., rN represents monthly returns

    """
    # <COMPLETE THIS PART>

    # Ensure the index is a PeriodIndex
    if not isinstance(df.index, pd.PeriodIndex):
        raise ValueError("The DataFrame index must be a PeriodIndex")

    # Calculate the cumulative return for each column
    cumulative_ret = (1 + df).prod() - 1

    return cumulative_ret
# ----------------------------------------------------------------------------
# Part 8: Answer questions
# ----------------------------------------------------------------------------
# NOTES:
#
# - THE SCRIPTS YOU NEED TO SUBMIT ARE
#   zid_project2_main.py, zid_project2_etl.py, and zid_project2_characteristics.py
#
# - Do not create any other functions inside the scripts you need to submit unless
#   we ask you to do so.
#
# - For this part of the project, only the answers provided below will be
#   marked. You are free to create any function you want (IN A SEPARATE
#   MODULE outside the scripts you need to submit).
#
# - All your answers should be strings. If they represent a number, include 4
#   decimal places unless otherwise specified in the question description
#
# - Here is an example of how to answer the questions below. Consider the
#   following question:
#
#   Q0: Which ticker included in config.TICMAP starts with the letter "C"?
#   Q0_answer = '?'
#
#   You should replace the '?' with the correct answer:
#   Q0_answer = 'CSCO'
#
#
#     To answer the questions below, you need to run portfolio_main function in this script
#     with the following parameter values:
#     tickers: all tickers included in the dictionary config.TICMAP,
#     start: '2000-12-29',
#     end: '2021-08-31',
#     cha_name: 'vol'.
#     ret_freq_use: ['Daily',],
#     q: 3
#     Please name the three output files as DM_Ret_dict, Vol_Ret_mrg_df, EW_LS_pf_df.
#     You can utilize the three output files and auxiliary functions to answer the questions.

tickers = list(cfg.TICMAP.keys())
start = '2000-12-29'
end = '2021-08-31'
cha_name = 'vol'
ret_freq_use = ['Daily']
q = 3

dict_ret, df_cha, df_portfolios = portfolio_main(tickers, start, end, cha_name, ret_freq_use, q)

dict_ret['Daily'].to_csv('DM_Ret_dict.csv')
df_cha.to_csv('Vol_Ret_mrg_df.csv')
df_portfolios.to_csv('EW_LS_pf_df.csv')

DM_Ret_dict = pd.read_csv('DM_Ret_dict.csv', index_col=0, parse_dates=True)
Vol_Ret_mrg_df = pd.read_csv('Vol_Ret_mrg_df.csv', index_col=0, parse_dates=True)
EW_LS_pf_df = pd.read_csv('EW_LS_pf_df.csv', index_col=0, parse_dates=True, date_format='%Y-%m-%d')


# Q1: Which stock in your sample has the lowest average daily return for the
#     year 2008 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
Q1_ANSWER = 'INTC'

# Q2: What is the daily average return of the stock in question 1 for the year 2008.
Q2_ANSWER = '-0.03'

# Q3: Which stock in your sample has the highest average monthly return for the
#     year 2019 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
Q3_ANSWER = 'INTC'

# Q4: What is the average monthly return of the stock in question 3 for the year 2019.
Q4_ANSWER = '0.08'

# Q5: What is the average monthly total volatility for stock 'TSLA' in the year 2010?
Q5_ANSWER = '0.0313'

# Q6: What is the ratio of the average monthly total volatility for stock 'V'
#     in the year 2008 to that in the year 2018? Keep 1 decimal places.
Q6_ANSWER = '0.5'

# Q7: How many effective year-month for stock 'TSLA' in year 2010. An effective year-month
#     row means both monthly return in 'tsla' column and total volatility in 'tsla_vol'
#     are not null.
Q7_ANSWER = '252'

# Q8: How many rows and columns in the EW_LS_pf_df data frame?
Q8_ANSWER = '252,2'

# Q9: What is the average equal weighted portfolio return of the quantile with the
#     lowest total volatility for the year 2019?
Q9_ANSWER = '-0.4601'

# Q10: What is the cumulative portfolio return of the total volatility long-short portfolio
#      over the whole sample period?
Q10_ANSWER = '-1.0'
# ----------------------------------------------------------------------------
# Part 9: Add t_stat function
# ----------------------------------------------------------------------------
# We've outputted EW_LS_pf_df file and save the total volatility long-short portfolio
# in 'ls' column from Part 8.

# Please add an auxiliary function called ‘t_stat’ below.
# You can design the function.
# But make sure that when function get called, t_stat(EW_LS_pf_df),
# the output is a DataFrame with one row called 'ls' and three columns below:
#  1.ls_bar, the mean of 'ls' columns in EW_LS_pf_df, keep 4 decimal points
#  2.ls_t, the t stat of 'ls' columns in EW_LS_pf_df, keep 4 decimal points
#  3.n_obs, the number of observations of 'ls' columns in EW_LS_pf_df, save as integer

# Notes:
# Please add the function in zid_project2_main.py.
# The name of the function should be t_stat and including docstring.
# Please replace the '?' of ls_bar, ls_t and n_obs variables below
# with the respective values of the 'ls' column in EW_LS_pf_df from Part 8,
# keep 4 decimal places if it is not an integer:
ls_bar = '0.0076'
ls_t = '1.4469'
n_obs = '235'


# <ADD THE t_stat FUNCTION HERE>
import pandas as pd

def t_stat(df):
    """
    Calculate the mean (ls_bar), t-statistic (ls_t), and number of observations (n_obs)
    of the 'ls' column in the given DataFrame.

    Parameters
    ----------
    df : DataFrame
        A DataFrame containing the 'ls' column.

    Returns
    -------
    result : DataFrame
        A DataFrame with one row and three columns: 'ls_bar', 'ls_t', 'n_obs'.
    """
    ls = df['ls']
    ls_bar = ls.mean()
    ls_se = ls.std(ddof=1) / (len(ls) ** 0.5)  # Using sample standard deviation to calculate standard error
    ls_t = ls_bar / ls_se
    n_obs = ls.count()
    result = pd.DataFrame({'ls_bar': [ls_bar], 'ls_t': [ls_t], 'n_obs': [n_obs]}, index=['ls'])
    return result

if __name__ == "__main__":
    file_path = 'EW_LS_pf_df.csv'
    EW_LS_pf_df = pd.read_csv(file_path, index_col=0, parse_dates=True, date_format='%Y-%m')


    t_stat_result = t_stat(EW_LS_pf_df)

    print(t_stat_result)

    ls_bar = round(t_stat_result['ls_bar'].values[0], 4)
    ls_t = round(t_stat_result['ls_t'].values[0], 4)
    n_obs = int(t_stat_result['n_obs'].values[0])

    print(f"ls_bar: {ls_bar}, ls_t: {ls_t}, n_obs: {n_obs}")

# ----------------------------------------------------------------------------
# Part 10: share your team's project 2 git log
# ----------------------------------------------------------------------------
# In week6 slides, we introduce Git and show how to work collaboratively on Git.
# You are not necessary to use your UNSW email to register the git account.
# But when you set up your username, you will follow the format zid...FirstNameLastName.
#
# Please follow the instruction there to work with your teammates. The team leader
# will need to create a Project 2 Repo on GitHub and grant teammates access to the Repo.
# For teammates, you will need to clone the repo and then coding as a team.
#
# The team will need to generate a git log from git terminal.
# You can use 'cd <...>' direct your terminal into the project 2 repo directory,
# then export the git log:
# git log --pretty=format:"%h%x09%an%x09%ad%x09%s" >teamX.txt
# Here is an example output:
# .......
# dae0fa9	zid1234 Sarah Xiao	Mon Feb 12 16:33:22 2024 +1100	commit and push test
# fa26a62	zid1234 Sarah Xiao	Mon Feb 12 16:32:02 2024 +1100	commit and push test
# 800bf27	zid5678 David Lee	Mon Feb 12 16:12:30 2024 +1100	for testing
# .......
#
# Please replace the """?""" with your team's project 2 git log:
git_log = """
92d2b5e	Jiani Tang	Thu Aug 1 11:15:24 2024 +1000	typo & pre_link update
9208460	Jiani Tang	Thu Aug 1 11:11:55 2024 +1000	extra changes about .idea
7d3dc8f	z5536092	Thu Aug 1 00:42:48 2024 +1000	Update zid_project2_main.py
f1e6dd3	z5536092	Wed Jul 31 16:27:51 2024 +1000	Update zid_project2_main.py
aa7be41	Jiani Tang	Wed Jul 31 13:00:31 2024 +1000	extra changes about .idea
e58dace	Jiani Tang	Wed Jul 31 12:58:28 2024 +1000	git log update
3c5ff94	Jiani Tang	Wed Jul 31 12:57:39 2024 +1000	etl_debug_finished
1a67b10	Ahdiani Febriyanti	Wed Jul 31 03:54:08 2024 +1000	Merge remote-tracking branch 'origin/master'
148d2eb	Ahdiani Febriyanti	Wed Jul 31 03:53:56 2024 +1000	change the function
f04eb01	z5536092	Tue Jul 30 23:14:44 2024 +1000	Update zid_project2_main.py
85412d5	Ahdiani Febriyanti	Tue Jul 30 22:16:07 2024 +1000	Merge remote-tracking branch 'origin/master'
8a36d6e	Ahdiani Febriyanti	Tue Jul 30 22:14:14 2024 +1000	refresh the portfolio
c382ce9	Jiani Tang	Tue Jul 30 21:53:23 2024 +1000	etl_debug_finished
003c8a0	Jiani Tang	Tue Jul 30 21:41:21 2024 +1000	etl_debug_finished
7358595	Jiani Tang	Tue Jul 30 21:21:06 2024 +1000	etl_debug_finished
327d6bc	z5536092	Tue Jul 30 02:07:07 2024 +1000	Update zid_project2_main.py
17fe8d5	z5536092	Sat Jul 27 21:01:46 2024 +1000	Update zid_project2_main.py
1cb1868	z5507587AhdianiFebriyanti	Sat Jul 27 18:59:19 2024 +1000	Delete toolkit_config.py
ff8b982	Ahdiani Febriyanti	Sat Jul 27 18:04:32 2024 +1000	toolkit_config.py
bf9c3de	z5507587AhdianiFebriyanti	Sat Jul 27 17:51:41 2024 +1000	Delete toolkit_config
3243c0e	z5507587AhdianiFebriyanti	Sat Jul 27 17:37:12 2024 +1000	Create toolkit_config
a076967	Ahdiani Febriyanti	Sat Jul 27 16:35:10 2024 +1000	7.1-7.2
316dce6	Ahdiani Febriyanti	Sat Jul 27 16:31:13 2024 +1000	7.1
4f1bbdb	Ahdiani Febriyanti	Sat Jul 27 16:21:56 2024 +1000	import fr etl and cha
0d8d248	Ahdiani Febriyanti	Sat Jul 27 16:21:18 2024 +1000	import fr etl and cha
ba1ceb9	Ahdiani Febriyanti	Sat Jul 27 16:16:25 2024 +1000	5.1-5.5
6aca47c	Ahdiani Febriyanti	Sat Jul 27 16:06:41 2024 +1000	merge_table function
a57d4b9	Ahdiani Febriyanti	Sat Jul 27 16:02:05 2024 +1000	vol_cal function
1ec98cb	Ahdiani Febriyanti	Sat Jul 27 15:42:53 2024 +1000	import modules
66b96ee	Ahdiani Febriyanti	Sat Jul 27 14:16:15 2024 +1000	complete vol_cal function
191655a	Ahdiani Febriyanti	Sat Jul 27 13:32:18 2024 +1000	Merge remote-tracking branch 'origin/master'
5d87f2d	z5507587AhdianiFebriyanti	Sat Jul 27 12:56:44 2024 +1000	import modules
16f20f8	z5507587AhdianiFebriyanti	Sat Jul 27 12:56:44 2024 +1000	Delete toolkit_config.py
694420a	Ahdiani Febriyanti	Sat Jul 27 10:01:45 2024 +1000	Initial commit
669b9e7	Jiani Tang	Thu Jul 25 19:58:23 2024 +1000	Q2-Q4 Finished
e1a9e11	Jiani Tang	Thu Jul 25 19:56:52 2024 +1000	Q2-Q4 Finished
2f8b0a8	Jiani Tang	Thu Jul 25 19:19:49 2024 +1000	4.4 update
8020b59	Jiani Tang	Thu Jul 25 14:48:24 2024 +1000	4.2 update
69e3b8c	Jiani Tang	Wed Jul 24 15:06:59 2024 +1000	test finished
3e88cd0	Jiani Tang	Wed Jul 24 14:01:12 2024 +1000	test finished
b7597c3	Jiani Tang	Wed Jul 24 13:33:25 2024 +1000	file change test
de320ca	Jiani Tang	Wed Jul 24 13:33:01 2024 +1000	file change test "import pandas as pd"
929a750	Jiani Tang	Wed Jul 24 13:08:41 2024 +1000	file change test "import pandas as pd"
5ce66f1	Jiani Tang	Wed Jul 24 12:53:23 2024 +1000	update the file position
a3dc0f0	Jiani Tang	Wed Jul 24 12:42:10 2024 +1000	Initial commit
"""


# ----------------------------------------------------------------------------
# Part 11: project 2 mini-presentation
# ----------------------------------------------------------------------------
# In this part, you are going to record and present a strictly less than 15 minutes long presentation.
# You should seek to briefly describe:
# 1.	What are the null and alternative hypotheses that the project 2 is testing
# 2.	What’s the methodology of the portfolio construction
#       and how is it implemented in Project 2 codebase?
# 3.	What inferences can we draw from the output of Part 9,
#       including the average return and t-stats of the long-short portfolio?
# 4.	Do you think the results are reliable? Why or why not?
# 5.	Is there any further work you would like to pursue based on Project 2?
#       Share your to-do list.
#
# For this mini-presentation, the group can decide whether all members should appear in the presentation video.
# You can use websites like YouTube or Zoom to record and share your videos with us,
# or share your videos via OneDrive.
# Please **AVOID** using VooV, QQ, and WeChat to share videos,
# as we have faced access issues with these platforms previously.

# Please replace the """?""" with your team's presentation video link.
# If you have set a password, please replace the """?""" with the actual password to ensure accessibility,
# or leave the Presentation_Password variable as it is.
Presentation_link = """https://youtu.be/QKsNmj58zKc"""
# Presentation_Password = """?"""


def _test_get_avg():
    """ Test function for `get_avg`
    """
    # Made-up data
    ret = pd.Series({
        '2019-01-01': 1.0,
        '2019-01-02': 2.0,
        '2020-10-02': 4.0,
        '2020-11-12': 4.0,
    })
    df = pd.DataFrame({'some_tic': ret})
    df.index = pd.to_datetime(df.index)

    msg = 'This is the test data frame `df`:'
    util.test_print(df, msg)

    res = get_avg(df,  2019)
    to_print = [
        "This means `res =get_avg(df, year=2019) --> 1.5",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


def _test_get_cumulative_ret():
    """ `Test function for `get_cumulative_ret`

    """
    # Made-up data
    idx_m = pd.to_datetime(['2019-02-28',
                            '2019-03-31',
                            '2019-04-30',]).to_period('M')
    stock1_m = [0.063590, 0.034290, 0.004290]
    stock2_m = [None, 0.024390, 0.022400]
    monthly_ret_df = pd.DataFrame({'stock1': stock1_m, 'stock2': stock2_m, }, index=idx_m)
    monthly_ret_df.index.name = 'Year_Month'
    msg = 'This is the test data frame `monthly_ret_df`:'
    util.test_print(monthly_ret_df, msg)

    res = get_cumulative_ret(monthly_ret_df)
    to_print = [
        "This means `res =get_cumulative_ret(monthly_ret_df)",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


if __name__ == "__main__":
    pass

_test_get_avg()
_test_get_cumulative_ret()



