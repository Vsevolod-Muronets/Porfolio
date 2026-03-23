#!/bin/bash

curl -G "https://api.hh.ru/vacancies?per_page=20&text=$1%20$2&search_field=name" | jq '{page, found, clusters, arguments, per_page, pages,
	items}' > hh.json
