# Secret 2FA

Secret 2FA is a Python library designed to automate **secret 2fa authentication (2FA)** for Facebook using **Pyppeteer
**. This tool helps retrieve 2FA codes automatically.

## 🚀 Features

- Automates the process of entering and retrieving Facebook 2FA codes.
- Uses **Pyppeteer** to interact with Facebook's authentication page.
- Designed for **high accuracy** and **speed**.

## 🔧 Installation

Install via pip:

```bash
#pip install secret_2fa


import secret_2fa

secret = secret_2fa.authen()
secret.set_code("KONLS2C33L2DHJYDGPBDZ3S7ENLVH7DK")
code_1 = secret.get_code()

secret.set_code("SIKDMCCV6VTN6ECL7TEHKEXG5LHNFWC4")
code_2 = secret.get_code()

secret.set_code("S6DK6M4WL2K6B3W27VSNXRKKOKBF2DA3")
code_3 = secret.get_code()

secret.close()

print(code_1, code_2, code_3)
#167662 232484 422762

