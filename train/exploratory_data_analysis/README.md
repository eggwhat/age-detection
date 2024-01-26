### Exploratory data analysis

=========================================

The notebook is designed to analyze and derive insights from 'metadata.csv' file and ultimately on analyzing the basic statistics of several .jpg images.

Data Structure
--------------

The data for model training should be placed in the `/train/data` directory, also referred to as `DATA_DIR` in `consts.py`. The structure of the data directory is as follows:

```

    ├── data
    │   ├── imdb_crop
    │   │   ├── **
    │   │   │  ├── **.jpg
    │   │   ├── imdb.mat
    │   ├── wiki_crop
    │   │   ├── **
    │   │   │  ├── **.jpg
    │   │   ├── wiki.mat
```

Source:

1. imdb_crop: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar

2. wiki_crop: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/wiki_crop.tar

To use this notebook:

1. Ensure that the data is structured as mentioned in the "Data Structure" section.
2. Run each cell in the notebook sequentially to perform exploratory data analysis.

Most important first steps - preparation for EDA
------------------------------------------------

1. Imports
----------

```
    import os
    import csv
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import seaborn as sns
    import statsmodels.api as sm
    from scipy import stats
    from PIL import Image
    from tabulate import tabulate
```

This cell imports various libraries necessary for data analysis and visualization. Key libraries include:

- ``pandas`` and ``numpy`` for data manipulation,
- ``matplotlib`` and ``seaborn`` for data visualization,
- ``statsmodels`` and ``scipy`` for statistical analysis,
- ``PIL`` for image processing,
- ``tabulate`` for presenting tabular data.

2. Setting up Data Path
------------------------

```

    path_to_metadatacsv = os.path.realpath('../data/metadata.csv')
    print(path_to_metadatacsv)
```

This cell calculates the real path of the 'metadata.csv' file, which is presumably the main dataset for analysis. The resolved path is printed for verification.

3. Reading CSV File
-------------------

```

    rows = [] 
    with open(path_to_metadatacsv, 'r') as file:
        read_metadatacsv = csv.reader(file)
        column_names = next(read_metadatacsv)
        for row in read_metadatacsv:
            rows.append(row)
    print("Column names:", column_names)
    print("\nThe first few sample rows:\n")
    for row in rows[:10]:
        print(row)
```

In this cell, the notebook:

- Opens and reads the CSV file specified in the previous cell.
- Extracts and prints the column names of the dataset.
- Reads the first few rows of the dataset for a preliminary overview.

4. Loading CSV File into DataFrame
-----------------------------------


```
    df_metadata = pd.read_csv(path_to_metadatacsv)
    df_metadata.head()
```

This cell loads the CSV file (referenced by `path_to_metadatacsv`) into a Pandas DataFrame named `df_metadata`. It then displays the first few rows of the DataFrame using the `head()` method. This is a common practice in data analysis to get a quick glimpse of the dataset structure and contents.

**General overview of Code Cells**
----------------------------------

The notebook includes various code cells for tasks such as data loading, cleaning, analysis, and visualization. Key code cells include:

1. **Imports** - explained above
2. **Data Path Setup** - explained above
3. **Data Loading** - explained above
4. **Preliminary Analysis**
5. **Exploratory Data Analysis**
6. **Image Analysis**

Preliminary Analysis
--------------------

The notebook provides analysis for subsequent data cleansing approaches, including:

- Collection size analysis.
- Checking whether NaN values are present.
- Analysis of outliers, including values impossible in biology.

Exploratory Data Analysis
-------------------------

This section covers:

- Techniques for uncovering patterns, trends, and relationships in the data.
- Statistical summaries and visualizations for understanding the data

Image Analysis
--------------

This section delves into:

- Loading and analyzing image data.
- Extracting basic statistics like format, size, and dimensions from images.
- Visualizing image data.

Conclusion
----------

**The most important thing** after analyzing this data set is that it contains **values that are impossible** for the ages of men and women. In the world of biology this is impossible. We set the upper possible age limit for a human to be 122 years, the lower one to 1, according to the oldest living person.

Article: https://en.wikipedia.or/wiki/List_of_the_verified_oldest_people