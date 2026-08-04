{{- define "service-chart.name" -}}
{{- .Values.nameOverride | default .Chart.Name -}}
{{- end -}}
