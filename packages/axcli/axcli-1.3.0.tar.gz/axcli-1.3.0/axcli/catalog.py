import click, httpx, asyncio, json, queue
from colorama import Fore, Style
import axinite.tools as axtools

CATALOG = "https://raw.githubusercontent.com/jewels86/Axinite/refs/heads/main/templates/catalog.txt"
PAGE_LEN = 10

@click.command("catalog")
@click.option("-u", "--url", type=str, help="The URL of the catalog file.", default=CATALOG)
def catalog(url):
    "Shows a catalog where you can download templates."
    print(f"Welcome to the {Fore.RED}Axinite Template Catalog{Style.RESET_ALL}!")
    systems = []
    system_queue = queue.Queue()

    def download(x):
        return httpx.get(x).text
    def link(x):
        if not x.startswith("http") or not x.startswith("https"):
            return f"{url.rsplit('/', 1)[0]}/{x}"
        return x

    try:
        print("\033[KDownloading catalog...", end="\r")
        catalog = download(url)
        print("\033[KParsing catalog...", end="\r")
        for line in catalog.splitlines():
            line = link(line)
            system_queue.put(line)
        print("\033[KFinished!", end="\r")
    except httpx.HTTPError:
        print(f"{Fore.RED}Error{Style.RESET_ALL}: Could not download catalog {url}.")
        return
    
    async def fetch_systems():
        while not system_queue.empty():
            system_url = system_queue.get()
            try:
                response = await asyncio.to_thread(download, system_url)
                system = json.loads(response)
                systems.append(system)
                
            except httpx.HTTPError:
                pass

    async def main():
        fetch_task = asyncio.create_task(fetch_systems())
        while not system_queue.empty():
            print(f"\033[KWaiting for systems to download ({len(systems)})...", end="\r")
            await asyncio.sleep(0.2)
        await fetch_task

    asyncio.run(main())

    print(f"\033[KDownloaded {len(systems)} systems.")
    
    def print_page(n):
        start = n * PAGE_LEN
        end = min(start + PAGE_LEN, len(systems))
        i = 0
        for system in systems[start:end]: 
            print(f"{Fore.RED}{i}{Style.RESET_ALL}: {system['name']}")
            i += 1
    def main_prompt(n):
        start = n * PAGE_LEN
        end = min(start + PAGE_LEN, len(systems))
        n_pages = len(systems) // PAGE_LEN
        print_page(n)
        print(f"[s{start}-s{end -1}] Select systems to download (comma-separated), [p0-p{n_pages}] Select a page to print, or 'q' to quit.")
        return click.prompt(">", type=str)

    def print_system(n):
        print(f"{Fore.RED}System{Style.RESET_ALL}: {systems[n]['name']}")
        print(f"{Fore.RED}Description{Style.RESET_ALL}: {systems[n]['description']}")
        print(f"{Fore.RED}Author{Style.RESET_ALL}: {systems[n]['author']}")
        print(f"{Fore.RED}License{Style.RESET_ALL}: {systems[n]['license']}")
        print("Download? [y/n]")
        return click.prompt(">>", type=str)

    input = main_prompt(0)
    page = 0
    while input != "q":
        if input.startswith("s"):
            system_indices = input[1:].replace(" ", "").split(',')
            valid_indices = []
            for i in system_indices:
                if i.isdigit():
                    valid_indices.append(int(i))
                elif i.startswith('s') and i[1:].isdigit():
                    valid_indices.append(int(i[1:]))
            valid_indices = [i for i in valid_indices if 0 <= i < len(systems)]
            if valid_indices:
                for system in valid_indices:
                    input = print_system(system)
                    if input == "y":
                        template = download(link(systems[system]["path"]))
                        filename = systems[system]["path"].rsplit('/', 1)[-1]
                        with open(filename, "w") as f:
                            f.write(template)
                        print(f"{Fore.GREEN}System {systems[system]['name']} downloaded!{Style.RESET_ALL}")
                    else:
                        print("Canceled.")
                input = main_prompt(page)
            else:
                print(f"{Fore.RED}Error{Style.RESET_ALL}: Invalid system number(s).")
                input = main_prompt(page)
        elif input.startswith("p"):
            _page = int(input[1:])
            if _page >= 0 and _page < len(systems) // PAGE_LEN:
                page = _page
                input = main_prompt(page)
            else:
                print(f"{Fore.RED}Error{Style.RESET_ALL}: Invalid page number.")
                input = main_prompt(page)
        else:
            print(f"{Fore.RED}Error{Style.RESET_ALL}: Invalid input.")
            input = main_prompt(page)