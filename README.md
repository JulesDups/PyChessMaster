# PyChessMaster

Un jeu d'échecs complet développé en Python avec pygame, offrant une expérience de jeu fluide et intuitive.

![Chess Board](assets/img/board_preview.png)

## Fonctionnalités

- **Interface graphique complète** basée sur pygame
- **Implémentation des règles officielles d'échecs** :
  - Mouvements spécifiques pour chaque pièce (Roi, Dame, Tour, Fou, Cavalier, Pion)
  - Prise en passant
  - Roque (petit et grand)
  - Promotion des pions
  - Détection des situations d'échec
  - Détection automatique d'échec et mat
- **Assistance au joueur** :
  - Surbrillance des cases où la pièce sélectionnée peut se déplacer
  - Indication visuelle lorsque le roi est en échec
- **Fonctionnalités d'interface** :
  - Indicateur du joueur actif
  - Historique des coups
  - Message de fin de partie

## Prérequis

- Python 3.10 ou supérieur
- Bibliothèque pygame

## Installation

1. Clonez le dépôt ou téléchargez les fichiers source

```bash
git clone https://github.com/votre-nom/PyChessMaster.git
cd PyChessMaster
```

2. Installez les dépendances requises

```bash
pip install pygame
```

## Lancement du jeu

Exécutez le fichier principal pour démarrer le jeu :

```bash
python chess.py
```

## Comment jouer

1. **Sélectionner une pièce** : Cliquez sur l'une de vos pièces
2. **Déplacer une pièce** : Cliquez sur une case en surbrillance pour déplacer la pièce sélectionnée
3. **Promotion de pion** : Lorsqu'un pion atteint la dernière rangée, sélectionnez la pièce souhaitée dans la fenêtre qui apparaît
4. **Fin de partie** : Le jeu se termine automatiquement par échec et mat, pat, ou abandon

## Structure du projet

```
PyChessMaster/
├── chess.py           # Point d'entrée principal
├── board.py           # Gestion du plateau et affichage
├── events.py          # Gestion des événements utilisateur
├── moves.py           # Validation des mouvements
├── utils.py           # Fonctions utilitaires
├── assets/            # Ressources graphiques
│   └── img/           # Images des pièces et du plateau
└── README.md          # Documentation
```

## Commandes en jeu

| Action                 | Commande                                       |
| ---------------------- | ---------------------------------------------- |
| Sélectionner une pièce | Clic gauche sur la pièce                       |
| Déplacer une pièce     | Clic gauche sur une case de destination valide |
| Annuler la sélection   | Clic droit ou clic sur une autre pièce         |
| Quitter le jeu         | Fermer la fenêtre ou touche Échap              |

## Développement futur

- [ ] Mode joueur contre IA avec plusieurs niveaux de difficulté
- [ ] Gestion du temps (horloge d'échecs)
- [ ] Sauvegarde et chargement de parties
- [ ] Notation algébrique des coups
- [ ] Mode en ligne pour jouer contre d'autres joueurs

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
