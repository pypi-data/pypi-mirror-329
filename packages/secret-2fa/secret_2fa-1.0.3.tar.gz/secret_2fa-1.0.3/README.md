# Secret 2FA  

Secret 2FA is a Python library designed to automate **secret 2fa authentication (2FA)** for Facebook using **Pyppeteer**. This tool helps retrieve 2FA codes automatically.  

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
code = secret.get_code()
print(code)
#063471

