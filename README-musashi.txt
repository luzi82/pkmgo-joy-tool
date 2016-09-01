sudo aptitude install python3-dev

git clone git@github.com:luzi82/pkmgo-joy-tool.git
cd pkmgo-joy-tool
git checkout -b musashi origin/musashi
git submodule init
git submodule update

cd third-party/pokemongo-api
sudo pip install -r requirements.txt
cd ../..

./prepare.sh

# edit config.json, encrypt_lib=[PROJECT_ROOT]/third-party/pgoencrypt/src/libencrypt.so
