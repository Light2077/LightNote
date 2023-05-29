import time

import streamlit as st
import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.random.randn(2, 3), columns=("col %d" % i for i in range(3)))

my_table = st.table(df1)

df2 = pd.DataFrame(np.random.randn(2, 3), columns=("col %d" % i for i in range(3)))

time.sleep(3)
my_table.add_rows(df2)
# Now the table shown in the Streamlit app contains the data for
# df1 followed by the data for df2.
