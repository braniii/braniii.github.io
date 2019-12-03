default:
	sass --no-source-map style.scss static/style.css

watch:
	sass --watch --no-source-map style.scss static/style.css

.PHONY: default watch
