## Exécution avec Docker

Pour lancer le conteneur Docker de SQL Server, exécutez la commande suivante dans votre terminal :

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=Your$tr0ngP@ssw0rd!" -p 1433:1433 1588081b6d03
```

ACCEPT_EULA=Y : Accepte le contrat de licence.

SA_PASSWORD : Définit le mot de passe pour l'utilisateur sa.

-p 1433:1433 : Expose le port 1433 pour accéder à SQL Server depuis l'hôte.

1588081b6d03 : ID de l'image Docker.



## Gestion des Migrations

Ce projet utilise **Flask-Migrate** pour gérer l'évolution du schéma de la base de données.

### Initialiser les migrations

Pour initialiser les migrations, utilisez la commande suivante :

```bash
flask db init
```

### Mettre à jour une bdd existante

Marquer les migrations comme appliquées et la bdd comme à jour

```bash
flask db stamp head
```


### Créer une migration

Pour générer un script de migration à partir des modifications dans vos modèles, utilisez la commande suivante :

```bash
flask db migrate -m "migration message"
```

### Appliquer une migration

Pour appliquer une migration à la base de données, utilisez la commande suivante :

```bash
flask db upgrade
```

### Annuler une migration

Pour annuler la dernière migration appliquée à la base de données, utilisez la commande suivante :

```bash
flask db downgrade
```

### Historique des migrations

Pour afficher l'historique des migrations appliquées à la base de données, utilisez la commande suivante :

```bash
flask db history
```

### Documentation API avec Swagger

Pour accéder à la documentation de l'API avec Swagger, ouvrez le lien suivant dans votre navigateur :

```
http://localhost:5000/api/docs
```


