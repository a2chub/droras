import uvicorn
from pprint import pprint

from .convert_heatlist import download_heat_list


def main():
    heat_list = download_heat_list()
    pprint(heat_list, indent=4)

    uvicorn.run("droras.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
