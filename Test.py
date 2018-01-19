import aiohttp
import asyncio
import time
import requests

urls = ["https://www.nytimes.com/",
        "https://www.nytimes.com/2018/01/18/books/mark-epstein-advice-not-given.html",
        "https://www.nytimes.com/2018/01/17/opinion/treating-opioid-addiction.html",
        "https://www.nytimes.com/2018/01/17/well/move/how-our-bones-might-help-keep-our-weight-stable.html",
        "https://www.nytimes.com/2018/01/18/smarter-living/how-to-maintain-friends.html",
        "https://www.nytimes.com/2018/01/18/opinion/obama-prisoners-clemency.html",
        "https://www.nytimes.com/2018/01/16/science/tails-weapons-dinosaurs.html",
        "https://www.nytimes.com/2018/01/18/travel/five-places-to-go-in-los-angeles-highland-park.html",
        "https://www.nytimes.com/2018/01/18/opinion/violence-pacification-vietnam-war.html",
        "https://www.nytimes.com/2018/01/17/travel/winter-olympics-trip-planning.html",
        "https://www.nytimes.com/2018/01/18/dining/drinks/beer-ipa-sam-adams-sierra-nevada.html",
        "https://www.nytimes.com/2018/01/18/opinion/productivity-saving-careers.html",
        "https://www.nytimes.com/2018/01/16/magazine/beyond-the-bitcoin-bubble.html",
        "https://www.nytimes.com/2018/01/18/world/asia/north-korea-oil-smuggling.html",
        "https://www.nytimes.com/2018/01/18/business/economy/tax-housing.html",
        "https://www.nytimes.com/2018/01/18/opinion/government-shutdown-chip-republicans.html",
        "https://www.nytimes.com/video/us/100000005684789/cities-bizarre-bids-to-be-amazons-new-home.html",
        "https://www.nytimes.com/2018/01/18/technology/amazon-finalists-headquarters.html",
        "https://www.nytimes.com/2018/01/18/arts/music/philippe-jaroussky-diversity.html",
        "https://www.nytimes.com/2018/01/19/us/politics/right-left-react-government-shutdown.html",
        "https://www.nytimes.com/2018/01/18/style/high-maintenance-hbo-ben-sinclair-weed.html",
        "https://www.nytimes.com/2018/01/18/movies/three-billboards-outside-ebbing-missouri.html",
        "https://www.nytimes.com/2018/01/18/nyregion/driving-manhattan-congestion-traffic.html",
        "https://www.nytimes.com/2018/01/18/sports/football/vikings-eagles.html",
        "https://www.nytimes.com/2018/01/17/theater/jerry-springer-the-opera-new-group-john-rando-terrence-mann.html",
        "https://www.nytimes.com/2018/01/18/science/musk-oxen-climate-change.html",
        "https://www.nytimes.com/2018/01/18/obituaries/stansfield-turner-dead.html",
        "https://www.nytimes.com/2018/01/16/arts/television/the-assassination-of-gianni-versace-review.html",
        "https://www.nytimes.com/2018/01/18/health/drug-prices-hospitals.html",
        "https://www.nytimes.com/interactive/2018/01/18/travel/what-to-do-36-hours-in-washington-dc.html",
        "https://www.nytimes.com/2018/01/12/us/politics/black-colleges-borrower-defense-devos.html",
        "https://www.nytimes.com/interactive/2018/01/16/dining/canadian-food.html",
        "https://www.nytimes.com/2018/01/18/magazine/fear-of-the-federal-government-in-the-ranchlands-of-oregon.html",
        "https://www.nytimes.com/2018/01/18/realestate/living-way-off-campus-in-williamsburg-brooklyn.html",
        "https://www.nytimes.com/2018/01/18/upshot/the-us-fertility-rate-is-down-yet-more-women-are-mothers.html",
        "https://www.nytimes.com/2018/01/18/insider/i-figure-skating-reporter-full-circle-with-tonya-harding.html",
        "https://www.nytimes.com/2018/01/16/business/gm-nafta.html",
        "https://www.nytimes.com/2018/01/16/t-magazine/food/angela-dimayuga-breakfast-recipes.html",
        "https://www.nytimes.com/2016/09/27/well/activity-trackers-may-undermine-weight-loss-efforts.html",
        "https://well.blogs.nytimes.com/2012/04/04/meet-the-active-couch-potato/",
        "https://well.blogs.nytimes.com/2011/01/12/the-hazards-of-the-couch/",
        "https://www.nytimes.com/2018/01/10/well/move/facial-exercises-may-make-you-look-3-years-younger.html",
        "https://www.nytimes.com/2018/01/03/well/move/exercise-microbiome-health-weight-gut-bacteria.html",
        "https://www.nytimes.com/2017/12/27/well/move/the-year-in-fitness-exercise-add-intensity-live-to-see-another-year.html",
        "https://www.nytimes.com/2017/12/20/well/move/why-sitting-may-be-bad-for-your-heart.html",
        "https://www.nytimes.com/2017/12/06/well/move/how-exercise-can-make-for-healthier-fat.html",
        "https://www.nytimes.com/2018/01/18/your-money/bitcoin-irs-taxes.html",
        "https://www.nytimes.com/2018/01/18/books/review/10-new-books-we-recommend-this-week.html",
        "https://www.nytimes.com/2018/01/18/smarter-living/super-bowl-party-host.html",
        "https://www.nytimes.com/2018/01/17/business/investing-in-2018.html",
        "https://www.nytimes.com/2018/01/16/smarter-living/bridesmaid-how-to.html",
        "https://www.nytimes.com/2017/05/12/world/americas/dinosaur-fossil-nodosaur-alberta-oil-sands.html",
        "https://www.nytimes.com/2016/06/04/arts/international/dinosaurs-star-power-has-yet-to-translate-at-auction.html",
        "https://www.nytimes.com/2018/01/18/science/earthquakes-moon-cycles.html",
        "https://www.nytimes.com/2018/01/17/science/saiga-deaths-bacteria.html",
        "https://www.nytimes.com/2018/01/17/science/marmots-antisocial-lifespan.html",
        "https://www.nytimes.com/2018/01/13/science/dead-squid.html",
        "https://www.nytimes.com/2018/01/12/science/mars-plants-soil.html",
        "https://www.nytimes.com/2018/01/16/opinion/the-truth-behind-a-bright-shining-lie.html",
        "https://www.nytimes.com/2018/01/16/opinion/the-largest-military-construction-project-in-history.html",
        "https://www.nytimes.com/2018/01/12/opinion/when-american-soldiers-met-vietnamese-cuisine.html",
        "https://www.nytimes.com/2018/01/11/opinion/three-journeys-to-khe-sanh.html",
        "https://www.nytimes.com/2018/01/09/opinion/coffee-cafes-vietnam-war.html",
        "https://www.nytimes.com/2017/02/06/dining/craft-breweries-lines-ale.html",
        "https://www.nytimes.com/2018/01/05/dining/drinks/beer-review-american-brown-ales.html",
        "https://www.nytimes.com/2017/12/29/world/asia/south-korea-ship-seized.html",
        "https://www.nytimes.com/2017/12/22/world/asia/north-korea-security-council-nuclear-missile-sanctions.html",
        "https://www.nytimes.com/2017/11/08/world/asia/trump-china-xi-jinping-north-korea.html",
        "https://www.nytimes.com/2018/01/03/us/politics/trump-north-korea-wedge-south-korea.html",
        "https://www.nytimes.com/2017/12/16/business/economy/tax-bill-housing.html",
        "https://www.nytimes.com/2017/12/12/us/quakes-wildfires-california-cost-of-living.html",
        "https://www.nytimes.com/2017/12/01/business/economy/single-family-home.html",
        "https://www.nytimes.com/2017/11/10/business/economy/california-republican-tax-bills.html",
        "https://www.nytimes.com/2018/01/18/opinion/krugman-childrens-health-insurance-program.html",
        "https://www.nytimes.com/2018/01/18/us/politics/government-shutdown-house-vote.html",
        "https://www.nytimes.com/2017/10/26/business/amazon-headquarters-competition.html",
        "https://www.nytimes.com/interactive/2017/09/09/upshot/where-should-amazon-new-headquarters-be.html",
        "https://www.nytimes.com/2017/10/23/technology/amazon-headquarters.html",
        "https://www.nytimes.com/2017/10/18/nyregion/in-amazon-bid-new-york-brags-about-well-everything.html",
        "https://www.nytimes.com/2017/09/07/technology/amazon-headquarters-north-america.html",
        "https://www.nytimes.com/2018/01/16/insider/what-were-reading.html",
        "https://www.nytimes.com/2018/01/16/us/politics/right-and-left-react-to-president-trumps-comments-on-immigration.html",
        "https://www.nytimes.com/2018/01/12/insider/what-were-reading.html",
        "https://www.nytimes.com/2018/01/11/us/politics/right-left-react-nsa-spying-warantless-surveillance.html",
        "https://www.nytimes.com/2018/01/09/insider/what-were-reading.html",
        "https://www.nytimes.com/2016/09/11/arts/television/call-it-a-growing-family-high-maintenance-moves-to-hbo.html",
        "https://www.nytimes.com/2016/09/16/arts/television/review-high-maintenance-hbo.html",
        "https://www.nytimes.com/2017/11/08/movies/review-three-billboards-outside-ebbing-missouri-martin-mcdonagh.html",
        "https://www.nytimes.com/2017/12/26/nyregion/uber-car-congestion-pricing-nyc.html",
        "https://www.nytimes.com/2017/12/29/nyregion/new-york-congestion-pricing-new-support-steadfast-critics.html",
        "https://www.nytimes.com/2018/01/16/nyregion/cuomos-congestion-pricing-for-new-york-city-begins-to-take-shape.html",
        "https://www.nytimes.com/2017/11/28/nyregion/congestion-pricing-new-york.html",
        "https://www.nytimes.com/2018/01/17/sports/afc-championship-prediction.html",
        "https://www.nytimes.com/2018/01/17/sports/nfc-championship-prediction.html",
        "https://www.nytimes.com/2018/01/04/sports/football/nfl-speed-leonard-fournette.html",
        "https://www.nytimes.com/2018/01/15/sports/vikings-saints-stefon-diggs-marcus-williams.html",
        "https://www.nytimes.com/2008/01/30/theater/30cnd-springer.html",
        "https://www.nytimes.com/2013/09/19/arts/music/a-bittersweet-opening-for-anna-nicole-and-city-opera.html",
        "https://www.nytimes.com/2009/07/18/theater/18springer.html",
        "https://www.nytimes.com/2018/01/11/science/climate-change-lakes-streams.html"]


async def async_test():
    start_time = time.time()
    # for url in urls:
    #     await fetch(url)
    #     print(url)
    async with aiohttp.ClientSession() as client:
        # for url in urls:
        #     html = await fetch(client, url)
        #     print("hi{}", url)
        results = await asyncio.wait([asyncio.ensure_future(fetch(url)) for url in urls])
        print(results)
    print("async: {}", time.time() - start_time)


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            await resp.text()
            print(url)
            return


def sync_test():
    start_time = time.time()
    for url in urls:
        requests.get(url)
    print("sync:  {}", time.time() - start_time)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_test())
    loop.close()

    sync_test()
