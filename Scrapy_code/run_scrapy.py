import sys
import platform
import logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import signal

# Ensure the win32 reactor is used on Windows
if platform.system() == 'Windows':
    try:
        import twisted.internet.win32eventreactor

        twisted.internet.win32eventreactor.install()
    except ImportError:
        import twisted.internet.selectreactor

        twisted.internet.selectreactor.install()
else:
    import twisted.internet.selectreactor

    twisted.internet.selectreactor.install()

from twisted.internet import reactor


# Custom function to start the Scrapy process without signal handling
def run_spider(spider_name):
    configure_logging()
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # Start the crawl
    process.crawl(spider_name)

    # Remove signal handlers to prevent the error
    try:
        # Assuming the process object has a private attribute to store the shutdown handler
        del process._signal_shutdown
    except AttributeError:
        pass

    # Start the reactor without installing signal handlers
    reactor.run(installSignalHandlers=False)


if __name__ == "__main__":
    run_spider('books')
