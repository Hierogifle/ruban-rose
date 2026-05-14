# 🎗️ Ruban Rose - Breast Cancer Histopathological Classification

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-GPU%20T4x2-20BEFF.svg)](https://www.kaggle.com/)

> **Classification automatique de tumeurs mammaires à partir d'images histopathologiques utilisant des modèles de Vision Transformer optimisés.**

Dans le cadre du projet **Octobre Rose**, ce projet développe un système d'aide au diagnostic pour la détection précoce du cancer du sein. Grâce à la computer vision et au deep learning, l'objectif est d'identifier automatiquement les premiers signes du cancer et d'augmenter les chances de rémission.

---

## 🎯 Contexte et Objectifs

### Le Défi Médical

Les **carcinomes canalaires invasifs** (Invasive Ductal Carcinoma) représentent près de **80% des cas de cancer du sein**. Une détection précoce et précise est cruciale pour :
- Améliorer le taux de survie à 5 ans (actuellement ~99% pour un cancer localisé)
- Réduire le temps de diagnostic
- Standardiser l'analyse histopathologique
- Diminuer la charge de travail des pathologistes

### Objectifs du Projet

1. **Classifier automatiquement** 8 types de tumeurs (4 bénignes + 4 malignes)
2. **Optimiser les performances** sur les classes minoritaires difficiles
3. **Comparer plusieurs architectures** de deep learning (ResNet-50, Vision Transformer)
4. **Gérer le déséquilibre des classes** avec des techniques avancées (WeightedRandomSampler)
5. **Produire un modèle déployable** avec des métriques de production

---

## 📊 Dataset

### BreaKHis - Breast Cancer Histopathological Database

- **7 909 images** histopathologiques couleur (RGB)
- **82 patientes** (données anonymisées)
- **8 classes** de tumeurs mammaires
- **4 grossissements** : 40X, 100X, 200X, 400X

#### Classes de tumeurs :

**Tumeurs bénignes (30%)** :
- Adenosis
- Fibroadenoma
- Phyllodes Tumor
- Tubular Adenoma

**Tumeurs malignes (70%)** :
- Ductal Carcinoma (majoritaire)
- Lobular Carcinoma
- Mucinous Carcinoma
- **Papillary Carcinoma** (minoritaire - classe difficile)

🔗 **[Télécharger le dataset sur Kaggle](https://www.kaggle.com/datasets/ambarish/breakhis)**

Voir [data/README.md](data/README.md) pour plus de détails.

---

## 🏗️ Architecture du Projet

ruban-rose/
├── notebooks/
│   └── 04_vit_optuna_weighted.ipynb    # Notebook principal Version 4
├── results/
│   ├── figures/                         # Graphiques et visualisations
│   │   ├── confusion_matrix_v4.png
│   │   ├── roc_curves_v4.png
│   │   └── training_history_v4.png
│   └── metrics/                         # Métriques d'évaluation
│       └── classification_report_v4.csv
├── data/
│   └── README.md                        # Documentation du dataset
├── documentation/
│   └── Sujet_pdf_Projet_Ruban_rose.pdf  # Cahier des charges
├── requirements.txt                      # Dépendances Python
├── LICENSE                               # Licence MIT
└── README.md                             # Ce fichier

---

## 🚀 Installation et Utilisation

### Prérequis

- Python 3.10+
- CUDA 11.8+ (pour l'accélération GPU)
- 16 GB RAM minimum
- GPU recommandé (Tesla T4, V100, ou supérieur)

### Installation

```bash
# Cloner le repository
git clone https://github.com/Hieroglife/ruban-rose.git
cd ruban-rose

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution

#### Sur Kaggle (Recommandé)

1. Uploader le notebook sur Kaggle
2. Activer le GPU (T4 x2)
3. Ajouter le dataset BreaKHis
4. Run All (~90 minutes)

#### En local

```bash
# Télécharger le dataset depuis Kaggle
# Ajuster le chemin DATA_ROOT dans le notebook

# Lancer Jupyter
jupyter notebook

# Ouvrir notebooks/04_vit_optuna_weighted.ipynb
```

---

## 🧠 Modèles et Méthodologie

### Architecture : Vision Transformer (ViT)

Le modèle utilise **Google ViT-base-patch16-224** pré-entraîné sur ImageNet-21k :

- **Architecture** : Vision Transformer (self-attention)
- **Patches** : 16×16 pixels
- **Input size** : 224×224×3
- **Paramètres** : ~86M
- **Fine-tuning** : Classification head adapté à 8 classes

### Optimisation des Hyperparamètres : Optuna

Optimisation Bayésienne sur 20 trials :
- **Learning rate** : [1e-5, 1e-3]
- **Batch size** : [16, 32, 64]
- **Optimizer** : Adam, AdamW, SGD
- **Weight decay** : [1e-5, 1e-2]
- **Dropout** : [0.1, 0.5]

### Gestion du Déséquilibre : WeightedRandomSampler

Pour gérer les classes minoritaires (Papillary Carcinoma) :

```python
# Calcul des poids inversement proportionnels à la fréquence
class_counts = compute_class_weights(dataset)
sample_weights = [class_counts[label] for _, label in dataset]

# Weighted sampler pour sur-échantillonner les classes minoritaires
sampler = WeightedRandomSampler(
    weights=sample_weights,
    num_samples=len(sample_weights),
    replacement=True
)
```

### Data Augmentation

Techniques appliquées pour améliorer la généralisation :
- Random horizontal/vertical flips
- Random rotation (±15°)
- Color jitter (brightness, contrast)
- Random affine transformations
- Normalization (ImageNet stats)

---

## 📈 Résultats

### Performance Globale

| Modèle | Accuracy | F1-Score (macro) | Training Time |
|--------|----------|------------------|---------------|
| ResNet-50 (Baseline) | 87.3% | 0.84 | 45 min |
| ViT + Optuna | 91.2% | 0.89 | 75 min |
| **ViT + Optuna + WeightedSampler** | **92.8%** | **0.91** | **90 min** |

### Résultats par Classe (Version 4 - WeightedSampler)

| Classe | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| **Ductal Carcinoma** | 0.96 | 0.98 | **0.97** | 450 |
| **Lobular Carcinoma** | 0.94 | 0.95 | **0.95** | 320 |
| Mucinous Carcinoma | 0.88 | 0.85 | 0.87 | 180 |
| **Papillary Carcinoma** | 0.82 | 0.79 | **0.80** | 120 |
| Adenosis | 0.91 | 0.93 | 0.92 | 280 |
| Fibroadenoma | 0.89 | 0.91 | 0.90 | 250 |
| Phyllodes Tumor | 0.93 | 0.94 | 0.94 | 200 |
| Tubular Adenoma | 0.85 | 0.82 | 0.83 | 150 |

### Impact du WeightedRandomSampler

Amélioration significative sur les classes difficiles :

| Classe | F1 sans sampler | F1 avec sampler | Gain |
|--------|-----------------|-----------------|------|
| **Papillary Carcinoma** | 0.59 | **0.80** | **+21%** ✅ |
| **Mucinous Carcinoma** | 0.79 | **0.87** | **+8%** ✅ |
| Tubular Adenoma | 0.91 | 0.83 | -8% ⚠️ |

**Trade-off observé** : L'amélioration des classes minoritaires se fait au détriment d'une légère baisse sur Tubular Adenoma (classe bien représentée initialement).

---

## 🔬 Analyse et Insights

### Points Forts

✅ **Papillary Carcinoma** : +21% F1-score grâce au WeightedSampler  
✅ **Ductal/Lobular Carcinoma** : Excellentes performances (F1 > 0.95)  
✅ **Robustesse** : Bonnes performances sur toutes les classes (F1 > 0.80)  
✅ **Généralisation** : Data augmentation efficace  

### Points d'Amélioration

⚠️ **Tubular Adenoma** : Légère baisse avec le sampler (-8%)  
⚠️ **Temps d'entraînement** : 90 min sur GPU T4×2  
⚠️ **Complexité du modèle** : 86M paramètres (ViT)  

### Recommandations

1. **Focal Loss** : Alternative au WeightedSampler pour gérer le déséquilibre
2. **Ensemble Methods** : Combiner ViT + ResNet pour améliorer la robustesse
3. **Test-Time Augmentation (TTA)** : Améliorer la généralisation en inférence
4. **Architecture plus légère** : ViT-small ou EfficientNet pour le déploiement

---

## 🛠️ Technologies Utilisées

### Deep Learning & ML
- **PyTorch 2.0+** : Framework de deep learning
- **TorchVision** : Modèles pré-entraînés et transformations
- **Optuna** : Optimisation bayésienne des hyperparamètres
- **Albumentations** : Data augmentation avancée

### Data Science
- **NumPy** : Calcul numérique
- **Pandas** : Manipulation de données tabulaires
- **Scikit-learn** : Métriques et preprocessing

### Visualisation
- **Matplotlib** : Graphiques et plots
- **Seaborn** : Visualisations statistiques

### Infrastructure
- **Kaggle** : GPU Tesla T4 x2, environnement cloud
- **Jupyter Notebook** : Développement interactif

---

## 📚 Références

### Dataset
Spanhol, F., Oliveira, L. S., Petitjean, C., Heutte, L.
"A Dataset for Breast Cancer Histopathological Image Classification"
IEEE Transactions on Biomedical Engineering, Vol. 63, No. 7, pp. 1455-1462, 2016
DOI: 10.1109/TBME.2015.2496264

### Modèles
- [Vision Transformer (ViT) - Dosovitskiy et al., 2021](https://arxiv.org/abs/2010.11929)
- [Deep Residual Learning (ResNet) - He et al., 2016](https://arxiv.org/abs/1512.03385)

### Techniques
- [Optuna: A Next-generation Hyperparameter Optimization Framework](https://arxiv.org/abs/1907.10902)
- [Focal Loss for Dense Object Detection - Lin et al., 2017](https://arxiv.org/abs/1708.02002)

---

## 👨‍💻 Auteur

**Olivier Bonnin**  
Master IA/DATA - La Plateforme  
Projet Ruban Rose - Octobre Rose 2025

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

Le dataset BreaKHis est utilisé sous licence académique uniquement.

---

## 🙏 Remerciements

- **La Plateforme** pour l'encadrement pédagogique
- **Kaggle** pour l'infrastructure GPU gratuite
- **Spanhol et al.** pour le dataset BreaKHis
- **Google Research** pour le modèle Vision Transformer pré-entraîné
- **Communauté Octobre Rose** pour la sensibilisation au cancer du sein

---

## 📞 Contact & Support

Pour toute question ou suggestion :
- 🐙 GitHub : [@olivier-bonnin](https://github.com/olivier-bonnin)

---

<p align="center">
  <i>« Grâce au dépistage anticipé et aux traitements modernes, le taux de survie à 5 ans pour un cancer du sein localisé est d'environ 99 %. »</i>
</p>

<p align="center">
  🎗️ <b>Ensemble contre le cancer du sein</b> 🎗️
</p>
