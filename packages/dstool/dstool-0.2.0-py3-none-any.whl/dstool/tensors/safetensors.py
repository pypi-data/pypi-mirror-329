import json

import cupy as cp
import safetensors as st
from rich.table import Table
from safetensors.torch import save_file
from vllm.delta.compressor import LosslessCompressor


def get_tensor_stats(filepath):
    tensor_stats = {}
    with st.safe_open(filepath, "torch") as f:
        for key in f.keys():
            tensor_stats[key] = {
                "shape": f.get_tensor(key).shape,
                "dtype": f.get_tensor(key).dtype,
                "nbytes": f.get_tensor(key).nbytes,
                "range": f"{f.get_tensor(key).min():.2f} - {f.get_tensor(key).max():.2f}",
            }
    return tensor_stats


def tensorstats_to_table(filepath, tensor_stats):
    table = Table(title=f"Tensor Stats <{filepath}>")
    table.add_column("Key")
    table.add_column("Shape")
    table.add_column("Dtype")
    table.add_column("Kilobytes")
    table.add_column("Range")
    for key in tensor_stats:
        table.add_row(
            key,
            str(tensor_stats[key]["shape"]),
            str(tensor_stats[key]["dtype"]),
            str(tensor_stats[key]["nbytes"] / 1024),
            tensor_stats[key]["range"],
        )
    return table


def decompress(in_filepath: str, out_filepath: str):
    lc = LosslessCompressor()
    tensors = {}
    with st.safe_open(in_filepath, "torch") as f:
        metadata = f.metadata()
        keys = f.keys()
        for key in keys:
            tensors[key] = f.get_tensor(key)
        tensor_dtypes = json.loads(metadata["dtype"])
        tensor_shapes = json.loads(metadata["shape"])
    with cp.cuda.Device(0):
        for key in tensors.keys():
            tensors[key] = cp.array(tensors[key], copy=False)
    tensors = lc.decompress_state_dict(
        tensors,
        tensor_shapes,
        tensor_dtypes,
        use_bfloat16=False,
        target_device="cuda:0",
    )
    # save the decompressed tensors
    save_file(tensors, out_filepath)
