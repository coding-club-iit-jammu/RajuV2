pwd
sudo pm2 delete raju
cp -r /home/azureuser/azagent/_work/r2/a/_coding-club-iit-jammu_RajuV2/* /home/azureuser/RajuV2/
cd /home/azureuser/RajuV2/
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo pm2 -f start raju.py --no-autorestart --interpreter /home/azureuser/RajuV2/venv/bin/python
sudo pm2 startup systemd
sudo pm2 save