#!/bin/bash

echo
echo "+======================"
echo "| START: SPAWNHUB"
echo "+======================"
echo

echo
echo "SPAWNHUB: Incrementing build number"
echo
cv=`cat version.txt`
nlbn="$(echo $cv | rev | cut -d. -f1 | rev)"
nbn=`echo $nlbn | awk '{$1++; print $0}'`
nb=${cv%.*}"."${nbn}
echo $nb > version.txt

echo 
echo "SPAWNHUB: Inserting new build numbers into dockerfile"
echo
host=`uname -a`
case "${host}" in
    Darwin*)
        esccv=$(echo "${cv}" | sed -e 's/[]$.*[\^]/\\&/g' )
        escnb=$(echo "${nb}" | sed -e 's/[]$.*[\^]/\\&/g' )
        sed -i '' "s/${esccv}/${escnb}/" Dockerfile
        ;;
    *)
        esccv=`echo ${cv} | head -c -1 | cut -d' ' -f1`
        escnb=`echo ${nb} | head -c -1 | cut -d' ' -f1`
        echo $esccv
        echo $escnb
        sed -i.bak s/$esccv/$escnb/g Dockerfile
esac

echo 
echo "SPAWNHUB: Building SPA"
echo
cd SpawnHubSPA
dotnet publish -c Release
cd ..

echo 
echo "SPAWNHUB: Copying Ansible"
echo
cp ../ansible.cfg ./AnsibleContent/
cp ../automation-agent.j2 ./AnsibleContent/
cp ../deployConfig.json ./AnsibleContent/
cp ../playbook.yaml ./AnsibleContent/
cp ../omPlaybook* ./AnsibleContent/
cp ../gskygrogan_cmdemo.pem ./AnsibleContent/key.pem
cp ../credentials ./
cp ../awsconfig ./awsconfig
cp -r ../tls ./AnsibleContent/
cp -r ../src ./AnsibleContent/
cp ../thp.service ./AnsibleContent/

echo 
echo "SPAWNHUB: Building container"
echo
docker build -t graboskyc/mongodb-sa-sm-spawnhub:latest -t graboskyc/mongodb-sa-sm-spawnhub:v${nb} .

echo 
echo "SPAWNHUB: Starting container"
echo
docker stop testqacmsh
docker rm testqacmsh
docker run -t -i -d -p 8000:8000 --name testqacmsh --restart unless-stopped -e "APIPW=bW9uZ29yb2Nrcw" -v /var/run/docker.sock:/var/run/docker.sock graboskyc/mongodb-sa-sm-spawnhub:v${nb}

echo
echo "+======================"
echo "| END: SPAWNHUB"
echo "+======================"
echo
