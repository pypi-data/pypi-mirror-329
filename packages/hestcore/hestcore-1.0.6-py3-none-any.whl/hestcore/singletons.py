import copy
import os
from huggingface_hub import snapshot_download
import threading


class TissueSegmenter:
    def __init__(self):
        self._model = None
        self.lock = threading.Lock()
        self._weights_dir = None
        self._model_name = None
        
    def _load_model(self, weights_dir, model_name, auto_download):
        import torch
        from torch import nn
        
        model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50')
        model.classifier[4] = nn.Conv2d(
            in_channels=256,
            out_channels=2,
            kernel_size=1,
            stride=1
        )
        
        weights_path = os.path.join(weights_dir, model_name)
    
        if auto_download:
            snapshot_download(repo_id="MahmoodLab/hest-tissue-seg", repo_type='model', local_dir=weights_dir, allow_patterns=model_name, cache_dir=weights_dir)
        
        if torch.cuda.is_available():
            checkpoint = torch.load(weights_path)
        else:
            checkpoint = torch.load(weights_path, map_location=torch.device('cpu'))
            
        new_state_dict = {}
        for key in checkpoint['state_dict']:
            if 'aux' in key:
                continue
            new_key = key.replace('model.', '')
            new_state_dict[new_key] = checkpoint['state_dict'][key]
        model.load_state_dict(new_state_dict)
        self._model = model
    
    def get_model(self, weights_dir, model_name, auto_download):
        """ Will reload the model only if differents weights_dir or model_name are specified """
        with self.lock:
            if self._model is None or weights_dir != self._weights_dir or model_name != self._model_name:
                self._weights_dir = weights_dir
                self._model_name = model_name
                self._load_model(weights_dir, model_name, auto_download)
            return copy.deepcopy(self._model)
            
segmenter_singleton = TissueSegmenter()