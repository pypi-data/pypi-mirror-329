#!/usr/bin/env python3

import logging

from prometheus_client import Gauge, start_http_server
from datetime import datetime
import time
from the_conf import TheConf
from yfinance import Ticker

metaconf = {
    "source_order": ["env", "files"],
    "config_files": [
        "~/.config/yfinance-exporter.json",
        "/etc/yfinance-exporter/yfinance-exporter.json",
    ],
    "parameters": [
        {"name": {"default": "yfinance-exporter"}},
        {
            "type": "list",
            "stocks": [
                {"name": {"type": str}},
                {"isin": {"type": str}},
                {"ycode": {"type": str}},
            ],
        },
        {"loop": [{"interval": {"type": int, "default": 240}}]},
        {
            "prometheus": [
                {"port": {"type": int, "default": 9100}},
                {"namespace": {"type": str, "default": ""}},
            ]
        },
        {"logging": [{"level": {"default": "WARNING"}}]},
    ],
}
conf = TheConf(metaconf)
logger = logging.getLogger("yfinance-exporter")
try:
    logger.setLevel(getattr(logging, conf.logging.level))
    logger.addHandler(logging.StreamHandler())
except AttributeError as error:
    raise AttributeError(
        f"{conf.logging.level} isn't accepted, only DEBUG, INFO, WARNING, "
        "ERROR and FATAL are accepted"
    ) from error

DAEMON = Gauge("daemon", "", ["name", "section", "status"])
STOCK = Gauge(
    "financial_positions",
    "",
    [
        "bank",
        "account_type",
        "account_name",
        "account_id",
        "line_name",
        "line_id",
        "value_type",  # par-value, shares-value, gain, gain-percent, quantity
    ],
    namespace=conf.prometheus.namespace,
)


def collect(stock):
    logger.debug("Collecting for %r", stock.name)
    labels = [
        stock.ycode.split(".")[1] if "." in stock.ycode else "",
        "stocks",
        "market",
        "market",
        stock.name,
        stock.isin,
        "par-value",
    ]
    ticker = Ticker(stock.ycode)
    try:
        value = ticker.fast_info["last_price"]
    except KeyError:
        value = None
    if not isinstance(value, (int, float)):
        try:
            STOCK.remove(*labels)
        except KeyError:
            pass
        return False
    STOCK.labels(*labels).set(value)
    return True


def main():
    labels = {"name": conf.name, "section": "config"}
    DAEMON.labels(status="loop-period", **labels).set(conf.loop.interval)
    DAEMON.labels(status="item-count", **labels).set(len(conf.stocks))

    labels["section"] = "exec"
    while True:
        start = datetime.now()
        DAEMON.labels(status="items-ok", **labels).set(0)
        DAEMON.labels(status="items-ko", **labels).set(0)

        for stock in conf.stocks:
            if collect(stock):
                DAEMON.labels(status="items-ok", **labels).inc()
            else:
                DAEMON.labels(status="items-ko", **labels).inc()

        exec_interval = (datetime.now() - start).total_seconds()
        DAEMON.labels(status="exec-time", **labels).set(exec_interval)
        DAEMON.labels(status="loop-count", **labels).inc()
        interval = conf.loop.interval - exec_interval
        if interval > 0:
            time.sleep(interval)


if __name__ == "__main__":
    logger.info(
        "Starting yfinance exporter with %d stocks to watch", len(conf.stocks)
    )
    start_http_server(conf.prometheus.port)
    main()
