Chart Generator API
============

Chart Generator is a simple tool for generating charts from data. It returns a URL to the generated image of the chart.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Chart Generator API](https://apiverve.com/marketplace/api/chartgenerator)

---

## Installation
	pip install apiverve-chartgenerator

---

## Configuration

Before using the chartgenerator API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Chart Generator API documentation is found here: [https://docs.apiverve.com/api/chartgenerator](https://docs.apiverve.com/api/chartgenerator).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_chartgenerator.apiClient import ChartgeneratorAPIClient

# Initialize the client with your APIVerve API key
api = ChartgeneratorAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = {  "type": "bar",  "data": {   "labels": [ "Q1", "Q2", "Q3", "Q4" ],   "datasets": [    {     "label": "Users",     "data": [ 50, 60, 70, 180 ]    },    {     "label": "Revenue",     "data": [ 100, 200, 300, 400 ]    }   ]  } } 
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
    "id": "15e899a6-5eec-40ca-a617-4480f5a801c8",
    "format": ".png",
    "expires": 1740173365411,
    "type": "bar",
    "downloadURL": "https://storage.googleapis.com/apiverve.appspot.com/chartgenerator/15e899a6-5eec-40ca-a617-4480f5a801c8.png?GoogleAccessId=635500398038-compute%40developer.gserviceaccount.com&Expires=1740173365&Signature=BlQo5Pp0YfG9MmKGKHtvbULtYPA5jenQ14ZYrKzqZRKGVz9yiiEsVaRq0XsVFj2fM5pSZ8NRcT%2FZj%2FtIHTFid6jxjp6PPdZmO%2Fu9uNKjS5b204U0xQxtg%2F9t6TIzk%2BzthmV0JZl8xeZph6B4htBUrZWv7gVW0RDbnHnQPfXcoqKW8CMRmN%2F9crjQNtCqpvdPMS4VMYbCoqDFpLj2SaRqitYhzK9oyA6GNQ9ZyQoM0wGJrXnyYLGq5uq00xWs9hql%2FSzehgAKJj%2BrtE%2F0%2FGfBB3zFbgzolggYQKxrj6I%2FusvO%2F3Ng5UO84Bbz%2BIqQcZr7BAUW1mF49096fYhplEOayg%3D%3D"
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