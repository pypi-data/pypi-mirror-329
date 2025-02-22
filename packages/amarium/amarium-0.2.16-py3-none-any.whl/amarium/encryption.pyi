from .utils import prepare_file_name_saving as prepare_file_name_saving
from typing import Tuple

def generate_asymmetric_keys(
    key_size: int, private_key_name: str, public_key_name: str
) -> Tuple[bytes, bytes]: ...
