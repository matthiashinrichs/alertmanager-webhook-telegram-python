# alertmanager-webhook-telegram-python
A webhook receiver for prometheus' alertmanager to alert via telegram

Send alerts via telegram bot. Run it locally, in Docker or Kubernetes.

To get it to work you need to change the following values:
- `chatID`
- `botToken`

You can enable basic auth by setting these values:

`app.config['BASIC_AUTH_FORCE'] = True`

`app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'`

`app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'`


Set `app.config['BASIC_AUTH_FORCE'] = False` to completely disable basic auth.

If you run it in Docker the values in ENV variables, see `docker-compose.yaml.example`.
This will overwrite the default values.

You can test if it's working:
---
```
curl -XPOST --data '{"receiver":"telegram-webhook","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"Watchdog","prometheus":"monitoring/prometheus-operator-prometheus","severity":"none"},"annotations":{"message":"This is an alert meant to ensure that the entire alerting pipeline is functional.\\nThis alert is always firing, therefore it should always be firing in Alertmanager\\nand always fire against a receiver. There are integrations with various notification\\nmechanisms that send a notification when this alert is not firing. For example the\\n\"DeadMansSnitch\" integration in PagerDuty.\\n"},"startsAt":"2020-04-25T11:13:15.47Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prometheus.k8s.hnrx.local/graph?g0.expr=vector%281%29&g0.tab=1","fingerprint":"3ab1c4d83af12d03"}],"groupLabels":{},"commonLabels":{"alertname":"Watchdog","prometheus":"monitoring/prometheus-operator-prometheus","severity":"none"},"commonAnnotations":{"message":"This is an alert meant to ensure that the entire alerting pipeline is functional.\\nThis alert is always firing, therefore it should always be firing in Alertmanager\\nand always fire against a receiver. There are integrations with various notification\\nmechanisms that send a notification when this alert is not firing. For example the\\n\"DeadMansSnitch\" integration in PagerDuty.\\n"},"externalURL":"http://alertmanager.k8s.hnrx.local","version":"4","groupKey":"{}/{job=~\"^(?:.*)$\"}:{}"}' http://localhost:9119/alert
```

Webhook configuration in prometheus:
---
```
route:
  receiver: telegram-webhook
  group_by:
  - instance
  - job
  routes:
  - receiver: telegram-webhook
    match_re:
      job: .*
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
receivers:
- name: telegram-webhook
  webhook_configs:
  - send_resolved: true
    http_config:
      basic_auth:
	      username: 'admin'
	      password: 'password'
    url: http://alertmanager-webhook-telegram-python:9119/alert
```
