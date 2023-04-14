<h1 align="center" style="color:white;">ToDo-FastAPI</h1>

<div align="center">
  
  [![Status](https://img.shields.io/badge/status-progress-orange?)]()
  
</div>


In this repository you will find all the necesary recourse to test and run this projet by yourself
<br>
This project use Python 3.9


## 📝 Content

- [Why?](#about)
- [How to clone it and run it](#getting_started)
- [Build with](#built_using)
- [Author](#authors)

## 🧐 Why? <a name = "about"></a>

This is just a super tiny project to try to get more knowledge about FastAPI, and because is for a school project, so, yeah super funny

Since it's not finished, there are some useless code commented.

## 🏁 How to clone it and run it <a name = "getting_started"></a>

 Clone the repository where you are gonna work
    
```bash
 git clone https://github.com/Jorgeablade/ToDo-FastAPI.git
```

Create or activate the venv. In case you wanna create a new venv, just delete the one you cloned and create a new one.
But if you are keeping this one, run:
    
```bash
 ./.venv/Scripts/Activate.ps1 # If you are in Windows
 source ./.venv/Scripts/activate # If Linux distribution
```

Create a random key using random_key.py. This will create a .env with SECRET=blablablablablabla :)

```bash
 ./random_key.py
``` 
    
 And run the project
    
```bash
 uvicorn app:app --reload 
```  

## ⛏️ Build with <a name = "built_using"></a>

- [FastAPI](https://fastapi.tiangolo.com/az/)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [Pydantic](https://docs.pydantic.dev/)

## ✍️ Author <a name = "authors"></a>

- [@Thepicolo](https://github.com/Jorgeablade) - Student / Trying to be a Developer
