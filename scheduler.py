from rocketry import Rocketry
app = Rocketry(execution="async")


@app.task('every 5 seconds')
async def do_things():
    ...

if __name__ == "__main__":
    app.run()