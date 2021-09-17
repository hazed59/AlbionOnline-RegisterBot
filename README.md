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

pip install -r requeriments.txt

python main.py

## TODO

- [X] Create Database and table (DONE)
- [ ] Custom bot prefix
- Setup command
  - Ask
    - [X] Bot prefix (DONE)
    - [X] Guild ID (DONE)
    - [X] Alliance ID (DONE)
    - [X] Guild Rol ID (DONE)
    - [X] Alliance Rol ID (DONE)
    - [ ] Update sql insert to avoid duplicate rows
  - [X] Confirm values (Prefix, GuildName, GuildTag, AllianceName, AllianceTag, GuildRolName) (DONE)
  - [X] Save values in Database (DONE)
- Register command
  - [X] Check if user its already registered
  - [X] Add role (DONE)
  - [X] Change nickname (DONE)
  - [X] Store users in guild database
  - [ ] Update sql SELECT to get data from GUILD instead of return every value and get first
  - [ ] Check from all guilds/alliances (separator a ',')
- addGuild command
  - [ ] Add Guild to exit field (separator a ',')
- addAlliance command
  - [ ] Add Alliance to exit field (separator a ',')
- [X] Command timeouts (DONE)
- [X] Auto-clean commands or whole channel

### TODO Later

- [ ] Blacklist command
- [ ] Cleanup of users if the arent any more on the guild or alliance
- [X] Unregister command (Para usuarios)
- [ ] forceUnregister command (Unregister user, for users with manage roles permission, por si está blacklisted)
- [ ] Send query to guild and save all members every X minutes, avoiding spamming the API
- [ ] Cleanup users every day, if they arent on the guild and remove from database
