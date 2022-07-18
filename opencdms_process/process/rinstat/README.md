# Development notes for `cdms_products.py`
IDEMS International, Stephen Lloyd

This document contains extracts of personal notes that I made when I set up my development environment for `cdms_products.py`. 

I do not claim these notes are complete, or that this is the optimal development environment. I share these notes in case they are useful for other developers. Please feel free to correct or enhance these notes.

We could also add a Wiki page for this repo.
## Set up development environment
### Install WSL with Ubuntu 20.04 LTS
- Set up Windows Subsystem for Linux (WSL). The instructions are [here](https://docs.microsoft.com/en-us/windows/wsl/setup/environment). 
- However `wsl –install` did not work on my laptop. The instructions say 'you must be running a recent build of Windows (Build 20262+)'. I could only upgrade to '19044I'. So I followed the manual instructions [here](https://docs.microsoft.com/en-us/windows/wsl/install-manual)
- I executed steps 1 to 6
- In Step 6, I selected Ubuntu 20.04 LTS
### Install R
See instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-20-04).
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
sudo apt update
sudo apt install r-base
sudo -i R
```
### Fork GitHub repos
Fork these 3 repos (see [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo)):
- https://github.com/opencdms/opencdms-process
- https://github.com/opencdms/pyopencdms
- https://github.com/opencdms/opencdms-test-data

### Install Git
Check we have the latest version of Git, and set user name, email and credential manager. See [here](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-git).
```bash
sudo apt-get install git
git config --global user.name "Stephen Lloyd"
git config --global user.email stephen.lloyd03@gmail.com
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/libexec/git-core/git-credential-manager-core.exe"

# clone GitHub repos
mkdir -p ~/opencdms/processes
cd ~/opencdms/processes
git clone https://github.com/lloyddewit/opencdms-process.git
git clone https://github.com/lloyddewit/pyopencdms.git
git clone https://github.com/lloyddewit/opencdms-test-data.git

# add reference to upstream
cd opencdms-process
git remote add upstream https://github.com/opencdms/opencdms-process.git
git remote -v
cd ~/opencdms/processes
```
### Set up Python 3.8.10
```bash
#setup virtual environment
sudo apt-get install python3-venv
python3 -m venv opencdms-env
. opencdms-env/bin/activate

#install pip3
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
pip3 install --upgrade pip

# install mysqlclient, see https://askubuntu.com/questions/1321141/unable-to-install-mysqlclient-on-ubuntu-20-10
sudo apt install python3-dev build-essential
sudo apt install libssl1.1
sudo apt install libssl1.1=1.1.1f-1ubuntu2
sudo apt install libssl-dev
sudo apt install libmysqlclient-dev
pip3 install mysqlclient>=2.0.3

# manual install steps to get opencdms-process/requirements.txt to execute
sudo apt-get update -y
sudo apt-get install -y python3-psycopg2
sudo apt install libpq-dev
pip3 install psycopg2>=2.9.1
pip3 install -r ~/opencdms/processes/opencdms-process/requirements.txt
pip3 install -r ~/opencdms/processes/pyopencdms/requirements.txt

# manual install steps to pyopencdms/requirements_dev.txt to execute
pip3 install click>=7.1.2
pip3 install -r ~/opencdms/processes/pyopencdms/requirements_dev.txt

# Add `opencdms` to the virtual environment's python path
echo $HOME"/opencdms/processes/pyopencdms/" > opencdms-env/lib/python3.8/site-packages/opencdms.pth
```
### Install VS Code
Set [here](https://code.visualstudio.com/docs/remote/wsl-tutorial).
```bash
cd ~/opencdms/processes
code .
```
This should install VS Code server and then launch the VS Code client.
I installed the Python and GitHub VS Code extensions for WSL
For Python, I was prompted automatically.
For GitHub I installed manually.

### Installed `cdms.products`
```r
sudo -i R
devtools::install_github("IDEMSInternational/cdms.products")
is_available <- require("cdms.products")
is_available
[1] TRUE
q()
```
### Installed VS Code `Juypter` extension
Installed WSL `Juypter` extension so that I could view data frame contents in VS Code debugger. See [here](https://stackoverflow.com/questions/60097076/view-dataframe-while-debugging-in-vs-code).
### Installed `black` formatter
`black` is an opinionated formatter, it will automatically format the code on save. For this repo, all developers should install Black, with the default settings, so that the code has a consistent format regardless of which developer wrote/maintained the code.

In VS Code terminal window (Python environment):
```python
pip3 install black
```
Set up VS Code to use black formatter on save. See [here](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0).
## Odd problems I had, and how I fixed them
### Pytest could not find the functions in the `r-instat` directory
Solution:
- The minus in `r-instat` seemed to be causing problems
- Created a new directory called `rinstat`
- Moved all the `r-instat` files to the new folder
- Added a `__init__.py` file to the new folder
- There was also an `r_instat.py` file in the parent directory, this was making the autocomplete confusing
- I renamed `r-instat.py` to `windrose.py` and moved it to the `rinstat` directory
### Could not install R `devtools`
I followed the instructions [here]( https://community.rstudio.com/t/i-cant-install-any-package-on-linux-ubuntu-with-the-install-packages-function/97735).
The solution was to manually remove all the existing R directories, and then reinstall R from scratch
```bash
R -e '.libPaths()'
sudo rm -r /usr/local/lib/R/site-library
sudo rm -r /usr/lib/R/site-library
sudo rm -r /usr/lib/R/library
sudo apt-get remove r-base-core
sudo apt-get remove r-base
sudo apt-get autoremove

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
sudo apt update
sudo apt install r-base
sudo apt install build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev

sudo -i R 
install.packages('devtools')
devtools::install_github("IDEMSInternational/RInstatClimatic")
```

### Could not install R `clifro` pacakage
The RInstatClimatic installation failed trying to install the R `clifro` package with ‘Error, nc-config not found or not executable’.
I found a solution [here](https://stackoverflow.com/questions/42891050/install-ncdf4-package-error-nc-config-not-found-or-not-executable).
```bash
sudo apt-get install libnetcdf-dev
which nc-config
sudo -i R 
install.packages("ncdf4")
devtools::install_github("IDEMSInternational/RInstatClimatic")
is_available <- require("RInstatClimatic")
is_available
[1] TRUE
```
### VS Code test discovery failed
The only warning was that no packages were installed in "/usr/lib/R/site-library".
So I installed an arbitrary package at this location and the VS Code test discovery worked!

```r
sudo -i R
install.packages("naflex", lib="/usr/lib/R/site-library")
q()
```


