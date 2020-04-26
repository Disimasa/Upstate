import json
import logging
from typing import List

from unibots.tools import cut_text

VK_ALLOWED_COLORS = {'primary', 'secondary', 'negative', 'positive'}


class Button:
    hide: bool = False  # for Alice

    def __init__(self, text: str, color: str = 'secondary',
                 url: str or None = None, callback: str or None = None):
        if callback is None:
            callback = text
        if color not in VK_ALLOWED_COLORS:
            raise ValueError(f'Color for VK must be chosen from these: {", ".join(VK_ALLOWED_COLORS)}')

        self.text = text          # Everywhere
        self.color = color        # VK
        self.url = url            # Everywhere
        self.callback = callback  # Everywhere

    @property
    def vk_button(self) -> dict:
        # FIXME добавить callback в Payload
        formed = {'action': {'type': 'text', 'payload': '', 'label': self.text}, 'color': self.color}
        if self.url is not None:
            formed['action']['link'] = self.url
            formed['action']['type'] = 'open_link'
        return formed

    @property
    def telegram_button(self) -> dict:
        formed = {'text': self.text}
        if self.url is not None:
            formed['url'] = self.url
        elif self.callback is not None:
            formed['callback_data'] = self.callback
        return formed

    @property
    def alice_button(self) -> dict:
        formed = {'title': self.text, 'payload': {'text': self.callback}, 'hide': self.hide}
        if self.url is not None:
            formed['url'] = self.url
        return formed

    def __repr__(self):
        self.__str__()

    def __str__(self):
        return json.dumps(f'{self.text}')


class Keyboard:
    def __init__(self, buttons: List[List[Button]], hide: bool = False, inline: bool = False, resize: bool = True):
        self.buttons = buttons  # Everywhere
        self.hide = hide  # Everywhere
        self.inline = inline  # Everywhere
        self.resize = resize  # Tg TODO should be departed

    @property
    def vk_keyboard(self) -> dict:
        # Very important! Buttons will not work without ensure_ascii=True
        # Also really bad crunch from VK to accept json as string inside json (0_o)
        if self.inline and self.hide:
            logging.warning('Inline buttons can`t be hidden after click! hide=True will be ignored')
        return json.dumps({
            'one_time': self.hide if not self.inline else False, 'inline': self.inline,
            'buttons': [[button.vk_button for button in row] for row in self.buttons]
        }, ensure_ascii=False)

    @property
    def telegram_keyboard(self) -> dict:
        buttons = [[button.telegram_button for button in row] for row in self.buttons]
        if self.inline:
            logging.warning('Inline buttons can`t be hidden after click! hide=True will be ignored')
            return json.dumps({'inline_keyboard': buttons})
        return json.dumps({'keyboard': buttons, 'resize_keyboard': self.resize, 'one_time_keyboard': self.hide})

    @property
    def alice_keyboard(self) -> List[dict]:
        formed = list()
        for row in self.buttons:
            for button in row:
                # Buttons in Alice are inlined if they have hide=False
                button.hide = self.hide and not self.inline
                formed.append(button.alice_button)
        return formed

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n'.join('\t'.join(str(button) for button in row) for row in self.buttons)


class Card:
    def __init__(self, alice_id=None, telegram_id=None, vk_id=None, path=None, title='', description=''):
        self.alice_id = alice_id
        self.telegram_id = telegram_id
        self.vk_id = vk_id
        self.path = path

        self.title = title
        self.description = description

    @property
    def alice_card(self) -> dict:
        title = cut_text(
            self.title, 128,
            'Title length must be less then 128 symbols. Title will be cut!'
        )

        description = cut_text(
            self.description, 256,
            'Description length must be less then 256 symbols. Title will be cut!'
        )
        # TODO Протестировать поведение api с type: BigImage внутри itemlist
        # TODO добавить кнопку, если в этом есть необходимость
        return {'type': 'BigImage', 'image_id': self.alice_id, 'title': title, 'description': description}

    @property
    def vk_card(self) -> dict:
        return {'attachment': self.vk_id, 'message': self.caption}

    @property
    def caption(self):
        return self.title + '\n' + self.description

    @property
    def telegram_card(self) -> (str, str):
        return self.telegram_id if self.telegram_id is not None else self.path, self.caption

    def __str__(self):
        return '\n-------------------------------------\n' \
               f'{self.caption}\n{self.alice_id}/{self.telegram_id}/{self.vk_id}' \
               '\n-------------------------------------\n'

    def __repr__(self):
        return self.__str__()


class Gallery:
    def __init__(self, cards: List[Card], header: str = '', split: bool = False):
        self.cards = cards
        self.header = header
        self.split = split

    @property
    def alice_gallery(self) -> dict:
        cards = self.cards
        if len(self.cards) > 5:
            logging.warning('Maximum amount of images for Yandex Dialogs is 5! '
                            'Images with indexes greater then 4 will be dropped')
            cards = self.cards[:5]
        return {
            'type': 'ItemsList',
            "header": {"text": self.header},
            "items": [card.alice_card for card in cards],
        }

    @property
    def telegram_gallery(self):
        return self

    @property
    def vk_gallery(self):
        if self.split:
            return [{'message': self.header}, ] + [card.vk_card for card in self.cards]
        return [{'attachment': ','.join(card.vk_id for card in self.cards), 'message': self.header}]
