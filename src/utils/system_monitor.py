import argparse
import os
import subprocess as sp
import time

import mlflow
import psutil


def get_gpu_mem_info():
    output_to_list = lambda x: x.decode("ascii").split("\n")[:-1]
    COMMAND = "nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv"

    try:
        memory_use_info = output_to_list(sp.check_output(COMMAND.split(), stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError(f"command '{e.cmd}' return with error (code {e.returncode}): {e.output}")
    return memory_use_info


def get_dist_info():
    dist_info_config = {
        "node_rank": "NODE_RANK",
        "local_rank": "LOCAL_RANK",
        "world_rank": "RANK",
        "world_size": "WORLD_SIZE",
    }

    dist_info = {key: os.environ.get(value) for key, value in dist_info_config.items()}

    # Single GPU job
    if dist_info["world_size"] is None:
        dist_info["node_rank"] = 0
        dist_info["world_rank"] = 0
        dist_info["local_rank"] = 0
        dist_info["world_size"] = 1

    dist_info = {key: int(value) for (key, value) in dist_info.items()}
    return dist_info


def main(args):
    # run on each node but only on one process corresponding to first gpu
    dist_info = get_dist_info()
    if not (dist_info["local_rank"] == 0):
        return

    node_rank = dist_info["node_rank"] + 1  # one index for display

    metrics = {}
    metrics = {
        f"monitor/node_{node_rank:02}/ram_usage_percent": 0.0,
        f"monitor/node_{node_rank:02}/ram_usage_GB": 0.0,
        f"monitor/node_{node_rank:02}/cpu_usage_percent": 0.0,
        f"monitor/node_{node_rank:02}/swap": 0.0,
    }

    memory_use_info_list = get_gpu_mem_info()
    idx, gpu_percent, gpu_mem_used, gpu_mem_total = memory_use_info_list[0].split(",")
    gpu_mem_total = float(gpu_mem_total.split("MiB")[0])

    for gpu_idx, gpu_info in enumerate(memory_use_info_list, 1):
        metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/usage_percent"] = 0.0
        metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/mem_used_GB"] = 0.0
        metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/mem_used_percent"] = 0.0

    now = 0
    dt_sleep = args.watch_every_n_seconds

    while True:
        metrics[f"monitor/node_{node_rank:02}/ram_usage_GB"] = psutil.virtual_memory().used / 2**30
        metrics[f"monitor/node_{node_rank:02}/ram_usage_percent"] = psutil.virtual_memory().percent
        metrics[f"monitor/node_{node_rank:02}/cpu_usage_percent"] = psutil.cpu_percent()
        metrics[f"monitor/node_{node_rank:02}/swap"] = psutil.swap_memory().percent

        memory_use_info_list = get_gpu_mem_info()
        for gpu_idx, gpu_info in enumerate(memory_use_info_list, 1):
            _, gpu_percent, gpu_mem_used, _ = gpu_info.split(",")
            gpu_percent = float(gpu_percent.split("%")[0])
            gpu_mem_used = float(gpu_mem_used.split("MiB")[0])
            gpu_mem_percent = gpu_mem_used / gpu_mem_total * 100.0
            gpu_mem_used /= 1024.0

            metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/usage_percent"] = gpu_percent
            metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/mem_used_GB"] = gpu_mem_used
            metrics[f"monitor/node_{node_rank:02}/gpu_{gpu_idx:02}/mem_used_percent"] = gpu_mem_percent

        # for key, value in metrics.items():
        #     print(f"{key}: {value}")
        mlflow.log_metrics(metrics, step=now)

        time.sleep(dt_sleep)
        now += dt_sleep


def get_parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch_every_n_seconds", type=int, default=5)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("system_monitor.py begins")
    args = get_parsed_args()
    main(args)
    print("system_monitor.py done")
