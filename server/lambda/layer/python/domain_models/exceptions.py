

class LogicalException(Exception):
    pass


class WebsiteNotFoundException(LogicalException):
    def __init__(self, website_id):
        super().__init__(f"Unable to find website with ID {website_id}")


class ScrapeNotFoundException(LogicalException):
    def __init__(self, scrape_id):
        super().__init__(f"Unable to find scrape with ID {scrape_id}")


class ScreenshotNotFoundException(LogicalException):
    def __init__(self, key):
        super().__init__(f"Unable to find screenshot at location {key}")


class InvalidRequestException(LogicalException):
    pass
