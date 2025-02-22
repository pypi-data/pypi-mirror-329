BMI Calculator API
============

BMI Calculator is a simple tool for calculating body mass index. It returns the calculated BMI based on the weight and height provided.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [BMI Calculator API](https://apiverve.com/marketplace/api/bmicalculator)

---

## Installation
	pip install apiverve-bmicalculator

---

## Configuration

Before using the bmicalculator API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The BMI Calculator API documentation is found here: [https://docs.apiverve.com/api/bmicalculator](https://docs.apiverve.com/api/bmicalculator).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_bmicalculator.apiClient import BmicalculatorAPIClient

# Initialize the client with your APIVerve API key
api = BmicalculatorAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "weight": 70,  "height": 170,  "unit": "metric" }
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
    "height": "170 cm",
    "weight": "70 kg",
    "bmi": 24.221453287197235,
    "risk": "Low risk",
    "summary": "This weight is normal and you are healthy.",
    "recommendation": "A BMI between 18.5 and 24.9 falls within the 'normal' weight range according to the World Health Organization. This range is associated with the lowest health risk for conditions such as heart disease, diabetes, and certain cancers. However, it's important to note that BMI is not a perfect measure as it does not account for muscle mass, bone density, overall body composition, and racial and sex differences. Therefore, while it's a useful starting point, it should not be the only measure of one's health."
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