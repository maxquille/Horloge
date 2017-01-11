#! /bin/bash
# 	File name 	: 	patch-me.sh
#	Release		: 	CHL_v1.1
#	Date		: 	
#	Author		: 	M. QUILLE
#	Description	: 	-
#	

#	Versions des fichiers :
#		* horloge.pyw 			: 1.0.0
#		* confAppli.ini 		: CHL_v0.1.0.0
#		* logo.png				: CHL_v0.1.0.0
#		* distrib_version.txt	: raspberry_HorlogeImgBase_1.0.0.img

cd /tmp/

sleep 3

# Copie du script
cp ./horloge.pyw /home/pi/Horloge/soft

# Copie du fichier de conf
cp ./confAppli.ini /home/pi/Horloge/soft

# Mise Logo
cp ./logo.png /home/pi/Horloge/soft

# Mise à jour de l'OS


# Archivage de l'ancienne archive
mv /home/pi/Horloge/patch_horloge_current.tar.gz /home/pi/Horloge/backup/patch_horloge_backup.tar.gz

# Copie de l'archive
cp ./patch_horloge.tar.gz /home/pi/Horloge/patch_horloge_current.tar.gz

# Mise à jour de la version GLOBAL projet
echo "CHL_v1.1" > /version_global_projet.txt

# Sync
sync
sleep 3

# Fin du script
