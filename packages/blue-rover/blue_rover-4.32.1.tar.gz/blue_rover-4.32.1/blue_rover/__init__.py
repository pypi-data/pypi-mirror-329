NAME = "blue_rover"

ICON = "🐬"

DESCRIPTION = f"{ICON} AI x ROS."

VERSION = "4.32.1"

REPO_NAME = "blue-rover"

MARQUEE = (
    "https://github.com/waveshareteam/ugv_rpi/raw/main/media/UGV-Rover-details-23.jpg"
)

ALIAS = "@rover"


def fullname() -> str:
    return f"{NAME}-{VERSION}"
