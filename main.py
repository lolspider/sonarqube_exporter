import prometheus_client
import yaml
import json
from flask import Response, Flask
import requests
from requests.auth import HTTPBasicAuth
from src.custom_exporter import *

app = Flask(__name__)


@app.route("/health")
def health_check():
    return Response("OK")


@app.route("/metrics")
def response():
    # get projects list and get projects metrics
    try:
        r = requests.get(url=PROJECT_URL, auth=HTTPBasicAuth(TOKEN, ''))
        components = json.loads(r.text)["components"]
        # for example:  {"lead-management": 70.3}
        for i in components:
            project_metrics_url = METRICS_URL + "&component=%s" % i["key"]
            s = requests.get(url=project_metrics_url, auth=HTTPBasicAuth(TOKEN, ''))
            latest_value = json.loads(s.text)["measures"][0]["history"][-1]["value"]
            projects[i["key"]] = latest_value
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return Response(prometheus_client.generate_latest(CustomCollector("sonarqube_latest_coverage", "sonarqube metrics",
                                                                      projects)), mimetype="text/plain")


if __name__ == '__main__':
    # fetch config
    with open("./config.yaml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    # sonarqube url
    URL = config["SONARQUBE_URL"]
    TOKEN = config["AUTH_TOKEN"]
    # "/api/components/search?qualifiers=TRK&ps=500"
    PROJECT_URL = config["SONARQUBE_URL"] + config["PROJECT_API"]
    # "/api/measures/search_history?metrics=coverage&ps=1000"
    METRICS_URL = config["SONARQUBE_URL"] + config["METRICS_API"]

    projects = {}
    # Start up the server to expose the metrics.
    port = config["PORT"]

    app.run(host="0.0.0.0", port=port)
