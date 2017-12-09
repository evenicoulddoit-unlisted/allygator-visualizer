# Allygator Shuttle Visualizer
[**Door2Door Full-Stack Submission**](https://github.com/door2door-io/fullstack-code-challenge)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Summary
* Use the Heroku one-click deploy button to create the build, then run the test suite against it
* I focussed far more efforts on the backend/modelling/API-design side
* The front-end is very lightweight, lacks some tests, and doesn't provide clustering of markers as is in the spec
  * Hopefully however, it should demonstrate adequately my knowledge of both JS and CSS
* In terms of technologies, I've used Python 3, GeoDjango and Django Rest Framework on the back-end, and Angular on the front-end
  * Many alternatives would have been perfectly suitable
  * I chose these both because I know them well, and I know they are perfectly capable of creating testable and reliable APIs with geo-support
  * Given the fairly basic setup of the front-end, I need not have used a library. However, it does provide a clear structure on which to build, and ends up weighing only ~2kb, so seems perfectly reasonable
* The Angular project can be found within the `ng` directory, and the Django project within `visualizer`
  * A symlink within the Django static directory exposes the front-end

## Modelling
* I thought at some length as to how to best model the data
* In the end I opted for two models: `Vehicle` and `VehicleLocation`
  * `VehicleLocation` is a recording of every *valid* vehicle location emission
  * `Vehicle` is a representation of each individual vehicle
* Both the current location and the bearing of the vehicle are stored on the
  `Vehicle` model, instead of being calculated from the foreign key to
  `VehicleLocation`.
  * The bearing is calculated from an existing `current_location` value, which
    prevents an additional read each time an emission is made
  * I also chose *not* to index the foreign key from `VehicleLocation` to
    `Vehicle` as this would also have required an extra write per emission.
    This seemed a reasonable compromise given that the data is only really needed
    for the data science team
* Because this is a write-heavy system, at scale it might be worth/necessary to consider
  implementing:
  * Some sort of queueing system
  * Load balancing
  * Database sharding
* A Berlin spacial-reference is used to construct a 3.5km polygon defining the
  "city boundaries", and is used to validate incoming requests

## Testing / Code-Quality
* Only the back-end was tested, due to time constraints
* I used TDD to design the private API, and there should be a good level of
  coverage at both the unit and integration level
  * *Many of the tests strictly interact with the DB and so are not **pure** unit tests*
  * *I could have written more integration (view) tests to cover the edge-cases*
* The private API is also type-annotated and run against [MyPy](http://mypy-lang.org/)
* [`pycodestyle`](https://pycodestyle.readthedocs.io/) was used to enforce PEP8
* I've followed [PEP257's docstring conventions](https://www.python.org/dev/peps/pep-0257/) and with
  any luck the code should be readable and well structured
* The front-end uses [TSLint](https://palantir.github.io/tslint/)

## What is not covered
* I ran out of time implementing the front-end. I implemented the map-markers in a fairly trivial way, and it seemed as though the refactor to use a marker-clusterer would have been a fair amount of work
* The front-end has no tests and lacks robust error handling

## Future Considerations
* More research should be conducted to find web server technologies better places to handle many hundreds/thousands of concurrent requests
* API authentication/throttling/validation

## Development
* Ensure you have Python and NVM
* Install Python requirements
  * `pip install -r requirements.txt`
* Install Node requirements
  * `nvm use; npm install`
* To develop the back-end:
  * Use `python manage.py runserver` to spin up a development server
* To develop the front-end:
  * Change to the `ng` directory
  * Run `npm start` to launch a live-reloading Angular development server
  * Assumes the API can be found at `dev.local:8000`
