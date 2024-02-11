
# Order Assist ChatBot

## How to run the app?

Create a python3 environment (<=3.8.x)

```bash
  python3 -m venv venv
```

Activate environment

```bash
  source venv/bin/activate
```
Keyword "source" is not required for windows users.

Install Requirements

```bash
  pip3 install -r requirements.txt
```
Add your API keys in `actions/.env`.
In the project directory, first create a folder `models`. Open two terminals with virtual environment activated, In the first tab run:

```bash
  rasa train && rasa shell
```
running `rasa train` is only required once for training the model.

In the second tab run:

```bash
   cd actions && rasa run actions
```

