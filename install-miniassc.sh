#! /bin/bash
cd $PWD
if [[ ! -d "$HOME/.local/bin" ]]
then mkdir $HOME/.local/bin
echo "# add $HOME/.local/bin to PATH. added by install-miniassc.sh
case $PATH in 
*":$HOME/.local/bin:"*);;
*) PATH=$HOME/.local/bin:$PATH 
esac" >> $HOME/.bashrc
cd
. .bashrc
fi
chmod +x miniassc
cp miniassc $HOME/.local/bin
if [[ ! -d "$HOME/.local/share/script_assets" ]];
then mkdir $HOME/.local/share/script_assets; fi
cp main.py $HOME/.local/share/script_assets
cp $0 $HOME/.local/share/script_assets

# uninstalling previous extension
code --list-extensions | grep "miniassembly" | while read extension;
do
    #echo $extension
    code --uninstall-extension $extension --force
done

# installing vsc extension latest version
file=$(curl -s https://api.github.com/repos/Terre456/MiniAssembly-vsc-extension/contents/ | jq -r '.[] | select(.name | contains(".vsix")).name'| sort -Vr | head -1)
curl -L -O "https://raw.githubusercontent.com/Terre456/MiniAssembly-vsc-extension/master/$file"
code --install-extension $file