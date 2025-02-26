from loog import log


def test_function():
    log("DEBUG test", "debug")
    log("INFO test")
    log("WARNING test", "warning")
    log("ERROR test", "error")
    log("CRITICAL test", "critical")

    for i in range(10):
        log(f"INFO test {i}", "info")


if __name__ == "__main__":
    test_function()
