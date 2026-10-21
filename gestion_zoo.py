import csv
import os
from animal import Animal


class GestionZoo:
    """Contient la liste des animaux et gère la persistance CSV."""

    EN_TETES = ["identifiant", "nom", "espece", "age", "poids",
                "enclos", "statut_sante"]

    def __init__(self, chemin_fichier_csv="animaux.csv"):
        self.liste_animaux = []
        self.chemin_fichier_csv = chemin_fichier_csv

    # ---------- CRUD ----------
    def ajouter_animal(self, animal: Animal):
        if self.rechercher_animal(animal.identifiant):
            raise ValueError(f"L'identifiant {animal.identifiant} existe déjà.")
        self.liste_animaux.append(animal)
        self.sauvegarder_dans_csv()

    def supprimer_animal(self, identifiant):
        animal = self.rechercher_animal(identifiant)
        if animal is None:
            raise ValueError(f"Aucun animal avec l'identifiant {identifiant}.")
        self.liste_animaux.remove(animal)
        self.sauvegarder_dans_csv()

    def modifier_animal(self, identifiant, **kwargs):
        animal = self.rechercher_animal(identifiant)
        if animal is None:
            raise ValueError(f"Aucun animal avec l'identifiant {identifiant}.")
        animal.modifier_infos(**kwargs)
        self.sauvegarder_dans_csv()
        return animal

    def rechercher_animal(self, identifiant):
        for a in self.liste_animaux:
            if a.identifiant == str(identifiant):
                return a
        return None

    def rechercher_par_nom(self, mot_cle):
        mot_cle = mot_cle.lower().strip()
        return [a for a in self.liste_animaux
                if mot_cle in a.nom.lower() or mot_cle in a.espece.lower()]

    def afficher_animaux(self):
        return [a.afficher_infos() for a in self.liste_animaux]

    # ---------- Classement / Doyens ----------
    def classer_animaux(self, critere="age", inverse=True):
        if critere not in ("age", "poids"):
            raise ValueError("Critère de classement invalide.")
        return sorted(self.liste_animaux,
                      key=lambda a: getattr(a, critere),
                      reverse=inverse)

    def doyen(self):
        if not self.liste_animaux:
            return None
        return max(self.liste_animaux, key=lambda a: a.age)

    def plus_lourd(self):
        if not self.liste_animaux:
            return None
        return max(self.liste_animaux, key=lambda a: a.poids)

    # ---------- Statistiques ----------
    def afficher_statistiques(self):
        if not self.liste_animaux:
            return {"total": 0}

        ages = [a.age for a in self.liste_animaux]
        poids = [a.poids for a in self.liste_animaux]

        stats = {
            "total": len(self.liste_animaux),
            "age_moyen": round(sum(ages) / len(ages), 2),
            "poids_moyen": round(sum(poids) / len(poids), 2),
            "age_max": max(ages),
            "age_min": min(ages),
            "poids_max": max(poids),
            "poids_min": min(poids),
        }

        for statut in Animal.STATUTS_VALIDES:
            stats[f"statut_{statut}"] = sum(
                1 for a in self.liste_animaux if a.statut_sante == statut
            )

        especes = {}
        for a in self.liste_animaux:
            especes[a.espece] = especes.get(a.espece, 0) + 1
        stats["par_espece"] = especes

        return stats

    # ---------- Persistance CSV ----------
    def charger_depuis_csv(self, chemin=None):
        chemin = chemin or self.chemin_fichier_csv
        if not os.path.exists(chemin):
            self._creer_fichier_vide(chemin)
            return 0, 0

        self.liste_animaux = []
        rejetees = 0

        try:
            with open(chemin, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for ligne in reader:
                    try:
                        self.liste_animaux.append(Animal.from_dict(ligne))
                    except (ValueError, KeyError):
                        rejetees += 1
        except (OSError, csv.Error) as e:
            raise IOError(f"Erreur de lecture CSV : {e}")

        return len(self.liste_animaux), rejetees

    def sauvegarder_dans_csv(self, chemin=None):
        chemin = chemin or self.chemin_fichier_csv
        try:
            with open(chemin, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.EN_TETES)
                writer.writeheader()
                for animal in self.liste_animaux:
                    writer.writerow(animal.to_dict())
        except (OSError, csv.Error) as e:
            raise IOError(f"Erreur d'écriture CSV : {e}")

    def _creer_fichier_vide(self, chemin):
        try:
            with open(chemin, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.EN_TETES)
                writer.writeheader()
        except OSError as e:
            raise IOError(f"Impossible de créer {chemin} : {e}")