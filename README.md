# MiniAss

## Installation

Pour installer la commande `miniassc`, exécutez le script suivant :

```bash
bash install-miniassc.sh
```

---

## Traducteur MiniAss

MiniAss est un langage pseudo-assembleur créé pour simplifier l'utilisation du pseudo-assembleur du professeur Ledent (Cours CI2 UPC Grands-Moulins).

Exécuter l'assembleur est possible à cette adresse : https://www.irif.fr/~ledent/teaching/ci2/

---

## Mots-clés

* `move {adr} {val}` : met la valeur `val` à l'adresse `adr`.
* `add/sub/mul/div/mod {adr} {val1} {val2}` : effectue l'opération respective entre `val1` et `val2` (dans cet ordre) et stocke le résultat à l'adresse `adr`.
* `jump {li}` : saute jusqu'à la ligne `li`.
* `jump_eq/jump_neq/jump_g/jump_ge/jump_l/jump_le {val1} {val2} {li}` : compare `val1` et `val2`. Si le résultat est vrai, saute à la ligne `li`.
* `call {li}` : stocke la ligne courante dans la stack et saute à la ligne `li`.
* `ret` : saute à la ligne en tête de la stack.
* `malloc {adr} {val}` : alloue `val` cases mémoire dans le heap et stocke l'adresse de référence dans `adr`.
* `label {nom}` : crée un alias de numéro de ligne utilisable partout où un numéro de ligne est à préciser. Le nom doit être précédé d'un `$`.
* `loop ... end` : crée un bloc de boucle. Fonctionne toujours par paire ; s'il n'y a pas de `jump` vers l'extérieur, crée une boucle infinie.
* `push *{val}` : ajoute toutes les valeurs `val` en haut de la stack.
* `pop ~{val}` : supprime les `val` valeurs en haut de la stack (argument optionnel, équivalent à `pop 1` si absent).
* `halt` : termine le programme (équivalent à `exit` en bash).
* `print *{val}` : affiche les valeurs `val` séparées par des espaces.
* `println *{val}` : pareil que `print` mais saute une ligne à la fin.

---

## Balise spéciale

* `-break` : désigne la ligne du prochain mot-clé `end`. S'utilise partout où un numéro de ligne est nécessaire. Très utile pour sortir d'un bloc `loop ... end`.

---

## Registres

* `R0/R1/R2/R3/R4/R5/R6/R7` : manipulables à volonté. Conventionnellement, `R0` est utilisé pour stocker la valeur de retour d'une fonction.
* `SP` : (Stack Pointer) désigne l'adresse mémoire en haut de la stack.
* `PC` : (Program Counter) désigne le numéro de la ligne en train d'être exécutée.

---

## Gestion Mémoire

* `[adr]` : désigne la valeur dans le heap à l'adresse `adr`. L'opérateur `+` est autorisé.

### Exemple : Création de tableau

```miniassembly
malloc R0 3
move R1 0
loop
    jump_g R1 3 -break
    mul R2 R1 4
    move [R0 + R1] R2
    add R1 R1 1
end
print "le tableau en R0 contient:" [R0] [R0+1] [R0+2]
halt
```

Résultat attendu :

```
le tableau en R0 contient: 0 4 8
```

---

## Notes

Des modifications peuvent être ajoutées ultérieurement.

version 0.0.1

### Crédits
Boris Phalippou sabredeboris@gmail.com  
