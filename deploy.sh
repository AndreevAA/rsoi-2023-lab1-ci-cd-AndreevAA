mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "$SSH_PRIVATE_KEY" | tr -d '\r' > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
ssh-keyscan -H $VM2_IP >> ~/.ssh/known_hosts
sshpass -p $VM2_PASSWORD ssh -o StrictHostKeyChecking=no root@$VM2_IP "
echo "$VM2_PASSWORD" | sudo -S ls
cd rsoi-2023-lab1-ci-cd-AndreevAA
sudo docker-compose up --build -d
exit 0
"  
