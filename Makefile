# RareDiseaseHedge — one place for the whole pipeline + site build.
# The manual 6-step chain (fetch -> diff -> enrich -> ui -> report -> deploy) is
# what made refreshes error-prone; every step now has a target and `make all`
# runs them in order. `make test` gates changes on the accuracy harness.
#
#   make deps      install Python deps
#   make fetch     refresh source data (skips dead/manual sources gracefully)
#   make pipeline  run the candidate-discovery diff -> summary.json
#   make enrich    add PubMed/trials/ChEMBL/Orphadata/EU-orphan/CRL/eligibility
#   make ui        build the card-list dashboard (pipeline/ui)
#   make report    build the almanac data + assemble the deployable _site/
#   make deploy    push _site/ to Cloudflare Pages (needs wrangler auth)
#   make test      offline accuracy harness (fast, no data/network)
#   make test-real accuracy harness against the real data files
#   make check     data-integrity assertions against summary.json
#   make all       fetch -> pipeline -> enrich -> ui -> report  (no deploy)
#   make refresh   all + check + deploy

PY := python3
PIPE := pipeline
PROJECT := rarediseasehedge

.PHONY: deps fetch pipeline enrich ui report site deploy test test-real check all refresh clean

deps:
	$(PY) -m pip install -r $(PIPE)/requirements.txt

fetch:
	$(PY) $(PIPE)/fetch.py

pipeline:
	$(PY) $(PIPE)/rdh_diff.py

enrich:
	$(PY) $(PIPE)/enrich.py

ui:
	$(PY) $(PIPE)/build_ui.py

report:
	$(PY) $(PIPE)/report/build_report_data.py
	$(PY) $(PIPE)/report/build_site.py

site: report

deploy:
	npx --yes wrangler@latest pages deploy $(PIPE)/report/_site \
	  --project-name=$(PROJECT) --branch=main --commit-dirty=true

test:
	$(PY) $(PIPE)/test_accuracy.py

test-real:
	$(PY) $(PIPE)/test_accuracy.py --real

check:
	$(PY) $(PIPE)/test_data_integrity.py

all: pipeline enrich ui report

refresh: fetch all check deploy

clean:
	rm -rf $(PIPE)/report/_site
