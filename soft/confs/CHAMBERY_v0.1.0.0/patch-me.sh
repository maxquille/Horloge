#! /bin/bash
# 	File name 	: 	patch-me.sh
#	Release		: 	CHAMBERY_v1.0
#	Date		: 	
#	Author		: 	M. QUILLE
#	Description	: 	-
#	

#	Versions des fichiers :
#		* horloge.pyw 			: 1.0.4
#		* confAppli.ini 		: CHAMBERY_v0.1.0.0
#		* logo.png				: None
#		* distribution			: raspberry_HorlogeImgBase_1.0.1.img

cd /tmp/

sleep 2

# Copie du script
cp ./horloge /home/pi/Horloge/bin
chmod +x /home/pi/Horloge/bin/horloge

Copie du fichier de conf
cp ./confAppli.ini /home/pi/Horloge/bin

# Mise Logo
# cp ./logo.png /home/pi/Horloge/bin

# Mise à jour de l'OS


# Archivage de l'ancienne archive
mv /home/pi/Horloge/patch_horloge_current.tar.gz /home/pi/Horloge/backup/patch_horloge_backup.tar.gz

# Copie de l'archive
cp ./patch_horloge.tar.gz /home/pi/Horloge/patch_horloge_current.tar.gz

# Mise à jour de la version GLOBAL projet
echo "CHAMBERY_v1.0" > /version_global_projet.txt

# Sync
sleep 3
sync

# Fin du script
