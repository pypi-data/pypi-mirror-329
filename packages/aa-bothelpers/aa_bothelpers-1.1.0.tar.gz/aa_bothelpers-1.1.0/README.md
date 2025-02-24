# Bot helpers

Alliance Auth discord bot "helpers".

Various cogs and scripts to do some basic things between alliance auth and discord via the discord bot. Generally on the small side so not worthy of having their own app.

## Features

| Helper | Purpose |
| ------ | ------- |
| `Group Welcome` | Will provide a welcome message in a channel when a user joins a group. Useful for providing further directions to userse joining the group |

## discord bot cogs

| Cog    | Description |
| ------ | ----------- |
| `Links` | Can be access at either /link, /auth, /intel based on wether a link is flagged as an auth link. Links are added via admin |
| `IT` | Various IT related commands. |

## Future features

| Cog    | Purpose |
| ------ | ------- |
| `none` | nothing |

## Install

- Ensure you have installed and configured the Alliance Auth DiscordBot, <https://apps.allianceauth.org/apps/detail/allianceauth-discordbot>
- Install the app with your venv active

```bash
pip install aa-bothelpers
```

- Add `'bothelpers',` to your INSTALLED_APPS list in local.py.
- Add the below lines to your `local.py` settings file, adjust for which cogs you want. Settings for specific cogs are found in cog setup.

```python
BOTHELPERS_COGS = [
        "bothelpers.cogs.it",
        "bothelpers.cogs.links",
    ]
```

- Run migrations `python manage.py migrate`
- Gather your static files `python manage.py collectstatic` (There should be none from this app)
- Restart your auth

## Settings (local.py)

| Setting   | Default | Description |
| --------- | ------- | ----------- |
| `nothing` |         | nothing     |

## Permissions

| Perm              | Description                       |
| ----------------- | --------------------------------- |
| general.Can use IT commands | provide to anyone that needs to be able to use the IT commands |
