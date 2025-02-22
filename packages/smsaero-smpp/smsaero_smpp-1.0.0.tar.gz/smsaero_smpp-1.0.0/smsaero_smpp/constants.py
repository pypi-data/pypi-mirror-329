"""
Модуль с константами для SMPP клиента.
"""

# Маппинг SMPP статусов
STATUS_MAPPING = {
    "0": "unknown",  # UNKNOWN
    "1": "enroute",  # ENROUTE
    "2": "delivered",  # DELIVERED
    "3": "expired",  # EXPIRED
    "4": "deleted",  # DELETED
    "5": "undeliverable",  # UNDELIVERABLE
    "6": "accepted",  # ACCEPTED
    "7": "invalid",  # INVALID
    "8": "rejected",  # REJECTED
}

# Множество финальных статусов
FINAL_STATUSES = {"delivered", "expired", "deleted", "undeliverable", "rejected"}

# PDU команды
PDU_SUBMIT_SM_RESP = "submit_sm_resp"
PDU_DELIVER_SM = "deliver_sm"
PDU_QUERY_SM_RESP = "query_sm_resp"
PDU_GENERIC_NACK = "generic_nack"
