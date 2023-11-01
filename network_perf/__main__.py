import speedtest
from datetime import timedelta, datetime
import time
import logging
import json
from pathlib import Path

logger = logging.getLogger("network_perf")


def log(r):
    download = r["download"] / 1024 / 1024
    upload = r["upload"] / 1024 / 1024
    ts = datetime.fromisoformat(r["timestamp"]).astimezone()
    logger.info(f"at {ts:%d %b %H:%m} {download=:,.1f} Mb/s, {upload=:,.1f} Mb/s")


def run_once():
    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    logger.info("Testing...")
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    results_dict = s.results.dict()
    log(results_dict)
    return results_dict


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

while True:
    file = Path("results.json")
    try:
        with file.open() as f:
            results = json.load(f)
    except:
        logger.warning(f"Failed to load results from {file}", exc_info=True)
        results = []
    if results:
        log(results[-1])
    result = run_once()
    results.append(result)
    with file.open("w") as f:
        json.dump(results, f, indent=2)
    sleep_duration = timedelta(seconds=60)
    logger.info(f"Sleeping {sleep_duration}...")
    time.sleep(sleep_duration.total_seconds())
