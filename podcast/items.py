# author: @arthurnn89

from scrapy.item import Item, Field

class PodcastItem(Item):
	title = Field()
	author = Field()
	price = Field()
	category = Field()
	lang = Field()
	website = Field()
	email = Field()
