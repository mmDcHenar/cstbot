from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, types

from core.models import TGUser


class DBUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Update, dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: dict[str, Any],
            **kwargs: Any
    ) -> Any:
        user = data["event_from_user"]
        db_user, _ = await TGUser.objects.aupdate_or_create(
            id=user.id,
            defaults={"full_name": user.full_name, "username": user.username},
        )
        if db_user.is_banned:
            return
        data["db_user"] = db_user
        return await handler(event, data)
