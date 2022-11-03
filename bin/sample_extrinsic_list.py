from subscrape.db.subscrape_db import SubscrapeDB
import logging
import subscrape
import asyncio

async def main():
    
    extrinsic_idx = "14238250-2"
    
    config = {
        "kusama":{
            "_api": "SubscanV2",
            "extrinsics-list":[
                extrinsic_idx
            ],
        }
    }

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("wiping storage")
    subscrape.wipe_cache()
    logging.info("scraping")
    await subscrape.scrape(config)
    logging.info("transforming")

    db = SubscrapeDB.sqliteInstanceForPath("sqlite:///data/cache/sample_extrinsic_list.db")
    data = db.read_extrinsic(extrinsic_idx)

    assert data["extrinsic_hash"] == '0x408aacc9a42189836d615944a694f4f7e671a89f1a30bf0977a356cf3f6c301c'
    assert type(data["params"]) is list
    assert type(data["event"]) is list
    logging.info("done")
    

asyncio.run(main())