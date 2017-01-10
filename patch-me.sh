#! /bin/bash
# 	File name 	: 	patch-me.sh
#	Version		: 	
#	Date		: 	
#	Author		: 	M. QUILLE
#	Description	: 	-
#	

#	Fichier mis à jour avec ce patch :
#		* horloge.pyw v1.0.0
#		* confAppli.ini v1.0.0
#				

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

# Sync
sync
sleep 3

# Kill process
#kill -9 "$PPID"
#sleep 3

# Start process
#python /home/pi/Horloge/soft/horloge.pyw &

# Fin du script
