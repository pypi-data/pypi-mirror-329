![Version](https://img.shields.io/badge/version-1.0.5-blue)
![Static Badge](https://img.shields.io/badge/build-deployed-red)
![Static Badge](https://img.shields.io/badge/license-MIT-gren)
![Static Badge](https://img.shields.io/badge/created_at-january_2025-yellow)
![Static Badge](https://img.shields.io/badge/top_language-python-purple)
![Framework](https://img.shields.io/badge/framework-Pure_Python-darkorange)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="">
    <img src="https://github.com/user-attachments/assets/471ff04f-fae9-4be2-9945-0cebaac937a3" alt="Logo" width="400">
  </a>

  <h3 align="center">HTTPPOOL</h3>
 
   <p align="center">
    Get and storing the HTML data of a website using a cache system
    <br />
    <br />
    <a href="https://github.com/alexdevzz/httppool_pip_installer"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/alexdevzz/httppool_pip_installer/issues">Report Bug</a>
    ·
    <a href="https://github.com/alexdevzz/httppool_pip_installer/issues">Request Feature</a>
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

This library is developed using pure Python code, and is responsible for storing locally, through a cache system using a Producer-Consumer algorithm, the HTML information obtained from any web page. It includes a daemon process that is responsible for automatically updating the cache through a set time, independent for each URL and also includes a tracing system using a logger to monitor the status of the service.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
You need to make sure you have installed the following modules.
```s
pip install requests
```
If you do not have the library shown above installed, the httppool package will add it for you during its installation.

### Installation
```python
pip install Httppool
```

<!-- USAGE EXAMPLES -->
## Usage

### Example 1 
It will show you and store all the information of the web's HTML
```python
import Httppool as htp

url = 'https://www.prensa-latina.cu/deportes/'
content = htp.get_url_content(url)

print(content)
```

### Example 2 
If you use it in conjunction with a Web Scraping library like BeautifulSoup you can get the data you are interested in
```python
import Httppool as htp
from bs4 import BeautifulSoup

url = 'https://www.entumovil.cu/'

content = htp.get_url_content(url)
soup = BeautifulSoup(content, 'html.parser')
response = soup.find('div', id='etm-desription')

print(response.prettify())

# the content of response is:

# <div id="etm-desription">
#     <p>
#         Somos un equipo de desarrollo de servicios y aplicaciones para móviles
#         pertenecientes a la empresa Desoft. Desde sus
#         inicios trabajamos orientados a la satisfacción de las necesidades que
#         soliciten las empresas de informatizar sus procesos, así como brindar a
#         la población la posibilidad de obtener información de su interés a
#         través de consultas, suscripciones, notificaciones y compras on line  mediante mensajería de texto (SMS)…
#         <br/>
#     </p>
#     <p>
#         <br/>
#     </p>
# </div>
```

### Example 3
You can run the daemon process for automatic cache update
```python
from Httppool.deamon import HttppoolDeamon

deamon = HttppoolDeamon()
deamon.start()

# It will update the information of each URL 
# that is in the cache folder (httppool-cache) 
# every 15 min by default. This parameter can be changed
```

## Cache Structure
When using the library for the first time, 3 files are created for each URL in the httppool-cache folder and httppool-logger.log file. The following structure is created in the root directory of the current project:
```python
My_python_project
├── httppool-cache
│   ├── f47eda8cfe42cc7aa478686b321f22c6.lastaccess
│   ├── f47eda8cfe42cc7aa478686b321f22c6.url
│   └── f47eda8cfe42cc7aa478686b321f22c6.webpagedata
├── httppool-logger.log
├── my_python_script.py
```

### .lastaccess
The file `f47eda8cfe42cc7aa478686b321f22c6.lastaccess` shows the following information:
``` python
read: 2025-01-06 11:05:04   # last date of reading

write: 2025-01-06 11:05:04  # last date of writing

retry: 15  # time interval taken to update the cache
```

### .url
The file `f47eda8cfe42cc7aa478686b321f22c6.url` shows the following information:
``` python
# web page URL
https://www.entumovil.cu/  

# headers to be sent using the requests library
headers: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
```

### .webpagedata
The file `f47eda8cfe42cc7aa478686b321f22c6.webpagedata` shows the following information:
``` html
<!-- web page HTML information for future Scraping -->
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    
    <body>
        <div class="item " data-ref="empresariales">
            <a class="service-link" href="/web/servicios/empresariales/#service_item43s">
                <div class="service-button-label">
                    <p>Micropagos</p>
                </div>
                <div class="service-button" style="background-image:url(/media/iconMICROPAGO.png) ">
                </div>
            </a>
        </div>
    </body>
</html>
```

### httppool-logger.log
The library has a logger to track the traces of the cache system based on the producer-consumer algorithm:
```python
2025-01-06 11:05:02,571 : INFO : HTTPPOOL : Client : Consumming URL --> https://www.entumovil.cu/ 

2025-01-06 11:05:02,572 : DEBUG : HTTPPOOL : Starting new HTTPS connection (1): www.entumovil.cu:443 

2025-01-06 11:05:03,610 : DEBUG : HTTPPOOL : https://www.entumovil.cu:443 "GET / HTTP/1.1" 200 None 

2025-01-06 11:05:04,055 : INFO : HTTPPOOL : Producer : Got URL content --> https://www.entumovil.cu/ 
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Email: alexdev.workenv@gmail.com
