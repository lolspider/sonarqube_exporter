This project is to collect coverage metrics in sonarqube, now only support coverage metric.

### Change below env in config.yaml if necessary
```
PORT: 8991
SONARQUBE_URL: https://sonarqube.projects.com.cn
AUTH_TOKEN: "*********"
PROJECT_API: "/api/components/search?qualifiers=TRK&ps=500"
METRICS_API: "/api/measures/search_history?metrics=coverage&ps=1000"
```

### Run
```
python3 main.py
```

### Access
```
localhost:8991/metrics
```