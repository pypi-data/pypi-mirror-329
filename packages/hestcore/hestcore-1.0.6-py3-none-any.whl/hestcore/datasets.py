import h5py
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from .wsi import WSIPatcher, wsi_factory


class WSIPatcherDataset(Dataset):
    """ Dataset from a WSI patcher to directly read tiles on a slide  """
    
    def __init__(self, patcher: WSIPatcher, transform):
        self.patcher = patcher
        
        self.transform = transform
                              
    def __len__(self):
        return len(self.patcher)
    
    def __getitem__(self, index):
        tile, x, y = self.patcher[index]
        
        if self.transform:
            tile = self.transform(tile)

        return {'img': tile, 'coords': (x, y)}
    
def read_assets_from_h5(h5_path, keys=None, skip_attrs=False, skip_assets=False):
    assets = {}
    attrs = {}
    with h5py.File(h5_path, 'r') as f:
        if keys is None:
            keys = list(f.keys())
        for key in keys:
            if not skip_assets:
                assets[key] = f[key][:]
            if not skip_attrs:
                if f[key].attrs is not None:
                    attrs[key] = dict(f[key].attrs)
    return assets, attrs

def wsi_coords_dataset(slide_fpath, patches_h5_fpath, transforms=None, pil=False) -> WSIPatcherDataset:
    """ Create a dataset from an .h5 containing patch coordinates and size """
    wsi = wsi_factory(slide_fpath)
    assets, attrs = read_assets_from_h5(patches_h5_fpath)
    custom_coords = assets['coords']


    if 'patch_size_target' in attrs['coords']:
        # HEST compatibility
        patch_size = attrs['coords']['patch_size_target']
        src_pixel_size = attrs['coords']['pixel_size']
        dst_pixel_size = attrs['coords']['pixel_size'] * attrs['coords']['downsample']
    else:
        # Fishing rod compatibility
        patch_size = attrs['coords']['patch_size']
        src_pixel_size = 1.
        dst_pixel_size = attrs['coords']['downsample'][0]

    wsi_patcher = wsi.create_patcher(
        patch_size=patch_size, 
        src_pixel_size=src_pixel_size, 
        dst_pixel_size=dst_pixel_size, 
        custom_coords=custom_coords,
        pil=pil)
    return WSIPatcherDataset(wsi_patcher, transforms)
    
    
class H5HESTDataset(Dataset):
    """ Dataset to read ST + H&E from .h5 """
    def __init__(self, h5_path, img_transform=None, chunk_size=1000):
        self.h5_path = h5_path
        self.img_transform = img_transform
        self.chunk_size = chunk_size
        with h5py.File(h5_path, 'r') as f:
            self.n_chunks = int(np.ceil(len(f['barcode']) / chunk_size))
        
    def __len__(self):
        return self.n_chunks

    def __getitem__(self, idx):
        start_idx = idx * self.chunk_size
        end_idx = (idx + 1) * self.chunk_size
        with h5py.File(self.h5_path, 'r') as f:
            imgs = f['img'][start_idx:end_idx]
            barcodes = f['barcode'][start_idx:end_idx].flatten().tolist()
            coords = f['coords'][start_idx:end_idx]
            
        if self.img_transform:
            imgs = torch.stack([self.img_transform(Image.fromarray(img)) for img in imgs])
                    
        return {'imgs': imgs, 'barcodes': barcodes, 'coords': coords}