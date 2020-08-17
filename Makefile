.PHONEY: lint format unit integration diff deploy destroy

lint:
	PIPENV_DOTENV_LOCATION=.env pipenv run flake8 .
	PIPENV_DOTENV_LOCATION=.env pipenv run isort --check-only --profile black .
	PIPENV_DOTENV_LOCATION=.env pipenv run black --check --diff .

format:
	PIPENV_DOTENV_LOCATION=.env pipenv run isort --profile black .
	PIPENV_DOTENV_LOCATION=.env pipenv run black .

unit:
	PIPENV_DOTENV_LOCATION=.env pipenv run pytest -s tests/unit

integration:
	PIPENV_DOTENV_LOCATION=.env pipenv run pytest -s tests/integration

diff:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk diff --app stack/app.py || true

deploy:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk deploy --app stack/app.py --require-approval never

destroy:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk destroy --force --app stack/app.py
