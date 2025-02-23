from asyncio import run
from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.raw.functions.channels import ToggleForum
from pyrogram.raw.types import InputChannel
from pyrogram.types import ChatPrivileges, Chat
from src.loader import PG_DSN
from tg_auth import UserStatus
from x_model import init_db
from xync_client.loader import TG_API_ID, TG_API_HASH
from xync_schema import models
from xync_schema.models import Agent

max_privs = ChatPrivileges(
    # can_manage_chat=True,  3 default
    can_delete_messages=True,
    can_manage_video_chats=True,  # Groups and supergroups only
    can_restrict_members=True,
    can_promote_members=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True,  # Groups and supergroups only
    can_manage_topics=True,  # Supergroups only
    is_anonymous=True
)


class PyroClient:
    def __init__(self, agent: Agent):
        self.app: Client = Client(str(agent.user_id), TG_API_ID, TG_API_HASH, session_string=agent.auth["sess"])

    async def create_orders_forum(self, uid: int) -> tuple[int, bool]:
        async with self.app as app:
            app: Client
            forum: Chat = await app.create_supergroup(f"xync{uid}", "Xync Orders")
            if not (_ := await app.toggle_forum_topics(chat_id=forum.id, enabled=True)):
                r = await app.delete_channel(forum.id)
                r = await forum.leave()
                raise Exception(f"Chat {forum.id} for {app.me.username} not converted to forum")
            if added := await forum.add_members(["XyncNetBot"]):  # , "xync_bot"
                await forum.promote_member("XyncNetBot", max_privs)
                added = await forum.add_members([uid])
            else:
                pass
            try:
                await forum.get_member(uid)
            except UserNotParticipant:
                added = False
            # await forum.leave()
            return forum.id, added


async def main():
    _ = await init_db(PG_DSN, models, True)
    agent = await Agent.filter(
        actor__ex__name="TgWallet", auth__isnull=False, user__status__gt=UserStatus.RESTRICTED
    ).first()  # .order_by("-user__created_forums__count")
    pcl = PyroClient(agent)
    res = await pcl.create_orders_forum("cryrub")
    print(res)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from os import getenv as env

    load_dotenv()
    PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
    run(main())
