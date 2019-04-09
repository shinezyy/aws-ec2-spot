sudo mkfs.ext4 $1
sudo mkdir -p /media/data
sudo mount $1 /media/data
sudo chown -R zyy:zyy /media/data
mv ~/projects/emu-run /media/data
cd ~/projects && ln -s /media/data/emu-run .

