"""
Name : Automatic Database Backup
Author : burakustuner
Date : 01.11.2022
Description : This script can be used to create daily&monthly backups of database and check&remove old backup files.
"""

import os
import shutil
import time
from datetime import date

#----------------------------------------------------Giriş----------------------------------------------------------------------#
gunsayisi = 30 # Kaç gün önceki yedekler silinecek.
#DB bağlantı bilgileri
host="1.1.1.1"
port="5432"
username="postgres"
password="password"
database="test"

script_path=(os.path.dirname(os.path.realpath(__file__)))
dizin = script_path+'/gunluk_yedek' #'C:/path/vt_yedek/gunluk_yedek' # Günlük Yedeklerin oluşturulacağı ve taranacağı dizin. Varsayılan olarak scriptin olduğu klasörden çalışır.

#-------------------------------------------------------------------------------------------------------------------------------#
rapor=os.path.abspath(os.path.join(dizin, os.pardir))+"/rapor.txt"
def cleanBackupFolder():
    for root,_,files in os.walk(dizin):
        for f in files:            
            dosyayolu = os.path.join(root, f)
            veri_tarihi = os.path.getctime(dosyayolu)
            dosya_adi=os.path.basename(os.path.normpath(dosyayolu))
            if f.endswith('.backup'):
                if (time.time() - veri_tarihi) // (24 * 3600) >= gunsayisi:
                    try:
                        os.remove(dosyayolu)
                        print("Silinen dosya:", dosya_adi)
                        f = open(rapor, "a+", encoding="utf-8")
                        f.write(str(dosyayolu)+"silindi.\n")
                        f.close()                        
                    except:
                        print("HATA->Dosya silinemedi:", dosya_adi)
                        f = open(rapor, "a+", encoding="utf-8")
                        f.write("HATA dosya silinemedi ! ->" + str(dosyayolu)+"\n")
                        f.close()   
                else:
                    print(dosya_adi,'dosyası korundu.')
                    
def backupDatabase():
    tarih = date.today().strftime("%d-%m-%Y")
    dosya_adi =tarih + '.backup'
    try:
        print("Günlük yedekleme başladı.")
        os.chdir(dizin)
        os.system('SET PGPASSWORD='+password+'&pg_dump --file '+dosya_adi+' --host '+host+' --port '+port+' --username '+username+' --no-password --verbose --format=c --blobs '+database)
        print("Günlük yedekleme tamamlandı.")
        f = open(rapor, "a+", encoding="utf-8")
        f.write(str(dosya_adi)+" "+ "Günlük Yedekleme Başarılı\n")
        f.close()          
        if date.today().strftime("%d")=="01":
            try:            
                kaynak=os.path.abspath(dizin)+"/"+dosya_adi            
                hedef =os.path.abspath(os.path.join(dizin, os.pardir))+"/aylik_yedek/"+dosya_adi
                shutil.copyfile(kaynak, hedef)
                print("Aylık yedekleme yapıldı.")
                f = open(rapor, "a+", encoding="utf-8")
                f.write(str(dosya_adi)+" "+ "Aylık Yedekleme Başarılı\n")
                f.close()
            except:
                print("Aylık yedekleme yapılamadı.")
                f = open(rapor, "a+", encoding="utf-8")
                f.write("Hata ->"+str(dosya_adi)+" "+ "Aylık Yedekleme Başarısız\n")
                f.close()
    except:
        print("HATA->Yedekleme başarısız.")
        os.chdir(dizin)
        f = open(rapor, "a+", encoding="utf-8")
        f.write("Hata ->"+str(dosya_adi)+" "+ "Günlük Yedekleme Başarısız !!\n")
        f.close()    


backupDatabase()
cleanBackupFolder()
