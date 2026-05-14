# Dataset BreaKHis

## 📊 Source

Le dataset **BreaKHis** (Breast Cancer Histopathological Database) est disponible sur Kaggle :

🔗 **[BreaKHis Dataset on Kaggle](https://www.kaggle.com/datasets/ambarish/breakhis)**

## 📖 Description

Le dataset BreaKHis contient **7 909 images** histopathologiques de biopsies mammaires provenant de **82 patientes**.

### Caractéristiques :

- **Format** : Images PNG couleur (RGB)
- **Classes** : 8 types de tumeurs (4 bénignes + 4 malignes)
- **Grossissements** : 40X, 100X, 200X, 400X
- **Résolution** : Variable (environ 700×460 pixels)

### Classes de tumeurs :

#### Tumeurs bénignes :
- Adenosis
- Fibroadenoma
- Phyllodes Tumor
- Tubular Adenoma

#### Tumeurs malignes :
- Ductal Carcinoma
- Lobular Carcinoma
- Mucinous Carcinoma
- Papillary Carcinoma

## 📂 Structure du dataset

breakhis/
├── SOB/
│   ├── benign/
│   │   ├── adenosis/
│   │   │   ├── 40X/
│   │   │   ├── 100X/
│   │   │   ├── 200X/
│   │   │   └── 400X/
│   │   ├── fibroadenoma/
│   │   │   ├── 40X/
│   │   │   ├── 100X/
│   │   │   ├── 200X/
│   │   │   └── 400X/
│   │   ├── phyllodes_tumor/
│   │   │   ├── 40X/
│   │   │   ├── 100X/
│   │   │   ├── 200X/
│   │   │   └── 400X/
│   │   └── tubular_adenoma/
│   │       ├── 40X/
│   │       ├── 100X/
│   │       ├── 200X/
│   │       └── 400X/
│   └── malignant/
│       ├── ductal_carcinoma/
│       │   ├── 40X/
│       │   ├── 100X/
│       │   ├── 200X/
│       │   └── 400X/
│       ├── lobular_carcinoma/
│       │   ├── 40X/
│       │   ├── 100X/
│       │   ├── 200X/
│       │   └── 400X/
│       ├── mucinous_carcinoma/
│       │   ├── 40X/
│       │   ├── 100X/
│       │   ├── 200X/
│       │   └── 400X/
│       └── papillary_carcinoma/
│           ├── 40X/
│           ├── 100X/
│           ├── 200X/
│           └── 400X/
## 📥 Utilisation

Pour utiliser ce dataset dans ton environnement Kaggle :

```python
# Chemin vers le dataset sur Kaggle
DATA_ROOT = "/kaggle/input/datasets/ambarish/breakhis/"
```

Pour une utilisation locale, télécharge le dataset depuis Kaggle et ajuste le chemin.

## 📊 Répartition des images

Le dataset est déséquilibré, ce qui justifie l'utilisation de techniques comme le **WeightedRandomSampler** dans ce projet :

- **Classes malignes** : ~70% des images
  - Ductal Carcinoma : classe majoritaire
  - Papillary Carcinoma : classe minoritaire problématique
- **Classes bénignes** : ~30% des images

## 📚 Citation

Si tu utilises ce dataset dans tes recherches, cite l'article original :

Spanhol, F., Oliveira, L. S., Petitjean, C., Heutte, L.
"A Dataset for Breast Cancer Histopathological Image Classification"
IEEE Transactions on Biomedical Engineering, Vol. 63, No. 7, pp. 1455-1462, 2016
DOI: 10.1109/TBME.2015.2496264

## ⚖️ Licence

Le dataset BreaKHis est disponible pour un usage académique et de recherche uniquement.

## 🔗 Ressources complémentaires

- [Article original (IEEE)](https://ieeexplore.ieee.org/document/7312934)
- [Documentation Kaggle](https://www.kaggle.com/datasets/ambarish/breakhis)
- [Site officiel du dataset](https://web.inf.ufpr.br/vri/databases/breast-cancer-histopathological-database-breakhis/)

- 
