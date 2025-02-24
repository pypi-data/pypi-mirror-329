# Country Info Package

Ce package fournit des informations sur les pays, y compris :
- Le nom du pays
- Le code ISO
- L'indicatif téléphonique
- Le drapeau

## Installation

Pour installer le package, utilisez :

```bash
pip install py-country-info-all
```

## Importation

Pour impoter le package, utilisez :

```bash
from py_country_info_all import py_country_info_all

country = py_country_info_all.get_country_info("Burkina Faso")
print(country)
```
Resultat :

{'name': 'Burkina Faso', 'code': '226', 'iso': 'BF / BFA', 'flag': '🇧🇫'}

## Pour afficher tous les pays , utiliser :

```bash
countries = py_country_info_all.get_all_countries()
```


## Illustration 

![Description de l'image](assets/image.png)
