import uvicorn


def main():
    """This def running uvicorn for myapp"""

    uvicorn.run("myapp.app:app", host="0.0.0.0", port=8000, debug=True, reload=True)


if __name__ == "__main__":
    main()
