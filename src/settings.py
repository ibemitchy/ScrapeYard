from multiprocessing import cpu_count

# Global settings file
cpu_count = min(cpu_count() - 2, 1)
init_url = "https://www.nytimes.com/"
isASynchronous = True
isMultiprocess = True
max_pages = 100

cache_directory = "./cache"
nyc_regex = "^((http)(s){,1}(://www.)){,1}(nytimes.com/)[\d]{4}(/)[\d]{2}(/)[\d]{2}(/)[^.]*(.html)$"
output_directory = "./output"
