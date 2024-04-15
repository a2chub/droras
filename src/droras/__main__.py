import uvicorn


def main():
    uvicorn.run("droras.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
