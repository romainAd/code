# Corrélation entre les variables 

bivars = data[['categ','price','panier_moyen','age']] # Sélection des variables significatives
corr = bivars.corr()

print('\nTable des corrélations entre les variables significatives\n')
corr

# Mission 3

## Y a-t-il une corrélation entre le sexe des clients et les catégories de produits achetés ?

# Deux variables qualitatives(tranche d'âge et catégorie de produit acheté) 

 # Générer un tableau de contingence
 # Heatmap
 # Khi-2

# =================================================   Test de khi-2   ==========================================================

# Deux variables qualitatives. Une variable influence une autre variable?  ==+> Test du Khi 2 (χ²)
# La variable dépendante est celle qui peut changer : 'categ'.
# La variable indépendante, est celle qui ne peut changer chez l’individu :'sex'

# Hypothèse nulle   : Il n’y a pas de lien.
# Hypothèse valable : Il y a un lien.

# Trouver le degré de liberté : il faut trouver les valeurs dépendantes dans ces lignes et colonnes du tableau. 
# Cela s’obtient en multipliant le nombre de lignes du tableau moins un par le nombre de colonnes moins un 
# Pour chaque ligne il y a 2-1 = 1 variables indépendantes, et pour chaque colonne il y a 4-1 = 3  variable indépendante. ????
# Ce qui conduit à  1*3 = 3 degrés de liberté.

# Choisir le risque de se tromper, c’est-à-dire de rejeter à tort l'hypothèse nulle. 5 % de chance de se tromper est le seuil de probabilité le plus souvent choisi. 


**1 - Tableau de contingence**

X = "sex"
Y = "categ"

cont = data[[X,Y]].pivot_table(index=X,columns=Y,aggfunc=len,margins=True,margins_name="Total")
cont

**2 - Heatmap**

# Heatmap
plt.figure(figsize=(5,5))
tx = cont.loc[:,["Total"]]
ty = cont.loc[["Total"],:]
n = len(data)
indep = tx.dot(ty) / n

c = cont.fillna(0) # On remplace les valeurs nulles par 0
measure = (c-indep)**2/indep
xi_n = measure.sum().sum()
table = measure/xi_n
sns.heatmap(table.iloc[:-1,:-1],annot=c.iloc[:-1,:-1])
plt.show()

**3 - Khi-2**

# Deux variables qualitatives ===> calculer khi-2

chi2, pvalue, degrees, expected = chi2_contingency(cont)
chi2, degrees, pvalue

print('\nkhi-2 : {}  \nDegré de liberté : {}  \npvalue : {}'.format(chi2,degrees,pvalue))

## Corrélations avec l'âge

### Y a-t-il une corrélation entre l\'âge des clients  et le montant total des achats

# Une variable qualitative ordinale(tranche d'âge) et une variable quantitatiave(total des achats) ===> ANOVA

# Hypothèse H0 : Il n'y a pas de lien entre la tranche d'âge des clients et le montant total des achats
# Hypothèse H1 : Il y a un lien entre la tranche d'âge des clients et le montant total des achats

plt.figure(figsize=(5,6))
sns.boxplot(x='groupe_age', y='panier_moyen', data=data)
plt.show()

**Boîtes à moustaches panier moyen en fonction des tranches d'âges  ===> on note une différence 
entre les montants de panier moyen suivant les tranches d'âges**

**ANOVA**

mod = ols('panier_moyen ~ groupe_age', data=data).fit()
anova_table = anova_lm(mod, type=2)
print('\nTable ANOVA\n')
print(anova_table)

**p = 0 ===> H0 rejeté ===> Il existe bien un lien entre la tranche d\'âge des clients et le montant total des achats**

## Y a-t-il une corrélation entre l'âge des clients et la fréquence d’achat (ie. nombre d'achats par mois par exemple)

