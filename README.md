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

- Create Database and table
- Setup command
  - Ask
    - Bot prefix (DONE)
    - Guild ID (DONE)
    - Alliance ID (DONE)
    - Guild Rol ID (DONE)
    - Alliance Rol ID (DONE)
      - If empty use api alliance tag
  - Confirm values (Prefix, GuildName, GuildTag, AllianceName, AllianceTag, GuildRolName) (DONE)
  - Save values in Database
- Register command
  - Check if user its already registered
  - Add role
  - Change nickname
  - Store in guild database
- Cleanup of users if the arent any more on the guild or alliance
- Command timeouts (DONE)

### TODO Later

- Cleanup users every week, if they arent on the guild and remove from database
