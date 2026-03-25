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
if [[ ! -d "$HOME/.local/share/script_assets" ]];then mkdir $HOME/.local/share/script_assets; fi
cp main.py $HOME/.local/share/script_assets

# installing vsc extension
code --install-extension ./*.vsix
