### Expected folder structure

Since the data can be quite huge, it won't be stored in this repository. This is a documentation
on how to add data for model training and what is the expected structure/format.

`/train/data` is a default folder where data for model training should be put. However, feel free to
use an external one instead and change `DATA_DIR` in `consts.py`.

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

@article{Rothe-IJCV-2018,
  author = {Rasmus Rothe and Radu Timofte and Luc Van Gool},
  title = {Deep expectation of real and apparent age from a single image without facial landmarks},
  journal = {International Journal of Computer Vision},
  volume={126},
  number={2-4},
  pages={144--157},
  year={2018},
  publisher={Springer}
}