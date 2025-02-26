## 

<p align="center">
  <img src="https://uploads-ssl.webflow.com/6151887923ecfa4ac66a9e69/65168cccea1c9f0fcb33652c_logo-adaptive.svg" alt="Autoenhance.ai logo" align="center">
</p>

<h1 align="center">Autoenhance.ai Python SDK</h1>

<p align="center">The AI photo editor that enhances your workflow now available with easy and quick Python SDK</p>

## 👋 Navigation

* [Description](#description)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [Examples](#examples)

## <a id="description"></a>✨ Description

Our SDK will help you easily integrate Autoenhance.ai into your codebase in a matter of minutes. We've prepared methods for interacting with our API in all possible ways you might need.


## <a id="requirements"></a>⚠️ Requirements

* **Basic Python knowledge and a project set up**
* **Autoenhance.ai API key**
Don't have an API key ? Sign up in our [Webapp](https://www.app.autoenhance.ai/login), and you will find it on the [API page](https://app.autoenhance.ai/application-interface)!


## <a id="installation"></a>🔧 Installation

Install Autoenhance.ai SDK with a simple CLI command

With `pip`:
```bash
pip install autoenhance
```
With `poetry`:
```bash
poetry add autoenhance
```

## <a id="configuration"></a>⚙️ Configuration

Follow these simple steps in order to implement and configure our SDK

Import Autoenhance SDK package:
```bash
import autoenhance
```
Create a constant, and add your [API key](#requirements)
```bash
autoenhance = autoenhance.Autoenhance('YOUR API KEY');
```

Boom, that's it! Now you can interact with our API in a matter of seconds.

## <a id="examples"></a>💎 Examples

`Uploading image`
```bash

  import requests

  def upload_image(image_properties: dict, image_buffer):

    response = autoenhance.create_image(**image_properties)
    requests.put(
      response.s3_put_object_url,
      headers={
        "Content-Type": "image/jpeg",
      },
      body=image_buffer
    )
```

`Retrieving order`
```bash
  def get_order(order_id):
    order = autoenhance.retrieve_order(orderId)
```

`Retrieving list of orders`
```bash
  def get_orders():
    response = autoenhance.list_orders()
    orders = response.orders
```

`Downloading enhanced image`
```bash
  def download_image(image_id):
    image_url = autoenhance.download_enhanced_image(image_url, size="large")
    return image_url.url
```