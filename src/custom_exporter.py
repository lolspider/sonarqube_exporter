from prometheus_client.core import GaugeMetricFamily


class CustomCollector(object):
    def __init__(self, metric_name, doc, projects):
        self._metric_name = metric_name
        self._doc = doc
        self._projects = projects

    def collect(self):
        for k, v in self._projects.items():
            g = GaugeMetricFamily(self._metric_name, self._doc, labels=["project"])
            g.add_metric([k], v)
            yield g
