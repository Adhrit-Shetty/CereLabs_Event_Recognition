function isNodeInstalled() {
    echo "Checking if Node is installed ..."
    if command --version node &>/dev/null; then
        echo "Installing Node ..."
        curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
        sudo apt-get install nodejs
        sudo apt-get install build-essential
        echo "Node has been installed."
        sleep 1
        updateNode
    else
        echo "Node has already been installed."
        sleep 1
        
    fi
}

function isNpmInstalled() {
    echo "Checking if npm is installed ..."
    if command -version npm &>/dev/null; then
        echo "Installing npm ..."
        curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
        sudo apt-get install nodejs
        sudo apt-get install build-essential
        echo "npm has been installed."
        sleep 1
        updateNode
    elif command -version npm != '5.6.0'; then
        sudo npm i -g npm to update
        echo "npm has been updated"
    else
        echo "npm has already been installed."
        sleep 1
        
    fi
}

# activate () {
#     /bin/bash "source ~/tensorflow/bin/activate"
#     echo 'here!'
# }

function install_required_packages(){
    echo "installing required node packages"
    sudo npm --prefix ./Electron_scripts/ install
    echo "required npm packages installed" 
}

function python_packages()
{
    read -p "Do you have a virtualenv for python(Y/N) : " dec
    if [[ "$dec" = "Y" || "$dec" = "y" ]];then
        read -p "Enter name of virtual environment : " directory
        if [ -d "$HOME/$directory" ]; then
            echo "Virtual environment exists"  
            echo "Finding out version of python"
            PYV=`~/$directory/bin/python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
            echo $PYV
            if [[ "$PYV" = '3.6' ]];then
                echo "installing required PYTHON packages"
                sudo ~/$directory/bin/pip install -r ./Python_scripts/requirements.txt
                echo "required PYTHON packages installed" 
            else
                echo "Install python 3.6 and then run the script"    
            fi
        else
            echo "No such virtual env exist"
        fi    
    else
        echo "Finding out version of python"
        PYV=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
        echo $PYV
        if [[ "$PYV" = '3.6' ]];then
            echo "installing required PYTHON packages"
            sudo pip install -r ./Python_scripts/requirements.txt
            echo "required PYTHON packages installed" 
        else
            echo "Install python 3.6 and then run the script"    
        fi
    fi
}
main(){
    # . ~/$1/.env/bin/activate
    # activate $1
    clear
    isNodeInstalled
    isNpmInstalled
    install_required_packages
    python_packages
}

main 