# Questions

## Hue and Tahoma (LBC)


> J’ai des produits (autres lampes et prises connectées) qui ne sont pas de la marque Philips ainsi qu’une box TaHoma de chez Somfy. 
> Pensez vous que tout peut être pilotable à partir d’une même appli en ajoutant ce hub?  


C'est une excellente question. Piloter vos produits Hue via l'application TaHoma est effectivement une alternative possible, mais voici les points importants à prendre en compte :

### 1. L'alternative via TaHoma

L'intégration est possible (la TaHoma reconnaît le pont Hue), mais cela comporte deux limites majeures :

- **Nécessité du pont Hue** : La TaHoma ne remplace pas le hub Philips. Vous devrez toujours avoir le pont Hue branché pour que la TaHoma puisse communiquer avec vos ampoules.
- **Fonctionnalités réduites** : L'application Somfy est parfaite pour les volets, mais elle est beaucoup moins complète que l'application Hue pour la gestion des lumières (ambiances, couleurs complexes, synchronisation vidéo).
- **Le problème des produits tiers** : Vos lampes et prises d'autres marques risquent de ne pas remonter dans l'interface TaHoma, ce qui ne résoudrait pas totalement votre problème de centralisation.

### 2. Ma configuration (pour comparaison)

C'est précisément pour éviter ces limitations que j'ai structuré mon installation ainsi :

- **Un Hub Hue** : Pour garder la meilleure expérience utilisateur sur l'éclairage. <!-- En principe fonctionne qu'avec produit Hue mais prise Osram sont OK mais ont été désactivées dans le passé, voir aussi Hue and ZLL -->
- **Une box TaHoma** : Indispensable pour mes équipements Somfy en protocole io (volets, portail).
- **Home Assistant** (sur Raspberry Pi avec clé SMLIGHT) : C'est le véritable cerveau de ma maison. Il récupère les informations de mon hub Hue, de ma TaHoma, et de tous mes produits Zigbee "low cost" (IKEA, Lidl, etc.).

**En résumé :**

Si vous voulez une solution simple sans mettre les mains dans la technique, l'intégration Hue/TaHoma est un bon début, mais elle vous oblige à garder les deux hubs. Si vous voulez une seule application universelle capable de tout gérer (y compris vos prises d'autres marques), une solution comme Home Assistant reste, selon moi, la plus performante sur le long terme.


## Hue and ZLL (LBC)


Some non-Philips Hue devices use ZLL (Zigbee Light Link). The successor standard, Zigbee 3.0, is supposed to be backward-compatible with ZLL, but compatibility depends on how well the device implemented the ZLL specification.

The Hue Bridge 2.1 uses a newer, stricter Zigbee 3.0 implementation to improve security. As a result, some third-party ZLL devices that worked with Bridge 2.0 are no longer supported on Bridge 2.1.

These devices can instead be paired directly via Z2M (Zigbee2MQTT), bypassing the Hue Bridge entirely.


