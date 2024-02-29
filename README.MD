Telegram bot creation

* `scraper.py` Scrapes data from group and add it to db
* `train_model.py` Uses the scraped data and creates a model
* `telegram_bod.py` The bot that uses the data

## Configurations
`Bot id: qjndhepncdhepnchohi_bot`

# Tensorflow
https://github.com/deganza/Install-TensorFlow-on-Mac-M1-GPU/blob/main/Install-TensorFlow-on-Mac-M1-GPU.ipynb

## Install miniconda as a package
```
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg
```

## Create a virtual environment
```
$ mkdir <project name>
$ cd <project name>
$ conda create --prefix ./env python=3.9
$ conda activate ./env
```
The reference to the environment will no be located at `<project name>/env` and `conda activate <project name>/env` can be used to activate

## Install tensorflow
```
$ conda install -c apple tensorflow-deps
$ pip3 install tensorflow-macos
$ pip3 install tensorflow-metal
```
# Telegram Bot
```
$ pip3 install telegram
$ pip3 install python-telegram-bot
```

## Open telegram app 
And ´Start´ a conversation with "@Botfather" (search the user)

/newbot

(enter name)


# Telegram scraper
```
$ pip3 install telethon pandas nltk
```
## Get channel id
To get the identifier of a Telegram group or channel in which a user is the admin, the user should do the following:
1. Navigate to a Telegram group or channel whose identifier the user wants to get.
2. Add @getidsbot to the selected group or channel and get the response containing the group or channel identifier.
3. Copy the obtained identifier and paste it to the Group Id field displayed under the enabled Telegram option when configuring event notifications.

# CREATE A CONFIG 
FILE CALLED `secret_config.json`
```
{
    "bot_token": "<bot token>",
    "bot_name": "<name of the generateh bod>",
    "api_hash": "<telegram api hash for scraping>",
    "api_id": "<telegram ap id for scraping>",
    "api_phone": "<telegram phone for scraping-verification>"
}
```