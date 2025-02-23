from dataclasses import dataclass, field
from spikezoo.models.base_model import BaseModel, BaseModelConfig
from typing import List


@dataclass
class SPCSNetConfig(BaseModelConfig):
    # default params for WGSE
    model_name: str = "spcsnet"
    model_file_name: str = "models"
    model_cls_name: str = "SPCS_Net"
    model_win_length: int = 41
    require_params: bool = True
    ckpt_path: str = 'weights/spcsnet.pth'


class SPCSNet(BaseModel):
    def __init__(self, cfg: BaseModelConfig):
        super(SPCSNet, self).__init__(cfg)
