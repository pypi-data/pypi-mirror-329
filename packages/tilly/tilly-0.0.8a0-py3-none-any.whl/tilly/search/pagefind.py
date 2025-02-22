import asyncio

from pagefind.index import PagefindIndex, IndexConfig



async def index_site(site=None, output_path=None, logfile=None):
    config = IndexConfig(
        logfile=logfile,
        output_path=output_path,
        verbose=True
    )
    async with PagefindIndex(config=config) as index:
        await asyncio.gather(
            index.add_directory(site),
        )

        await index.get_files()


if __name__ == "__main__":
    asyncio.run(index_site())