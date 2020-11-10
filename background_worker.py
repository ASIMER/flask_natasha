from time import sleep

from control_panel import db_get_rows, dialog_download, profile_dialogs_checker
from db_models import ChatSessions, Profiles


def worker_invites() -> None:
    """Send first messages in dialogue from 1:00 PM to 2:00 PM,
    works in background, time delta: 5 min"""
    # 5 min in seconds
    time_delta = 300

    while True:
        # code
        sleep(time_delta)


def worker_msg_sender() -> None:
    """Send messages with delay,
    works in background with exists dialogs, time delta: 5 min"""
    time_delta = 3600

    while True:
        # code

        # function()
        sleep(time_delta)


def worker_msg_updater() -> None:
    """Check inbox for all profiles with password
    and add new profiles which have written message,
    works in background, time delta: 5 min"""
    """Обновляет диалоги на основе текущих диалогов, не добавляя новые"""
    from main import logger
    time_delta = 3600

    while True:
        # code
        chats = db_get_rows([ChatSessions.chat_id,
                             Profiles.profile_id,
                             Profiles.profile_password],
                            ChatSessions.profile_id == Profiles.profile_id,
                            Profiles.profile_password)
        for chat in chats:
            chat_id = chat[0]
            account_id = chat[1]
            account_pass = chat[2]
            profiles = db_get_rows([
                    Profiles.profile_id
                    ],
                    ChatSessions.profile_id == Profiles.profile_id,
                    ChatSessions.chat_id == chat_id)
            for profile in profiles:
                profile_id = profile[0]
                logger.info(f'Message update worker start load dialog from:'
                            f'account: {account_id} and profile: {profile_id}')
                dialog_download(observer_login=account_id,
                                observer_password=account_pass,
                                sender_id=account_id,
                                receiver_profile_id=profile_id)
                dialog_download(observer_login=account_id,
                                observer_password=account_pass,
                                sender_id=profile_id,
                                receiver_profile_id=profile_id)
                logger.info(f'Message update worker finished load dialog from:'
                            f'account: {account_id} and profile: {profile_id}')
        sleep(time_delta)


def worker_profile_and_msg_updater() -> None:
    """Check inbox for all profiles with password
    and add new profiles which have written message,
    works in background, time delta: 5 min"""
    """Ищет в инбоксе и оутбоксе сообщения, первые 10 страниц, и загружает 
    их, попутно добавляя профиля и диалоги в базу"""
    from main import logger
    time_delta = 3600
    max_page = 3
    while True:
        # code
        profiles = db_get_rows([
                Profiles.profile_id,
                Profiles.profile_password
                ],
                Profiles.profile_password)
        for profile in profiles:
            profile_id = profile[0]
            profile_pass = profile[1]
            logger.info(f'Message update worker start load dialog from:'
                        f'account: {profile_id}')
            profile_dialogs_checker(observed_profile_id=profile_id,
                                    observed_profile_password=profile_pass,
                                    max_page=max_page)
            logger.info(f'Message update worker finished load dialog from:'
                        f'account: {profile_id}')
        sleep(time_delta)


def worker_timer(num) -> None:
    """Check inbox for all profiles with password
    and add new profiles which have written message,
    works in background, time delta: 5 min"""
    time_delta = 1
    i = 1
    while True:
        # code
        print(f"{num}: {i}")
        i += 1
