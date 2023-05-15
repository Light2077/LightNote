[(6条消息) Python：比较两个dataframe是否相等_assert_frame_equal_qcyfred的博客-CSDN博客](https://blog.csdn.net/qcyfred/article/details/102601971)

```python

import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
 
df1 = pd.DataFrame(np.arange(12).reshape(3, -1))
df2 = pd.DataFrame(np.arange(12).reshape(3, -1))
 
# df1 == df2  # 不要这样做

assert_frame_equal(df1, df2)
```

