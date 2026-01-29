import inspect
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import ContextInfo


class MyFunc:
    def __init__(self, client):
        self.client = client
        # key: Chat.User (str)
        self._expiration_map = {}
        self._patch_send_methods()

    def _patch_send_methods(self):
        for attr_name in dir(self.client):
            if attr_name.startswith('send_') and not attr_name.startswith('_') and attr_name.endswith(("video","image","sticker","message","audio")):
                original_method = getattr(self.client, attr_name)
                if inspect.iscoroutinefunction(original_method):
                    patched_method = self._create_patched_method(original_method)
                    setattr(self.client, attr_name, patched_method)

    def _create_patched_method(self, original_method):
        async def patched_send(*args, **kwargs):
            try:
                if args:
                    chat_jid = args[0]
                    if hasattr(chat_jid, 'User'):
                        jid_key = chat_jid.User
                        expiration = self._expiration_map.get(jid_key, 0)

                        if expiration > 0:
                            auto_context = ContextInfo(expiration=expiration)
                            user_context = kwargs.get("context_info")

                            if user_context is None:
                                # Tidak ada context_info dari user → gunakan auto
                                kwargs["context_info"] = auto_context
                            else:
                                # Ada context_info dari user → gabungkan
                                merged = ContextInfo()
                                merged.CopyFrom(user_context)
                                # MergeFrom tidak overwrite field yang sudah di-set,
                                # jadi expiration hanya ditambah jika belum ada.
                                merged.MergeFrom(auto_context)
                                kwargs["context_info"] = merged
            except (AttributeError, TypeError, ValueError):
                # Abaikan error struktur JID atau protobuf
                pass
            except Exception:
                # Jangan hentikan pengiriman hanya karena gagal inject context
                pass

            return await original_method(*args, **kwargs)

        return patched_send

    def set_expiration(self, chat_user: str, expiration: int):
        """Set expiration (dalam detik) untuk chat dengan user tertentu."""
        if expiration < 0:
            expiration = 0
        self._expiration_map[chat_user] = expiration

    def get_expiration(self, chat_user: str) -> int:
        return self._expiration_map.get(chat_user, 0)