import os
from urllib.parse import quote_plus


def whatsapp_context(_request):
    number = os.getenv("WHATSAPP_NUMBER", "77076307165").strip()
    message = os.getenv(
        "WHATSAPP_MESSAGE",
        "Сәлеметсіз Qundylyq, кеңес алуға бола ма?",
    ).strip()
    return {
        "whatsapp_url": f"https://wa.me/{number}?text={quote_plus(message)}"
    }

