#! /bin/bash
# 	File name 	: 	patch-me.sh
#	Release		: 	CHL_v1.3
#	Date		: 	
#	Author		: 	M. QUILLE
#	Description	: 	-
#	

#	Versions des fichiers :
#		* horloge.pyw 			: 1.0.1
#		* confAppli.ini 		: CHL_v0.1.0.0
#		* logo.png				: CHL_v0.1.0.0
#		* distribution			: raspberry_HorlogeImgBase_1.0.0.img

cd /tmp/

sleep 2

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
echo "CHL_v1.3" > /version_global_projet.txt

# Sync
sleep 3
sync

# Fin du script
