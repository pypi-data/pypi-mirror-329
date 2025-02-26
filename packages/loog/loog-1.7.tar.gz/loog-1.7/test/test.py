from test_function import test_function

from loog import log


def main():
    log("DEBUG test", "debug")
    log("INFO test")
    log("WARNING test", "warning")
    log("ERROR test", "error")
    log("CRITICAL test", "critical")

    log.log_off()
    log("log offed", "warning")

    log.log_on()
    log("log oned", "warning")

    test_function()


if __name__ == "__main__":
    log.set_display_level("debug")
    log.set_display_location(False)
    log.set_loglevel_color("debug", "blue")
    log.log_to_file()

    log.create_custom_loglevel("info")
    log.create_custom_loglevel("test", "green")
    log.set_loglevel_color("test", "green")
    log("TEST", "test")
    log("abcdefghijklmnopqrstuvwxyz" * 20, "test")
    # log.set_display_level("test")

    # main()

    log("color test", color="red")
    log("color test", "warning", color="green")
    log("color test", color="xkcd:red")
    log("color test", color="#123456")

