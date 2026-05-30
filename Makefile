.PHONY: setup data cointegration events backtest regime regime-adaptive all clean help

PYTHON := python
JUPYTER := jupyter nbconvert --execute --to notebook --inplace

help:
	@echo "Targets:"
	@echo "  setup         create venv + install requirements"
	@echo "  data          pull EIA series, build cleaned CSVs"
	@echo "  cointegration run Engle-Granger + Johansen + ECM"
	@echo "  events        run event study + spread-z paths"
	@echo "  backtest      run OOS backtest + PnL"
	@echo "  regime        run rolling-beta regime drift"
	@echo "  regime-adaptive run regime-gated + vol-scaled overlay"
	@echo "  all           run full pipeline end-to-end"
	@echo "  clean         remove processed data + checkpoints"

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

data:
	$(JUPYTER) notebooks/00_data_pull.ipynb

cointegration: data
	$(JUPYTER) notebooks/01_cointegration.ipynb

events: cointegration
	$(JUPYTER) notebooks/02_event_study.ipynb

backtest: events
	$(JUPYTER) notebooks/03_backtest.ipynb

regime: backtest
	$(JUPYTER) notebooks/04_regime_drift.ipynb

regime-adaptive: regime
	$(JUPYTER) notebooks/05_regime_adaptive.ipynb

all: regime-adaptive
	@echo "Pipeline complete. Headline numbers in README.md."

clean:
	rm -rf data/processed/*
	rm -rf notebooks/.ipynb_checkpoints
	rm -rf __pycache__ scripts/__pycache__
