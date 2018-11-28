montants = {
	"< 10 000 euros": 0,
	"> = 10 000 euros et < 25 000 euros" : 1,
	"> = 25 000 euros et < 50 000 euros" : 2,
	"> = 50 000 euros et < 75 000 euros" : 3,
	"> = 75 000 euros et < 100 000 euros" : 4,
	"> = 100 000 euros et < 200 000 euros" : 5,
	"> = 200 000 euros et < 300 000 euros" : 6,
	"> = 300 000 euros et < 400 000 euros" : 7,
	"> = 400 000 euros et < 500 000 euros" : 8,
	"> = 500 000 euros et < 600 000 euros" : 9,
	"> = 600 000 euros et < 700 000 euros" : 10,
	"> = 700 000 euros et < 800 000 euros" : 11,
	"> = 800 000 euros et < 900 000 euros" : 12,
	"> = 900 000 euros et < 1 000 000 euros" : 13,
	"> = 1 000 000 euros et < 1 250 000 euros" : 14,
	"> = 1 250 000 euros et < 1 500 000 euros" : 15,
	"> = 1 500 000 euros et < 1 750 000 euros" : 16,
	"> = 1 750 000 euros et < 2 000 000 euros" : 17,
	"> = 2 000 000 euros et < 2 250 000 euros" : 18,
	"> = 2 250 000 euros et < 2 500 000 euros" : 19,
	"> = 2 500 000 euros et < 2 750 000 euros" : 20,
	"> = 2 750 000 euros et < 3 000 000 euros" : 21,
	"> = 3 000 000 euros et < 3 250 000 euros" : 22,
	"> = 3 250 000 euros et < 3 500 000 euros" : 23,
	"> = 3 500 000 euros et < 3 750 000 euros" : 24,
	"> = 3 750 000 euros et < 4 000 000 euros" : 25,
	"> = 4 000 000 euros et < 4 250 000 euros" : 26,
	"> = 4 250 000 euros et < 4 500 000 euros" : 27,
	"> = 4 500 000 euros et < 4 750 000 euros" : 28,
	"> = 4 750 000 euros et < 5 000 000 euros" : 29,
	"> = 5 000 000 euros et < 5 250 000 euros" : 30,
	"> = 5 250 000 euros et < 5 500 000 euros" : 31,
	"> = 5 500 000 euros et < 5 750 000 euros" : 32,
	"> = 5 750 000 euros et < 6 000 000 euros" : 33,
	"> = 6 000 000 euros et < 6 250 000 euros" : 34,
	"> = 6 250 000 euros et < 6 500 000 euros" : 35,
	"> = 6 500 000 euros et < 6 750 000 euros" : 36,
	"> = 6 750 000 euros et < 7 000 000 euros" : 37,
	"> = 7 000 000 euros et < 7 250 000 euros" : 38,
	"> = 7 250 000 euros et < 7 500 000 euros" : 39,
	"> = 7 500 000 euros et < 7 750 000 euros" : 40,
	"> = 7 750 000 euros et < 8 000 000 euros" : 41,
	"> = 8 000 000 euros et < 8 250 000 euros" : 42,
	"> = 8 250 000 euros et < 8 500 000 euros" : 43,
	"> = 8 500 000 euros et < 8 750 000 euros" : 44,
	"> = 8 750 000 euros et < 9 000 000 euros" : 45,
	"> = 9 000 000 euros et < 9 250 000 euros" : 46,
	"> = 9 250 000 euros et < 9 500 000 euros" : 47,
	"> = 9 500 000 euros et < 9 750 000 euros" : 48,
	"> = 9 750 000 euros et < 10 000 000 euros" : 49,
	"> = 10 000 0000 euros": 50
}

import json, requests, csv
from datetime import datetime
from pprint import pprint

date = datetime.now().strftime('%d%m%Y')

print('Téléchargement du fichier de la HATVP...')
try:
	resp = requests.get(url="http://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json")
	data = json.loads(resp.text)
except:
	print("Erreur dans le téléchargement !")

print("Fichier téléchargé et bien rangé.")

### Montants déclarés

