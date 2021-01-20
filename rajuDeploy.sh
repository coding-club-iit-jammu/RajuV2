pwd
sudo pm2 delete raju
cp -r /home/azureuser/azagent/_work/r2/a/_coding-club-iit-jammu_RajuV2/* /home/azureuser/RajuV2/
cd /home/azureuser/RajuV2/
pip3 install -r requirements.txt
sudo pm2 -f start raju.py --no-autorestart --interpreter python3
sudo pm2 startup systemd
sudo pm2 save