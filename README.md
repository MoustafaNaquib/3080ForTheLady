# 3080 For The Lady

## Description
Bot that attempts to add 3080s into your cart on multiple online retailers. Sends a text notification if successful.
Currently supports BestBuy.


## Prerequisites:
Must have python 3 installed.
Create a free Twilio account @ https://www.twilio.com/

## Dependencies:
```python
pip install requests
pip install twilio>=6.0.0
```

## Development setup:
Follow these instructions to execute the script locally.

Update args.txt to include your information.

Example:
```text
--twilio_account=ACxxxxxxxxxxx
--twilio_token=xxxxxxxxxx
--twilio_number=+12222222222
--numbers=+133333333,+144444444,+1555555555 # Numbers to send text alert to
--stock_check_interval=10 # Seconds between inventory checks
```

Execute script using following command:
```python
python thrity80_bot.py @args.txt
```

