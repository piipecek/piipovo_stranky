document.getElementById("calculator").addEventListener("submit", function (e) {
    e.preventDefault();
    disableForm(true);
    showResults(false);
    removeAllProjectCards();

    // Get data from user
    const address = document.getElementById("input-address").value;
    const area = document.getElementById("input-area").value;
    const input_data = {
        address: address,
        area: area,
    };

    // Simulate server delay
    // (it looks like it's doing some work)
    setTimeout(function () {

        // CLIENT: Do some calculations
        // output = CALCULATE(input_data);

        // SERVER: Request data from server
        const address_arg = `?address=${encodeURIComponent(input_data.address)}`
        const area_arg = `&area=${encodeURIComponent(input_data.area)}`
        const url = "/api/get_sunturtle_data" + address_arg + area_arg;
        fetch(url).then(function (response) {
            return response.json();
        }).then(function (data) {
            // Finish stuff after receiving the response
            const output = data;

            // Expected output format:
            // - total_price:       int
            // - work_days:         int
            // - return_years:      int
            // - service_life:      int
            // - location_rating:   str
            // - projects:          object
            //   - location:        str
            //   - power:           str
            //   - year:            str
            console.log(output);

            // Update results
            document.getElementById("total-price").innerHTML = output.total_price;
            document.getElementById("work-days").innerHTML = output.work_days;
            document.getElementById("return-years").innerHTML = output.return_years;
            document.getElementById("service-life").innerHTML = output.service_life;
            document.getElementById("location-rating").innerHTML = output.location_rating;

            // Update projects
            output.projects.forEach(function (project) {
                addProjectCard(project.location, project.power, project.year);
            });

            // Open result window
            showResults(true);
            disableForm(false);
        });
    }, 1000);
}, true);

// For CLIENT side calculations
function CALCULATE(data) {
    const output = {
        total_price: 5000 * (10 + getRandomInt(100)),
        work_days: 2 + getRandomInt(15),
        return_years: 1 + getRandomInt(9),
        service_life: 8 + getRandomInt(9),
        location_rating: ["ideální", "průměrná", "špatná"][getRandomInt(3)],
    };
    return output;
}

// Helper function for getting 0-max random ints
function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

// Helper function to enable/disable form
function disableForm(state) {
    if (state) {
        document.getElementById("show-result-button").disabled = true;
        document.getElementById("show-projects-button").disabled = true;
        document.getElementById("main-submit-button").classList.add("disabled");
        document.getElementById("main-submit-spinner").classList.remove("absoff");
    } else {
        document.getElementById("main-submit-spinner").classList.add("absoff");
        document.getElementById("main-submit-button").classList.remove("disabled");
        document.getElementById("show-projects-button").disabled = false;
        document.getElementById("show-result-button").disabled = false;
    }
}

// Helper function to show/hide results
function showResults(state) {
    if (document.getElementById("show-result-button").classList.contains("collapsed") == state) {
        {
            const myCollapse = document.getElementById("collapseOne");
            const bsCollapse = new bootstrap.Collapse(myCollapse);
        }
    }
    if (document.getElementById("show-projects-button").classList.contains("collapsed") == state) {
        {
            const myCollapse = document.getElementById("collapseTwo");
            const bsCollapse = new bootstrap.Collapse(myCollapse);
        }
    }
}

// Helper function for creating cards
function addProjectCard(location, power, year) {
    const copy = document.getElementById("temp-card").cloneNode(true);
    copy.classList.remove("absoff");
    copy.id = "";
    copy.querySelector('[data-var="location"]').innerHTML = location;
    copy.querySelector('[data-var="power"]').innerHTML = power;
    copy.querySelector('[data-var="year"]').innerHTML = year;
    document.getElementById("card-container").append(copy);
}

// Helper function for deleting all cards
function removeAllProjectCards() {
    document.getElementById("card-container").innerHTML = "";
}