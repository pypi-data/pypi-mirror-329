{
    "name": "Prometheus Exporter Coopdevs",
    "summary": """
        Monitor Odoo metrics with Prometheus.
    """,
    "author": "Coopdevs Treball SCCL",
    "website": "https://coopdevs.coop",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["prometheus_exporter"],
    "data": [
        "data/ir_metric.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
