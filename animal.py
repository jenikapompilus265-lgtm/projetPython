import csv


class Animal:
    """Représente un animal du zoo avec validation des données."""

    STATUTS_VALIDES = ("Bon", "Sous surveillance", "Malade")
    SEUIL_SENIOR = 15  # années — justifié : espérance de vie moyenne élevée chez grands mammifères

    def __init__(self, identifiant, nom, espece, age, poids, enclos, statut_sante):
        self.identifiant = self._valider_identifiant(identifiant)
        self.nom = self._valider_texte(nom, "nom")
        self.espece = self._valider_texte(espece, "espèce")
        self.age = self._valider_age(age)
        self.poids = self._valider_poids(poids)
        self.enclos = self._valider_texte(enclos, "enclos")
        self.statut_sante = self._valider_statut(statut_sante)

    # ---------- Validations ----------
    @staticmethod
    def _valider_identifiant(identifiant):
        if identifiant is None or str(identifiant).strip() == "":
            raise ValueError("L'identifiant ne peut pas être vide.")
        return str(identifiant).strip()

    @staticmethod
    def _valider_texte(valeur, champ):
        if valeur is None or str(valeur).strip() == "":
            raise ValueError(f"Le champ '{champ}' ne peut pas être vide.")
        return str(valeur).strip()

    @staticmethod
    def _valider_age(age):
        try:
            age = int(age)
        except (ValueError, TypeError):
            raise ValueError("L'âge doit être un nombre entier.")
        if age < 0 or age > 100:
            raise ValueError("L'âge doit être compris entre 0 et 100.")
        return age

    @staticmethod
    def _valider_poids(poids):
        try:
            poids = float(poids)
        except (ValueError, TypeError):
            raise ValueError("Le poids doit être un nombre.")
        if poids <= 0:
            raise ValueError("Le poids doit être strictement supérieur à 0.")
        return poids

    @staticmethod
    def _valider_statut(statut):
        if statut not in Animal.STATUTS_VALIDES:
            raise ValueError(
                f"Statut invalide. Valeurs autorisées : {', '.join(Animal.STATUTS_VALIDES)}"
            )
        return statut

    # ---------- Méthodes métier ----------
    def modifier_infos(self, nom=None, espece=None, age=None, poids=None,
                       enclos=None, statut_sante=None):
        if nom is not None:
            self.nom = self._valider_texte(nom, "nom")
        if espece is not None:
            self.espece = self._valider_texte(espece, "espèce")
        if age is not None:
            self.age = self._valider_age(age)
        if poids is not None:
            self.poids = self._valider_poids(poids)
        if enclos is not None:
            self.enclos = self._valider_texte(enclos, "enclos")
        if statut_sante is not None:
            self.statut_sante = self._valider_statut(statut_sante)

    def est_senior(self, seuil=None):
        seuil = seuil if seuil is not None else self.SEUIL_SENIOR
        return self.age >= seuil

    def afficher_infos(self):
        return (f"[{self.identifiant}] {self.nom} ({self.espece}) — "
                f"{self.age} ans, {self.poids} kg, enclos {self.enclos}, "
                f"santé : {self.statut_sante}")

    def to_dict(self):
        return {
            "identifiant": self.identifiant,
            "nom": self.nom,
            "espece": self.espece,
            "age": self.age,
            "poids": self.poids,
            "enclos": self.enclos,
            "statut_sante": self.statut_sante,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["identifiant"], d["nom"], d["espece"], d["age"],
                   d["poids"], d["enclos"], d["statut_sante"])

    def __str__(self):
        return self.afficher_infos()

    def __repr__(self):
        return f"Animal({self.identifiant!r}, {self.nom!r})"