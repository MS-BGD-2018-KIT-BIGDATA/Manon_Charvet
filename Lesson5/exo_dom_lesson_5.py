# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement
# d'honoraires ? Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les
# dépassement d'honoraires ? Est ce que la densité de certains médecins / praticiens est corrélé à la densité de
# population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

####################
# LOAD DATA
#url_all_excel = 'http://www.data.drees.sante.gouv.fr/ReportFolders/reportFolders.aspx?IF_ActivePath=P,490,497,514'

#Honoraires
#Load data from excel file
honoraires_file = './Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
honoraires_xl = pd.ExcelFile(honoraires_file)
#2 sheets: 'Généralistes et MEP' & 'Spécialistes'
df_hon_generalist = honoraires_xl.parse('Généralistes et MEP')
df_hon_specialist = honoraires_xl.parse('Spécialistes')

#Density
density_file = './Effectif_et_densite_par_departement_en_2014.xls'
density_xl = pd.ExcelFile(density_file)
df_dens_generalist = density_xl.parse('Généralistes et MEP')
df_dens_specialist = density_xl.parse('Spécialistes')
# Cleaning empty columns
for i in range(5, 12):
    del df_dens_specialist['Unnamed: ' + str(i)]


####################
# CONCATENATION
df_density = pd.concat([df_dens_specialist, df_dens_generalist])
df_honoraire = pd.concat([df_hon_specialist, df_hon_generalist])

#df_dens.rename(columns = {'EFFECTIF':'EFFECTIFS'}, inplace = True)

df = pd.merge(df_density,df_honoraire)


####################
# CLEANING ???
df['TOTAL DES HONORAIRES (Euros)'] = df['TOTAL DES HONORAIRES (Euros)'].replace('nc', np.nan)
#df[[df['TOTAL DES HONORAIRES (Euros)']] != 'NaN']
df['DEPASSEMENTS (Euros)'] = df['DEPASSEMENTS (Euros)'].replace('nc', np.nan)
#df[[df['DEPASSEMENTS (Euros)']] != 'NaN']
#df['percent_dep'] = df['DEPASSEMENTS (Euros)']/df['TOTAL DES HONORAIRES (Euros)']
#print(df)


####################
#Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les
# dépassement d'honoraires ?
#densite = df['DENSITE /100 000 hab.']
#print(densite)
honoraires = df[['DENSITE /100 000 hab.','DEPASSEMENTS (Euros)','TOTAL DES HONORAIRES (Euros)']]
#honoraires_cleaned = honoraires.drop(honoraires.index[[1,3]])
honoraires_cleaned = honoraires.dropna(axis=0)
honoraires_cleaned = honoraires_cleaned[honoraires_cleaned['DEPASSEMENTS (Euros)']!=0.0]
#print(honoraires_cleaned)

pourcentage_depass_hon = honoraires_cleaned['DEPASSEMENTS (Euros)']/honoraires_cleaned['TOTAL DES HONORAIRES (Euros)']
#print(honoraires_cleaned)
densite = honoraires_cleaned['DENSITE /100 000 hab.']
print(densite)
print(pourcentage_depass_hon)



#print(df['DENSITE /100 000 hab.', 'DEPASSEMENTS (Euros)', 'TOTAL DES HONORAIRES (Euros)'])




####################
# PLOT
#print(df['DENSITE /100 000 hab.'])
#print(df['DENSITE /100 000 hab.'])
#plt.plot(df['DENSITE /100 000 hab.'], df['DEPASSEMENTS (Euros)'])
#fig, ax = plt.subplots()
#ax.scatter(df['EFFECTIFS'], df['DEPASSEMENTS (Euros)'], marker='+')
#plt.xlabel('Effectifs')
#plt.ylabel('Dépassements att')
#plt.show()



print('fini')
