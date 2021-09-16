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
    - Bot prefix (PARTIAL, MISSING DATAQBASE VARIABLE IN PREFIX)
    - Guild ID (DONE)
    - Alliance ID (DONE)
    - Guild Rol ID (DONE)
    - Alliance Rol ID (DONE)
  - Confirm values (Prefix, GuildName, GuildTag, AllianceName, AllianceTag, GuildRolName) (DONE)
  - Save values in Database (DONE)
- Register command
  - Check if user its already registered
  - Add role (DONE)
  - Change nickname (DONE)
  - Store in guild database
- Blacklist command
- Cleanup of users if the arent any more on the guild or alliance
- Command timeouts (DONE)
- Unregister command (Para usuarios)
- forceUnregister command (Unregister user, para los que tengan permisos de adminstrar roles)

### TODO Later

- Cleanup users every week, if they arent on the guild and remove from database
