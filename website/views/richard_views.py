from typing import Any, Dict
from flask import Blueprint, request, render_template
from random import randint, sample

richard_views = Blueprint("richard_views", __name__)
# https://www.solarnisady.cz/firmy/reference/page/1
projects = [
    {
        "location": "FVE Uničov",
        "power": "126",
        "year": "2008",
    },
    {
        "location": "FVE Kroměříž",
        "power": "52,8",
        "year": "2009",
    },
    {
        "location": "FVE Kondrac",
        "power": "1108,8",
        "year": "2009",
    },
    {
        "location": "FVE Lužice",
        "power": "975",
        "year": "2009",
    },
    {
        "location": "FVE Malešovice",
        "power": "3630",
        "year": "2009",
    },
    {
        "location": "FVE Břest II",
        "power": "1400",
        "year": "2009",
    },
]


@richard_views.route("/get_sunturtle", methods=["GET"])
def get_sunturtle():
    if request.method == "GET":
        return render_template("richard_test.html")


@richard_views.route("/get_sunturtle_data", methods=["GET"])
def get_sunturtle_data() -> Dict[str, Any]:
    """API Endpoint for doing the calculations."""
    if request.method == "GET":
        # Receive input data for the calculation
        input_data = {
            "address": request.args["address"],
            "area": request.args["area"],
        }
        print(input_data)
        # Send response with random data (for now)
        return {
            "total_price": 5000 * randint(10, 100),
            "work_days": randint(2, 15),
            "return_years": randint(1, 10),
            "service_life": 10 + randint(0, 10),
            "location_rating": ["ideální", "průměrná", "špatná"][randint(0, 2)],
            "projects": sample(projects, 2),
        }
    return {"message": "Use GET request!"}
