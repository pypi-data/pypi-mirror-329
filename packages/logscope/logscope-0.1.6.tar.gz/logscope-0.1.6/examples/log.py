from logscope import logger

log = logger()

log("Starting application")
log("Processing data", {"count": 100})

def example_function():
    log("Running example function\nfoobar")

example_function()
