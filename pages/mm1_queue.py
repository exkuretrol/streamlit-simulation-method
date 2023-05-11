import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="mm1 佇列 Demo",
    page_icon="️📈"
)

st.sidebar.header("mm1 佇列 Demo")

g = np.random.default_rng(seed=None)

# # 產生 n 個指數分佈的隨機數
# g.exponential(
#     scale = 1,    # beta = 1 / lambda
#     size = 10     # n
# )

st.latex(
    r'''
    f(x; \frac{1}{\beta}) = \frac{1}{\beta} \exp(-\frac{x}{\beta})
    '''
)

with st.sidebar:
    maximum_customer = st.number_input(label="最多來客數", min_value=1, value=20)
    inter_time = st.number_input(label = "平均來客時間；$\\beta$", min_value=1, value = 6)
    mean_serve_time = st.number_input(label = "平均服務時間", min_value=1, value = 6)
    business_time = st.number_input(label="營業時間", min_value=1, value = 60)


arrival_times = g.exponential(
    scale = inter_time,
    size = maximum_customer
)

CAI = np.cumsum(arrival_times)

# st.markdown(
#     """
#     - `AI` = customer arrival time
#     - `MI` = customer meal time
#     - `LI` = customer leaving time
#     - `WI` = customer waiting time
#     """
# )

AI = CAI[CAI <= business_time]

CAI = CAI[CAI <= business_time]

customer_number = len(AI)

MI = g.exponential(
    scale = mean_serve_time,
    size = customer_number
)

LI = np.zeros([customer_number])
WI = np.zeros([customer_number])
LI[0] = AI[0] + MI[0]
WI[0] = 0
for i in range(1, customer_number):
    LI[i] = max(AI[i], LI[i - 1]) + MI[i]
    WI[i] = LI[i] - AI[i] - MI[i]

st.dataframe(
    pd.DataFrame(
        {
            "抵達時間（AI）": AI,
            "用餐時間（MI）": MI,
            "等待時間（WI）": WI,
            "離開時間（LI）": LI
        }
    )
)

last_customer_leaving_time = LI[customer_number - 1]
sys_elimate_time = max(last_customer_leaving_time, business_time)
sys_serving_time = np.sum(MI)
sys_idling_time = sys_elimate_time - sys_serving_time
total_customer_waiting_time = np.sum(WI)
mean_waiting_time = np.mean(WI)
mean_meal_time = np.mean(MI)

simulation_result = f"""
- 來客數：{customer_number}
- 系統結束時間：{sys_elimate_time:.2f}
- 系統服務時間：{sys_serving_time:.2f}
- 系統閒置時間：{sys_idling_time:.2f}
- 所有客戶等待時間：{total_customer_waiting_time:.2f}
- 系統閒置率：{sys_idling_time / sys_elimate_time * 100:.2f}%
- 客戶平均等待時間：{mean_waiting_time:.2f}
- 客戶平均用餐時間：{mean_meal_time:.2f}
"""

st.markdown(simulation_result)
