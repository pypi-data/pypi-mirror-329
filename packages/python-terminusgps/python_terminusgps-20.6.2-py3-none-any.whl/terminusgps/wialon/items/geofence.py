from django.db import models

from terminusgps.wialon.items.base import WialonBase


class WialonGeofence(WialonBase):
    def __new__(cls) -> "WialonGeofence":
        raise NotImplementedError()

    class WialonGeofenceShape(models.IntegerChoices):
        LINE = 1
        POLYGON = 2
        CIRCLE = 3

    class WialonGeofenceColor(models.IntegerChoices):
        RED = int("ff0000", 16)
        ORANGE = int("ff7b00", 16)
        YELLOW = int("fffb00", 16)
        GREEN = int("20ff00", 16)
        BLUE = int("0090ff", 16)
        PURPLE = int("7000ff", 16)
        WHITE = int("f3f3f3", 16)
        BLACK = int("030303", 16)

    def create(
        self,
        resource_id: str | int,
        name: str,
        xpos: float,
        ypos: float,
        desc: str | None = None,
        shape: int = WialonGeofenceShape.CIRCLE,
        width: int = 100,
        flags: int = 0x04,
        color: int = WialonGeofenceColor.GREEN,
        text_color: int = WialonGeofenceColor.BLACK,
        text_size: int = 12,
        min_zoom: int = 2,
        max_zoom: int = 19,
    ) -> int | None:
        response = self.session.wialon_api.resource_update_zone(
            **{
                "itemId": resource_id,
                "id": 0,
                "callMode": "create",
                "n": name,
                "d": desc if desc else name,
                "t": shape,
                "w": width,
                "f": flags,
                "c": color,
                "tc": text_color,
                "ts": text_size,
                "min": min_zoom,
                "max": max_zoom,
                "p": [{"x": xpos, "y": ypos, "r": width}],
            }
        )
        if response:
            return int(response[0])
