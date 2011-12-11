# Scrapy settings for podcast project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
LOG_LEVEL = 'INFO'

BOT_NAME = 'podcast'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['podcast.spiders']
NEWSPIDER_MODULE = 'podcast.spiders'
DEFAULT_ITEM_CLASS = 'scrapy.item.Item'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)


ITEM_PIPELINES = (
    'podcast.pipelines.MySQLStorePipeline',
)


DEPTH_LIMIT=7
CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 16