# Core library for histopathology


`hestcore` is a core library used in the implementation of `HEST` and `MADELEINE`.

It provides the following features:

- Easy access of WSIs with multiple backends (Cucim, OpenSlide and Numpy)
- Precise background/tissue binary segmentation (powered by DeepLab V3)
- Seamless WSI access with iterators/PyTorch datasets
