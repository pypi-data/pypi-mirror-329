# `init-data-python`
A Python library that offers simple interface for validating Telegram Mini App initialization data.

# Installation
```bash
pip install init-data-python
```

# Usage
Instantiate `InitData` with raw initialization data and a bot token, then call `.validate()` to get the validation
result as a boolean.
```python
from init_data import InitData

init_data_raw = "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A279058397%2C%22first_name%22%3A%22Vladislav%22%2C%22last_name%22%3A%22Kibenko%22%2C%22username%22%3A%22vdkfrost%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%7D&auth_date=1662771648&hash=c501b71e775f74ce10e377dea85a7ea24ecd640b223ea86dfe453e0eaed2e2b2"
bot_token = "5768337691:AAH5YkoiEuPk8-FZa32hStHTqXiLPtAEhx8"

InitData(init_data_raw, bot_token).validate() # -> True
```
You can also specify the number of decoding iterations if the initialization data was encoded multiple times.
```python
InitData(...).validate(times_to_decode=2)
```
- Note: `times_to_decode` is a keyword-only parameter.