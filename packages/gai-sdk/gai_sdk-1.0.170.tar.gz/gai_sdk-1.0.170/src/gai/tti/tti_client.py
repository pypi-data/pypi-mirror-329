from enum import Enum
from PIL import Image
from io import BytesIO
from typing import Union, Optional
from gai.lib.http_utils import http_post
from gai.lib.logging import getLogger
logger = getLogger(__name__)
import json, base64
from gai.lib.config import GaiClientConfig


class TTIOutputType(Enum):
    BYTES="bytes"
    DATA_URL="data_url"
    IMAGE="image"


class TTIClient:

    def __init__(self, config: Optional[Union[GaiClientConfig|dict]]=None,name:Optional[str]="tti", file_path:str=None):
        
        # Load from default config file
        self.config:GaiClientConfig = None
        
        # Convert to ClientLLMConfig
        if isinstance(config, dict):
            # Load default config and patch with provided config
            self.config = GaiClientConfig.from_dict(config)
        elif isinstance(config, GaiClientConfig):
            self.config = config
        elif name:
            # If path is provided, load config from path
            self.config = GaiClientConfig.from_name(name=name,file_path=file_path)
        else:
            raise ValueError("Invalid config or path provided")

    def __call__(self, 
                 prompt:str, 
                 negative_prompt:str=None,
                 width:int=512,
                 height:int=512,
                 steps:int=50,
                 output_type:TTIOutputType = TTIOutputType.BYTES,
                 timeout:float=120.0
                 ):
        if not prompt:
            raise Exception("The parameter 'input' is required.")

        negative_prompt = negative_prompt or "ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, out of frame, ugly, extra limbs, bad anatomy, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck, extra head, cloned head, extra body, cloned body, watermark. extra hands, clone hands, weird hand, weird finger, weird arm, (mutation:1.3), (deformed:1.3), (blurry), (bad anatomy:1.1), (bad proportions:1.2), out of frame, ugly, (long neck:1.2), (worst quality:1.4), (low quality:1.4), (monochrome:1.1), text, signature, watermark, bad anatomy, disfigured, jpeg artifacts, 3d max, grotesque, desaturated, blur, haze, polysyndactyly"
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps
        }
        response = http_post(self.config.url, data,timeout=timeout)
        base64_img = json.loads(response.content.decode("utf-8"))["images"][0]
        image_data = base64.b64decode(base64_img)
        
        if TTIOutputType(output_type) == TTIOutputType.DATA_URL:
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_encoded_data}"
            return data_url
        elif TTIOutputType(output_type) == TTIOutputType.IMAGE:
            return Image.open(BytesIO(image_data))
        elif TTIOutputType(output_type) == TTIOutputType.BYTES:
            return image_data
        else:
            raise Exception("Output type not supported.")