**Une variable qualitative ordinale(tranche d\'âge) et une variable quantitatiave
(fréquence d'achats, nombre d'achats par mois) ===> ANOVA**


# Boîtes à moustaches nombre d'achats par mois en fonction des tranche d'âge  

# Hypothèse H0 : Il n'y a pas de lien entre la tranche d'âge des clients et le montant total des achats
# Hypothèse H1 : Il y a un lien entre la tranche d'âge des clients et le montant total des achats

**Calcul du nombre d\'achats effectués par mois**

data['nb_achat'] = 1
nb_session_achat_mois = data[['mois_achat','nb_achat','session_id']]
nbre_achat_mois = nb_session_achat_mois.groupby(['mois_achat']).sum()
nbre_achat_mois_reset_index = nbre_achat_mois.reset_index()
nbre_achat_mois_reset_index

# Jointure de la table du nombre de ventes avec celle des données globales

s = pd.merge(nbre_achat_mois_reset_index, data, on = 'mois_achat')

# Correction de la table issue de la jointure

s.rename(columns={'nb_achat_x':'nb_achat_mois'}, inplace=True)
u = s.drop('nb_achat_y', axis=1)
u

# Boîtes à moustaches nombre d'achats effectués par mois en fonction des tranches d'âge  ===> on note peu de différences 
# entre le nombre d'achats effectués par mois  en les groupes d'âges ??????

plt.figure(figsize=(6,6))
sns.boxplot(x='groupe_age', y='nb_achat_mois', data=u)
plt.title('\nBoîte à moustache du nombre d\'achats par tranches d\'âges \n')
plt.xlabel('\nGroupe d\'âge')
plt.ylabel('Nombre d\'achats\n')

plt.show()

**ANOVA**

# ANOVA
mod = ols('nb_achat_mois ~ groupe_age', data=u).fit()
anova_table = anova_lm(mod, type=2)
print('\nTable ANOVA\n')
print(anova_table)

**Hypothèse H0 retenu ===> Il n\'y a pas de lien entre la tranche d'âge des clients et le montant total des achats**

## Y a-t-il une corrélation entre l'âge des clients et la taille du panier moyen (en nombre d’articles)

# Hypothèse H0 : Il n'y a pas de lien entre l'âge des clients et la taille du panier moyen (en nombre d’articles)
# Hypothèse H1 : Il y a un lien entre l'âge des clients et la taille du panier moyen (en nombre d’articles)

**Calcul du nombre d\'articles achetés par produit**

nb_articles = data[['nb_achat','id_prod']]

nb_articles_mois = nb_articles.groupby(['id_prod']).sum()
nb_articles_mois_reset_index = nb_articles_mois.reset_index()
nb_articles_mois_reset_index.rename(columns={'nb_achat':'nb_articles'}, inplace=True)
nb_articles_mois_reset_index

# Table prenant en compte le nombre d'articles achetés par mois

p = pd.merge(nb_articles_mois_reset_index, data, on = 'id_prod')
p

# Article le plus vendu

p['nb_articles'].max()

# Identification de l'article le plus vendu
p.loc[p['nb_articles'] == 1081]


#import qgrid
widget_ved = qgrid.show_grid(p, show_toolbar=True)
widget_ved

**Une variable qualitative ordinale(tranche d\'âge) et une variable quantitatiave(nombre d\'articles) ===> ANOVA**

# Boîtes à moustaches 'nombre d'articles' en fonction des tranches d'âge  ===> on note une différence 
# entre les montants de panier moyen en les catégories

plt.figure(figsize=(6,6))
sns.boxplot(x='groupe_age', y='nb_articles', data=p)
plt.show()

**ANOVA**

# ANOVA
mod = ols('nb_articles ~ groupe_age', data=p).fit()
anova_table = anova_lm(mod, type=2)
print('\nTable ANOVA\n')
print(anova_table)

**Hypothèse H0 rejeté ==> Il n'y a pas de lien entre l\'âge des clients et la taille du panier moyen (en nombre d’articles)**

**2.3 Y a-t-il une corrélation entre l'âge des clients et la taille du panier moyen (en nombre d'articles)**

## Y a-t-il une corrélation entre l'âge des clients et les catégories de produits achetés

# Deux variables qualitatives ===> Générer un tableau de contingence
# Heatmap
# Deux variables qualitatives(tranche d'âge et catégorie de produit acheté) ===> Khi-2

**1 - Table de contingence**

X = "groupe_age"
Y = "categ"

cont_a = data[[X,Y]].pivot_table(index=X,columns=Y,aggfunc=len,margins=True,margins_name="Total")
cont_a

**2 - Heatmap**

# Heatmap

plt.figure(figsize=(5,5))
tx = cont_a.loc[:,["Total"]]
ty = cont_a.loc[["Total"],:]
n = len(data)
indep = tx.dot(ty) / n

c = cont_a.fillna(0) # On remplace les valeurs nulles par 0
measure = (c-indep)**2/indep
xi_n = measure.sum().sum()
table = measure/xi_n
sns.heatmap(table.iloc[:-1,:-1],annot=c.iloc[:-1,:-1])
plt.show()

**3 - Khi-2**

# Khi-2
chi2, pvalue, degrees, expected = chi2_contingency(cont_a)
chi2, degrees, pvalue
print('\nkhi-2 : {}  \nDegré de liberté : {}  \npvalue : {}'.format(chi2,degrees,pvalue))