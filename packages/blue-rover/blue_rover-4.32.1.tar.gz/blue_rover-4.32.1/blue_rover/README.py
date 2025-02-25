import os

from blue_objects import file, README

from blue_rover import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "blue-rover",
            "marquee": "https://github.com/waveshareteam/ugv_rpi/raw/main/media/UGV-Rover-details-23.jpg",
            "description": "based on [UGV Beast PI ROS2](https://www.waveshare.com/wiki/UGV_Beast_PI_ROS2).",
            "url": "./blue_rover/docs",
        }
    ]
)


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
        )
        for readme in [
            {
                "items": items,
                "path": "..",
            },
            {
                "path": "docs",
            },
        ]
    )
