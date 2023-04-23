import vk
import json
from .config import VK_TOKEN_USER, VK_MARKET_ID
from collections import defaultdict


def update_info_product():
    product = defaultdict(list)
    key = 0

    vkapi = vk.API(VK_TOKEN_USER)
    market_get = vkapi.market.get(count='50', v=5.131, owner_id=VK_MARKET_ID)

    for elem in market_get['items']:
        if elem['title'] != 'Доставка':
            product[key] = {'id': elem['id'],
                            'title': elem['title'],
                            'description': elem['description'],
                            'price': elem['price'],
                            'url_photo': elem['thumb_photo']
                            }

            key += 1

    return product


def main():
    pass


if __name__ == '__main__':
    main()