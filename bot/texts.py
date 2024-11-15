from core.models import Text


# TODO: these functions are not efficient, these may cause unneeded load into database.
# getting text must be in another approach.
# like loading all in startup, then using a message broker and after changes do a reload
# or just reload text from database within intervals (like one minute)

async def get_message_text(_title: str, **kwargs) -> str:
    """Get live message text from database. return `empty` if not found"""
    button = await Text.objects.filter(title=_title).afirst()
    text = button.text if button else "empty"
    for key in kwargs:
        text = text.replace(key.upper(), f"{kwargs[key]:,}" if isinstance(kwargs[key], int) else str(kwargs[key]))
    return text


async def get_button_text(_title: str, **kwargs) -> str:
    """Get live button text from database. return `empty` if not found"""
    message: Text = await Text.objects.filter(title=_title, is_button=True).afirst()
    text = message.text if message else "empty"
    for key in kwargs:
        text = text.replace(key.upper(), f"{kwargs[key]:,}" if isinstance(kwargs[key], int) else str(kwargs[key]))
    return text
