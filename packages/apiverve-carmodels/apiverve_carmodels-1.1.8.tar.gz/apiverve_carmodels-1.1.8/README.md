Car Models API
============

Car Models is a simple tool for getting information on cars. It returns information on various car models

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Car Models API](https://apiverve.com/marketplace/api/carmodels)

---

## Installation
	pip install apiverve-carmodels

---

## Configuration

Before using the carmodels API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Car Models API documentation is found here: [https://docs.apiverve.com/api/carmodels](https://docs.apiverve.com/api/carmodels).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_carmodels.apiClient import CarmodelsAPIClient

# Initialize the client with your APIVerve API key
api = CarmodelsAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "year": "2020",  "make": "Toyota",  "model": "Camry",  "trim": "LE" }
```

###### Simple Request

```
# Make a request to the API
result = api.execute(query)

# Print the result
print(result)
```

###### Example Response

```
{
  "status": "ok",
  "error": null,
  "data": {
    "count": 4,
    "filteredOn": [
      "year",
      "make",
      "model"
    ],
    "cars": [
      {
        "Make": "Acura",
        "CityMPG": "30",
        "CityELEC": "0",
        "CombMPG": "33",
        "CombELEC": "0",
        "Cyl": "4",
        "Displace": "1.5",
        "Drive": "Front-Wheel Drive",
        "Fuel": "Premium",
        "HighwELEC": "0",
        "HighwMPG": "37",
        "Trans": "Automatic (AV-S7)",
        "Size": "Large Cars",
        "Year": "2024",
        "Trim": "Integra",
        "Model": "Integra"
      },
      {
        "Make": "Acura",
        "CityMPG": "21",
        "CityELEC": "0",
        "CombMPG": "24",
        "CombELEC": "0",
        "Cyl": "4",
        "Displace": "2",
        "Drive": "Front-Wheel Drive",
        "Fuel": "Premium",
        "HighwELEC": "0",
        "HighwMPG": "28",
        "Trans": "Manual 6-spd",
        "Size": "Large Cars",
        "Year": "2024",
        "Trim": "Integra",
        "Model": "Integra"
      },
      {
        "Make": "Acura",
        "CityMPG": "26",
        "CityELEC": "0",
        "CombMPG": "30",
        "CombELEC": "0",
        "Cyl": "4",
        "Displace": "1.5",
        "Drive": "Front-Wheel Drive",
        "Fuel": "Premium",
        "HighwELEC": "0",
        "HighwMPG": "36",
        "Trans": "Manual 6-spd",
        "Size": "Large Cars",
        "Year": "2024",
        "Trim": "Integra A-Spec",
        "Model": "Integra"
      },
      {
        "Make": "Acura",
        "CityMPG": "29",
        "CityELEC": "0",
        "CombMPG": "32",
        "CombELEC": "0",
        "Cyl": "4",
        "Displace": "1.5",
        "Drive": "Front-Wheel Drive",
        "Fuel": "Premium",
        "HighwELEC": "0",
        "HighwMPG": "36",
        "Trans": "Automatic (AV-S7)",
        "Size": "Large Cars",
        "Year": "2024",
        "Trim": "Integra A-Spec",
        "Model": "Integra"
      }
    ]
  },
  "code": 200
}
```

---

## Customer Support

Need any assistance? [Get in touch with Customer Support](https://apiverve.com/contact).

---

## Updates
Stay up to date by following [@apiverveHQ](https://twitter.com/apiverveHQ) on Twitter.

---

## Legal

All usage of the APIVerve website, API, and services is subject to the [APIVerve Terms of Service](https://apiverve.com/terms) and all legal documents and agreements.

---

## License
Licensed under the The MIT License (MIT)

Copyright (&copy;) 2025 APIVerve, and EvlarSoft LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.