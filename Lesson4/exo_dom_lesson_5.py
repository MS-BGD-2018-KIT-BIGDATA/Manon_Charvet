# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement
# d'honoraires ? Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les
# dépassement d'honoraires ? Est ce que la densité de certains médecins / praticiens est corrélé à la densité de
# population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

import pandas as pd


url_all_excel = 'http://www.data.drees.sante.gouv.fr/ReportFolders/reportFolders.aspx?IF_ActivePath=P,490,497,514'

#data_spe = 'Effectif_et_densite_par_departement_en_2014.xls'
#data_honoraires = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'

#pd.read_excel(data_spe, sheetname=['Spécialistes', 'Généralistes et MEP'], na_values="nc")


honoraires_file = './sante/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
honoraires_xl = pd.ExcelFile(honoraires_file)




print('fini')
