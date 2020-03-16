from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .device import Device
from .message import Message
from .rec_items import RecItems
