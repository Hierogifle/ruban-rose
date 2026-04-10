# Ruban-rose

## 8 défis du projet ruban rose

1. Déséquiloibres de classes
2. Transfert Learning & fine-tuning
3. Augmentation médicale H&E
4. Métriques d'évaluation
5. Reproductibilité & seeds
6. Pipeline DataLoader sans fuite
7. Optimisation Optuna
8. Interprétabilité Grad-CAM

Accuracy, Precission, Recall, F1-score, AUC-ROC, etc...

Solution au déséquilibre des calsses : 3 approches
1. Weighted Cross-Entropy Loss
Principe : On assigne des poids plus élevés aux classes minoritaires dans la fonction de perte. Cela permet au modèle de se concentrer davantage sur les exemples rares et d'améliorer sa capacité à les classer correctement.

w_c = N / (C * n_c)
où N est le nombre total d'exemples, C est le nombre de classes, et n_c est le nombre d'exemples dans la classe c.

Avantages :
- Simple à implémenter.
- Stable
Limite : 
- Ne rééquilibre pas les batchs, ce qui peut entraîner des gradients bruyants et une convergence plus lente.

2. Weighted Random Sampler

Principe : Chaque sample est tiré avec une probabilité inversement proportionnelle à la fréquence de sa classe. Cela garantit que les classes minoritaires sont suréchantillonnées et les classes majoritaires sont sous-échantillonnées pendant l'entraînement.

Avantages :
- Rééquilibre les batchs, ce qui peut améliorer la convergence.
- Compatible avec n'importe quelle fonction de perte.
Limite :
- Peut entraîner un surapprentissage des classes minoritaires si elles sont très rares.

3. Focal Loss
Focal Loss = -α_t * (1 - p_t)^γ * log(p_t)
où p_t est la probabilité prédite pour la classe correcte, α_t est un facteur de pondération pour équilibrer les classes, et γ est un paramètre de focalisation qui réduit l'importance des exemples bien classés.

Avantages :
- Concentre l'apprentissage sur les exemples difficiles.
Paramètres recommandés : α = [0.25, 0.75], γ = 2.0
Limite :
- Hyperparamètres y à tuner, ce qui peut être complexe.

Recommandation : Weighted Random Sampler pour un bon compromis entre simplicité et efficacité, surtout si les classes sont très déséquilibrées. Weighted Cross-Entropy Loss peut être utilisé en complément pour renforcer l'importance des classes minoritaires. Focal Loss est à considérer si les classes minoritaires sont extrêmement rares et difficiles à classer.

Autres méthodes ?



Défi 3 : Transfer Learning - Feature extraction vs Fine-Tuning

1. Feature extraction
(Backbone gelé, on n'entraîne que les couches nouvelles de classification)

Quand utiliser ?

2. Fine-tuning
(backbone partiellement dégelé, on entraîne à la fois les nouvelles couches de classification et certaines couches du backbone)



3. Differential Learning Rates
param_groups dans AdamW






