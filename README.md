
# ScrapeYard #

A very simple and naive crawler and article scraper for The New York Times. My purpose for this is to get a better grasp of the Python 3 language while trying out new things such as multiprocessing and asynchronous programming.

## How do I get set up? ##

### Windows ###
* Install the dependencies using `pip install -r requirements.txt`
* Change the settings in `src/settings.py`
* Run the code `python scrapeyard.py`

## Results ##
Note that these benchmarks are absolutely unscientific and extremely flawed. For all I know, I may have had a 1GB Overwatch update taking place in the background as I was running these tests.

#### Crawler (150Mbps internet) ####
I should've used different websites in case New York Times had a limit for a single IP, but I also should've acquired real titration results rather than making values up back in chemistry class. TL;DR, don't hire me as a scientist. In my defence, I couldn't find any results after googling "100 URLs in array or json format."
* Synchronous:  36.47985076904297 seconds
* Asynchronous: 8.674529075622559 seconds

#### Scraper (CPU: i7 5820k) ####
I started by crawling and caching 50 HTML pages. I then duplicated the HTML pages until I had 4896 pages total. These acted as the input files for the scrapers. "Single process" corresponds with scraper.py and Multiprocess (n) means I'm running multiprocess_scraper.py with n processes.

Let's first run these on my hard drive.
##### Hard drive: SATA Barracuda (5400 RPM) #####
* Single process:   201.32148241996765 seconds
* Multiprocess (1): 199.33292937278748 seconds
* Multiprocess (6): 38.622724533081055 seconds

I was curious if those extra $$$ for my $olid$tate$ drive was worth it.
##### Solid state drive: Samsung 850 PRO 256GB #####
* Single process:   186.32595300674438 seconds
* Multiprocess (1): 188.27208900451660 seconds
* Multiprocess (6): 37.963175296783450 seconds

Huh? While the performance gain from increasing the number of processes was expected, I was quite surprised by how close the hard drive (HD) and solid state drive (SSD) results were. I was absolutely certain that the SSD would wipe the floor with the HD. My guess is that the amount of time the CPU took up due to parsing the HTMLs with BeautifulSoup was much greater than the time for the HD/SSD to write the parsed files.

#### Storage Tests: HD vs SSD ####
I removed all parsing functions and have set up the code so that each process will only do a file copy from one directory to another. This was to minimize CPU involvement and focus solely on I/O. I also prepared six Linux ISOs, each around 1.5GB, and set the number of processes to six. From the above results, I'm going to assume that scraper.py and multi_process_scraper.py with one process perform similarly, so I will not test scraper.py.

##### Hard drive: SATA Barracuda (5400 RPM) #####
* Multiprocess (1): 126.35425066947937 seconds
* Multiprocess (6): 764.972131729126 seconds

##### Solid state drive: Samsung 850 PRO 256GB #####
* Multiprocess (1): 38.89297127723694 seconds
* Multiprocess (6): 37.86269783973694 seconds

Look at that performance drop for the HD! I increased the number of Linux ISOs to 24 (35.6GB) to see if the SSD would behave any differently. Spoilers: nothing changed.
##### Solid state drive: Samsung 850 PRO 256GB #####
* Multiprocess (1):  169.43121695518494 seconds
* Multiprocess (24): 163.99551630020142 seconds

#### Summary ####
If the I/O bound is the network, asynchrony, multithreading, and multiprocessing will perform much better than synchrony.

For traditional HDs, asynchrony, multithreading, and multiprocessing will improve performance only when dealing with small files that do not cause a 100% load on the HD activity. If the file is large and saturates the HD activity, then synchrony will be much better. Multiple processes do not, unfortunately, spawn multiple, physical read-write heads. The decrease in performance is due to the single head (or head array) thrashing between multiple locations on the drive platter(s) during context switches from one process copying file A to the other copying file B.

For SSDs, it seems that for small files, asynchrony, multithreading, and multiprocessing will improve performance. However, there will be diminishing returns as the files become bigger. I'm not too informed on SSDs, but I'm guessing that the controller only allows a single file to be written to the drive at a time. However, there is no significant drop off in performance due to the lack of a mechanical read-write head.