f = open('entreprises'+date+'.csv', 'w')
wr = csv.writer(f,quoting=csv.QUOTE_ALL)

wr.writerow(["nom","idEnt","dateDebut","dateFin","montant"])

for publication in data['publications']:
	nom = publication['denomination']
	idEnt = publication['identifiantNational']
	for exercice in publication['exercices']:
		dateDebut = exercice['publicationCourante']['dateDebut']
		dateFin = exercice['publicationCourante']['dateFin']
		try: 
			montant = str(montants.get(exercice['publicationCourante']['montantDepense']))
		except:
			print("Pas de montant pour "+publication["denomination"]+"...")
			montant = ""	
		wr.writerow([nom,idEnt,dateDebut,dateFin,montant])

f.close()
print("Les informations sur les entreprises ont été récupérées.")

### Activités

f = open('activites'+date+'.csv', 'w')
wr = csv.writer(f,quoting=csv.QUOTE_ALL)

wr.writerow(["nom","idEnt","urlEnt","dateDebut","dateFin","montant","idAct","urlAct","objet","domaines","resp","actions","tiers"])

for publication in data['publications']:

	nom = publication['denomination']
	idEnt = publication['identifiantNational']
	urlEnt = "https://www.hatvp.fr/fiche-organisation/?organisation="+publication['identifiantNational']


	for exercice in publication["exercices"]:
		dateDebut = exercice['publicationCourante']['dateDebut']
		dateFin = exercice['publicationCourante']['dateFin']
		try:
			montant = str(montants.get(exercice['publicationCourante']['montantDepense'],'default'))
		except:
			montant = ""

		try:
			for activite in exercice['publicationCourante']["activites"]:
				idAct = activite['publicationCourante']["identifiantFiche"]
				urlAct = "https://www.hatvp.fr/fiche-organisation/?organisation="+publication['identifiantNational']+"&fiche="+activite['publicationCourante']["identifiantFiche"]
				objet = activite['publicationCourante']["objet"].replace('"','')
				try:
					domaines = ("|").join(activite['publicationCourante']["domainesIntervention"])
				except:
					domaines = ""
					print("Souci dans les domaines pour "+publication["denomination"]+"...")
				try:
					for action in activite['publicationCourante']['actionsRepresentationInteret']:
						resp = ("|").join(action["reponsablesPublics"])
						actions = ("|").join(action["actionsMenees"])
						tiers = ("|").join(action["tiers"])
						wr.writerow([nom,idEnt,urlEnt,dateDebut,dateFin,montant,idAct,urlAct,objet,domaines,resp,actions,tiers])
				except:
					wr.writerow([nom,idEnt,urlEnt,dateDebut,dateFin,montant,idAct,urlAct,objet,domaines,"","",""])
		except:
			print("Aucune activité pour "+publication["denomination"]+" n'a été trouvée")

f.close()
print("Les informations sur les activités ont été récupérées.")

### Employés

f = open('employes'+date+'.csv', 'w')
wr = csv.writer(f,quoting=csv.QUOTE_ALL)

wr.writerow(["nom","idEnt","civilite","nom complet","nom","fonction"])

for publication in data['publications']:
	nom = publication['denomination']
	idEnt = publication['identifiantNational']
	for collaborateur in publication["collaborateurs"]:
		civilite = collaborateur["civilite"]
		nomcc = collaborateur["prenom"]+" "+collaborateur["nom"]
		nomc = collaborateur["nom"]
		if("fonction" in collaborateur):
			fonction = collaborateur["fonction"]
		else:
			fonction = ""
		wr.writerow([nom,idEnt,civilite,nomcc,nomc,fonction])
	for dirigeant in publication["dirigeants"]:
		civilite = collaborateur["civilite"]
		nomcc = collaborateur["prenom"]+" "+collaborateur["nom"]
		nomc = collaborateur["nom"]
		if("fonction" in collaborateur):
			fonction = collaborateur["fonction"]
		else:
			fonction = ""
		wr.writerow([nom,idEnt,civilite,nomcc,nomc,fonction])

f.close()
print("Les informations sur les collaborateurs ont été récupérées.")
print("C'est bon, tout s'est bien passé !")