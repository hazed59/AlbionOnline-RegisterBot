# AlbionOnline-RegisterBot

## Setting up

virtualenv -p python3 env
source env/bin/activate
pip install -r requeriments.txt
Create a .env like this:

```env

TOKEN=XXXXXXXXXXXXXXXX

```

## Invite link

Those will be the permissions that the bot will have
![Permissions](./images/permissions_link.png)

### Link

<https://discord.com/oauth2/authorize?client_id=INSERT_CLIENT_ID_HERE&scope=bot&permissions=2617338880>

## Executing the bot

python main.py

## TODO

 - Change nickname on Discord adding tag before nick

 - Store registered users in DB

 - Alliance TAG and ask guild TAG to store in DB

 - Ask for rol to give to guild members

 - Ask for rol to give to alliance members

Cleanup of users if the arent any more on the guild or alliance
