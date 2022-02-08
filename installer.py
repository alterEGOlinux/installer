#!/usr/bin/env python
## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOlinux/installer/installer.py                                      ##
##   created        : 2022-02-02 11:53:41 UTC                                ##
##   updated        : 2022-02-08 11:27:40 UTC                                ##
##   description    : Install alterEGO Linux.                                ##
## _________________________________________________________________________ ##

import argparse
from collections import namedtuple
import os
import shlex
import shutil
import subprocess
import time

## [ CONFIGURATION ] ------------------------------------------------------- ##

timezone = 'America/New_York'
hostname = 'pc1'
root_passwd = 'toor'
user = 'hacker'
user_passwd = 'password1'

Package = namedtuple('Package', ['name', 'repository', 'mode'])
packages = [
    Package('alsa-utils', 'official', ['bare', 'minimal']),
    Package('arp-scan', 'official', ['bare', 'minimal', 'beast']),
    Package('base-devel', 'official', ['bare']),
    Package('bash-completion', 'official', ['bare', 'minimal']),
    Package('bat', 'official', ['bare', 'minimal']),
    Package('bc', 'official', ['bare', 'minimal']),
    Package('bind', 'official', ['minimal']),
    Package('binwalk', 'official', ['bare', 'minimal', 'beast']),
    Package('bleachbit', 'official', ['bare', 'minimal']),
    Package('bpytop', 'official', ['bare', 'minimal', 'beast']),
    Package('brave-bin', 'aur', ['bare', 'minimal']),
    Package('burpsuite', 'aur', ['bare', 'minimal', 'beast']),
    Package('cmatrix', 'official', ['bare', 'minimal', 'beast']),
    Package('code', 'official', ['bare', 'minimal']),
    Package('cronie', 'official', ['bare', 'minimal']),
    Package('dirbuster', 'aur', ['bare', 'minimal', 'beast']),
    Package('docker', 'official', ['bare', 'minimal', 'beast']),
    Package('dos2unix', 'official', ['bare', 'minimal']),
    Package('dunst', 'official', ['bare', 'minimal']),
    Package('easy-rsa', 'official', ['beast']),
    Package('entr', 'official', ['bare', 'minimal']),
    Package('exfat-utils', 'official', ['bare', 'minimal', 'beast']),
    Package('feh', 'official', ['bare', 'minimal']),
    Package('ffmpeg', 'official', ['bare', 'minimal']),
    Package('firefox', 'official', ['bare', 'minimal']),
    Package('freerdp', 'official', ['bare', 'minimal']),
    Package('fzf', 'official', ['bare', 'minimal']),
    Package('gimp', 'official', ['bare']),
    Package('git', 'official', ['bare']),
    Package('gnu-netcat', 'official', ['bare', 'minimal', 'beast']),
    Package('go', 'official', ['bare', 'minimal']),
    Package('gobuster-git', 'aur', ['bare', 'minimal', 'beast']),
    Package('grc', 'official', ['bare', 'minimal', 'beast']),
    Package('gromit-mpx-git', 'aur', ['beast']),
    Package('grub', 'official', ['bare']),
    Package('htop', 'official', ['bare', 'minimal']),
    Package('i3-gaps', 'official', ['bare', 'minimal']),
    Package('i3blocks', 'official', ['bare', 'minimal']),
    Package('imagemagick', 'official', ['bare', 'minimal']),
    Package('inkscape', 'official', ['bare', 'minimal']),
    Package('inxi', 'aur', ['bare', 'minimal', 'beast']),
    Package('john', 'official', ['bare', 'minimal', 'beast']),
    Package('jq', 'official', ['bare', 'minimal']),
    Package('jre11-openjdk', 'official', ['bare', 'minimal', 'beast']),
    Package('libreoffice-fresh', 'official', ['bare', 'minimal']),
    Package('librespeed-cli-bin', 'aur', ['bare', 'minimal']),
    Package('linux', 'official', ['bare']),
    Package('lynx', 'official', ['bare']),
    Package('man-db', 'official', ['bare', 'minimal']),
    Package('man-pages', 'official', ['bare', 'minimal']),
    Package('mariadb-clients', 'official', ['bare', 'minimal', 'beast']),
    Package('metasploit', 'official', ['bare', 'minimal', 'beast']),
    Package('mlocate', 'official', ['bare', 'minimal']),
    Package('mtools', 'official', ['bare', 'minimal']),
    Package('mtr', 'official', ['bare', 'minimal', 'beast']),
    Package('net-tools', 'official', ['bare', 'minimal', 'beast']),
    Package('networkmanager', 'official', ['bare']),
    Package('nfs-utils', 'official', ['bare', 'minimal']),
    Package('nikto', 'official', ['bare', 'minimal', 'beast']),
    Package('nmap', 'official', ['bare', 'minimal', 'beast']),
    Package('ntfs-3g', 'official', ['bare', 'minimal']),
    Package('openssh', 'official', ['bare', 'minimal']),
    Package('openvpn', 'official', 'beast'),
    Package('p7zip', 'official', ['bare', 'minimal']),
    Package('pandoc-bin', 'aur', ['bare', 'minimal']),
    Package('pavucontrol', 'official', ['bare', 'minimal']),
    Package('perl-image-exiftool', 'official', ['bare', 'minimal', 'beast']),
    Package('php', 'official', ['bare', 'minimal', 'beast']),
    Package('polkit-gnome', 'official', ['bare', 'minimal']),
    Package('postgresql', 'official', ['bare', 'minimal', 'beast']),
    Package('powershell-bin', 'aur', ['bare', 'minimal', 'beast']),
    Package('pptpclient', 'official', ['bare', 'minimal']),
    Package('pulseaudio', 'official', ['bare', 'minimal']),
    Package('pv', 'official', ['bare', 'minimal', 'beast']),
    Package('python-beautifulsoup4', 'official', ['bare', 'minimal', 'beast']),
    Package('python-pandas', 'official', ['bare', 'minimal', 'beast']),
    Package('python-pip', 'official', ['bare']),
    Package('python-pyaml', 'official', ['bare', 'minimal', 'beast']),
    Package('python-rich', 'official', ['bare', 'minimal', 'beast']),
    Package('qrencode', 'official', ['bare', 'minimal', 'beast']),
    Package('qterminal', 'official', ['bare', 'minimal', 'beast']),
    Package('qtile', 'official', ['bare', 'minimal', 'beast']),
    Package('ranger', 'official', ['bare', 'minimal']),
    Package('remmina', 'official', ['bare', 'minimal']),
    Package('rsync', 'official', ['bare', 'minimal']),
    Package('rustscan', 'aur', ['bare', 'minimal', 'beast']),
    Package('screen', 'official', ['bare', 'minimal']),
    Package('screenkey', 'official', ['bare', 'minimal', 'beast']),
    Package('shellcheck', 'official', ['bare', 'minimal', 'beast']),
    Package('simple-mtpfs', 'aur', ['bare', 'minimal']),
    Package('sqlitebrowser', 'official', ['bare', 'minimal', 'beast']),
    Package('sxiv', 'official', ['bare', 'minimal']),
    Package('tcpdump', 'official', ['bare', 'minimal', 'beast']),
    Package('tesseract', 'official', ['bare', 'minimal', 'beast']),
    Package('tesseract-data-eng', 'official', ['bare', 'minimal', 'beast']),
    Package('tesseract-data-fra', 'official', ['bare', 'minimal', 'beast']),
    Package('thunar', 'official', ['bare', 'minimal']),
    Package('thunar-volman', 'official', ['bare', 'minimal']),
    Package('tidy', 'official', ['bare', 'minimal', 'beast']),
    Package('tk', 'official', ['bare', 'minimal', 'beast']),
    Package('tmux', 'official', ['bare', 'minimal']),
    Package('traceroute', 'official', ['bare', 'minimal', 'beast']),
    Package('transmission-gtk', 'official', ['bare', 'minimal']),
    Package('tree', 'official', ['bare', 'minimal']),
    Package('ufw', 'official', ['bare', 'minimal']),
    Package('unrar', 'official', ['bare', 'minimal']),
    Package('unzip', 'official', ['bare', 'minimal']),
    Package('usbutils', 'official', ['bare', 'minimal']),
    Package('vim', 'official', ['bare']),
    Package('virtualbox-guest-utils', 'official', ['bare', 'minimal']),
    Package('w3m', 'official', ['bare', 'minimal']),
    Package('wfuzz-git', 'aur', ['bare', 'minimal', 'beast']),
    Package('wget', 'official', ['bare']),
    Package('whois', 'official', ['bare', 'minimal', 'beast']),
    Package('wireshark-qt', 'official', ['beast']),
    Package('xclip', 'official', ['bare', 'minimal']),
    Package('xcompmgr', 'official', ['bare', 'minimal']),
    Package('xdotool', 'official', ['bare', 'minimal']),
    Package('xfce4-terminal', 'official', ['bare', 'minimal']),
    Package('xorg-server', 'official', ['bare', 'minimal']),
    Package('xorg-xinit', 'official', ['bare', 'minimal']),
    Package('xterm', 'official', ['bare', 'minimal']),
    Package('youtube-dl', 'official', ['bare', 'minimal', 'beast']),
    Package('zaproxy', 'official', ['beast']),
    Package('zathura', 'official', ['bare', 'minimal']),
    Package('zathura-pdf-mupdf', 'official', ['bare', 'minimal']),
    Package('zbar', 'official', ['bare', 'minimal', 'beast']),
    ]

## [ UTILS ] --------------------------------------------------------------- ##

def message(msg_type, msg, wait=0):

    foreground_blue = '\033[34m'
    foreground_green = '\033[32m'
    foreground_red = '\033[31m'
    format_bold = '\033[1m'
    format_reset = '\033[00m'

    if msg_type == "action":
        print(f"{foreground_green}[*]{format_reset} {format_bold}{msg}{format_reset}")
    elif msg_type == "result":
        print(f"{foreground_blue}[-]{format_reset} {format_bold}{msg}{format_reset}")
    elif msg_type in ["warning", "error"]:
        print(f"{foreground_red}[!]{format_reset} {format_bold}{msg}{format_reset}")
    else:
        print(f"    {format_bold}{msg}{format_reset}")

    time.sleep(wait)

def execute(cmd, cwd=None, shell=False, text=True, input=None):

    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)
    if input:
        input = input.encode()
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, input=input)

    CommandResults = namedtuple('CommandResults', ['returncode'])
    return CommandResults(cmd_run.returncode)

def packages_list(required_by, mode=None):

    pkgs_list = []
    for pkg in packages:
        if required_by in ['pacstrap', 'pacman']:
            if mode in pkg.mode and pkg.repository == 'official':
                pkgs_list.append(pkg.name)
        elif required_by in ['aur_helper']:
            if mode in pkg.mode and pkg.repository == 'aur':
                pkgs_list.append(pkg.name)

    if required_by == 'pacstrap':
        pkgs_list.append('base')

    return pkgs_list

def git_clone(name, remote, local):
    message('action', f"Cloning {remote}.", wait=0)
    if not os.path.isdir(local):
        execute(f"git clone {remote} {local}")
    else:
        execute(f"git -C {local} pull")

## [ INSTALLER CLASS ] ----------------------------------------------------- ##

class Installer:

    def __init__(self, mode):

        self.mode = mode

    def partition(self):

        ## Create partition
        message('action', f"Creating and mounting the partition...", wait=0)

        ## ref. https://superuser.com/questions/332252/how-to-create-and-format-a-partition-using-a-bash-script
        ## On the HOST, you can get the details with:
        ## $ sudo sfdisk -d /dev/sda > sda.sfdisk

        partition = '''label: dos
                    device: /dev/sda
                    unit: sectors
                    sector-size: 512

                    /dev/sda1 : start=        2048, type=83, bootable
                    '''

        execute(f"sfdisk /dev/sda", input=partition)

        ## Format file system
        message('action', f"Formating the file system...", wait=0)
        execute(f"mkfs.ext4 /dev/sda1")

    def mount(self):

        ## Mount /dev/sda1 to /mnt
        message('action', f"Mounting /dev/sda1 to /mnt...", wait=0)
        execute(f"mount /dev/sda1 /mnt")

        ## Create ${HOME}
        message('action', f"Creating /home...", wait=0)
        os.mkdir('/mnt/home')

    def pkg_prep(self):

        ## Enable pacman parallel download
        pacman_conf = '/etc/pacman.conf'
        pacman_conf_bkp = pacman_conf + '.bkp'

        shutil.move(pacman_conf, pacman_conf_bkp)

        with open(pacman_conf_bkp, 'r') as _file_in:
            with open(pacman_conf, 'w') as _file_out:
                for line in _file_in.readlines():
                    if "#ParallelDownloads = 5" in line:
                        _file_out.write(line.replace("#ParallelDownloads = 5", "ParallelDownloads = 5"))
                    else:
                        _file_out.write(line)

        os.remove(pacman_conf_bkp)

        ## Few prep.
        execute(f"rm -rf /var/lib/pacman/sync")
        execute(f"curl -o /etc/pacman.d/mirrorlist 'https://archlinux.org/mirrorlist/?country=US&protocol=http&protocol=https&ip_version=4'")
        execute(f"sed -i -e 's/\#Server/Server/g' /etc/pacman.d/mirrorlist")
        execute(f"pacman -Syy --noconfirm archlinux-keyring")

    def pkg_install(self):

        ## Packages installation.
        message('action', f"Starting pacstrap...", wait=0)
        pkgs_list = ' '.join(packages_list('pacstrap', self.mode))

        message('result', f"Will install:\n{pkgs_list}", wait=0)
        run_pacstrap = execute(f"pacstrap /mnt {pkgs_list}")

        return run_pacstrap.returncode

    def fstab(self):

        message('action', f"Generating the fstab...", wait=0)
        execute(f"genfstab -U /mnt >> /mnt/etc/fstab", shell=True)

    def chroot(self):

        message('action', f"Preparing arch-root...", wait=0)

        os.mkdirs('/mnt/usr/local/alterEGO/installer')
        execute(f'arch-chroot /mnt git clone https://github.com/alterEGOlinux/installer.git /usr/local/alterEGO/installer')
        execute(f'arch-chroot /mnt python /usr/local/alterEGO/installer/installer.py --sysconfig {self.mode}')

    def git_clone_ael(self):
        git_clone('filesystem', 'https://github.com/alterEGOlinux/filesystem.git', '/usr/local/alterEGO/')

    def set_time(self):
        message('action', f"Setting clock and timezone...", wait=0)

        os.symlink(f'/usr/share/zoneinfo/{timezone}', '/etc/localtime')
        execute(f'timedatectl set-ntp true')
        execute(f'hwclock --systohc --utc')

    def set_locale(self):
        message('action', f"Generating locale...", wait=0)

        execute(f'sed -i "s/#en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen')
        with open('/etc/locale.conf', 'w') as locale_conf:
            locale_conf.write('LANG=en_US.UTF-8')
        os.putenv('LANG', 'en_US.UTF-8')
        execute(f'locale-gen')

    def set_network(self):
        message('action', f"Setting up network...", wait=0)

        with open('/etc/hostname', 'w') as etc_hostname:
            etc_hostname.write(hostname)
        with open('/etc/hosts', 'w') as etc_hosts:
            etc_hosts.write(f'''
                            127.0.0.1	localhost
                            ::1		localhost
                            127.0.1.1	{hostname}.localdomain	{hostname}
                            ''')

        message('result', f"Enabling NetworkManager daemon...", wait=0)
        execute(f'systemctl enable NetworkManager.service')

    def deploy_files(src, dst):
        '''
        The src is the source root directory.
        The dest is the source root of the destination.
        ref. http://techs.studyhorror.com/d/python-how-to-copy-or-move-folders-recursively
        '''

        if not os.path.exists(dst):
            os.makedirs(dst)

        message('action', f"Copying files to {dst}...", wait=0)

        for src_dir, dirs, files in os.walk(src):
            dst_dir = src_dir.replace(src, dst)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
                message('result', f"Creating directory {dst_dir}.", wait=0)

            for f in files:
                src_file = os.path.join(src_dir, f)
                dst_file = os.path.join(dst_dir, f)
                message('result', f"Copying {dst_file}.", wait=0)

                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy2(src_file, dst_file)

    def users(self):
        message('action', f"Configuring users and passwords...", wait=0)

        ## root
        message('result', f"Setting password for root user.", wait=0)
        execute(f"passwd", input=f'{root_passwd}\n{root_passwd}\n')

        ## user: ghost
        message('result', f"Creating user {user}", wait=0)
        execute(f"useradd -m -g users -G wheel,docker {user}") 
        message('result', f"Setting password for {user}", wait=0)
        execute(f"passwd {user}", input=f"{user_passwd}\n{user_passwd}\n")

        message('result', f"Enabling sudoers for {user}", wait=0)
        execute(f'sed -i "s/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers')

    def swapfile(self):
        message('action', f"Creating a 1G swapfile...", wait=0)

        execute(f"fallocate -l 1G /swapfile")
        os.chmod('/swapfile', 0o600)
        execute(f"mkswap /swapfile")
        execute(f"swapon /swapfile")

        with open('/etc/fstab', 'a') as fstab_file:
            fstab_file.write("/swapfile none swap defaults 0 0")

    def aur(self):
        git_clone('paru', 'https://aur.archlinux.org/paru.git', f"/opt/.build/paru")
        execute(f"chown -R {user}:users /opt/.build/paru")
        execute(f"su {user} -c 'makepkg -si --needed --noconfirm'", cwd='/opt/.build/paru')

        message('action', f"Installing AUR packages...", wait=0)
        pkgs_list = ' '.join(packages_list('aur_helper', self.mode))
        message('result', f"Will be installed:\n{pkgs_list}", wait=0)
        execute(f"sudo -u {user} /bin/bash -c 'paru -S --noconfirm {pkgs_list}'")

    def mandb(self):
        message('action', f"Generating mandb...", wait=0)
        execute(f"mandb")

    def set_java(self):
        ## Burpsuite not running with java 16.
        ## Will need to install jre11-openjdk.
        ## $ sudo archlinux-java set java-11-openjdk

        if self.mode == 'beast':
            message('action', f"Fixing Java...", wait=0)
            execute(f"archlinux-java set java-11-openjdk")

    def bootloader(self):
        message('action', f"Installing and configuring the bootloader...", wait=0)
        execute(f'grub-install /dev/sda')
        execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

    def vbox_services(self):
        if self.mode in ['minimal', 'beast']:
            message('action', f"Starting vbox service...", wait=0)
            execute(f'systemctl start vboxservice.service')
            execute(f'systemctl enable vboxservice.service')

## [ CLI ] ----------------------------------------------------------------- ##

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=str, choices=['bare', 'minimal', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--sysconfig", type=str, choices=['bare', 'minimal', 'beast'], help="Initiate the system configuration after the base install.")

    args = parser.parse_args()

    ## [ SYSTEM PREP ] ----------------------------------------------------- ##

    if args.install:
        mode = args.install
        message('action', f"This will install AlterEGO Linux in {mode} mode...", wait=5)

        installer = Installer(mode)

        ## ( PARTITION )
        installer.partition()

        ## ( MOUNTING PARTITION )
        installer.mount()

        ## ( PACSTRAP )
        installer.pkg_prep()

        ## Temporary solution due to few failure.
        run_pacstrap = installer.pkg_install()
        message('result', f"Pacstrap exited with code: {run_pacstrap}", wait=0)
        while run_pacstrap != 0:
            ## Need to fix return None when using message()
            if input(f"\033[34m[-]\033[00m \033[1mRe-run pacstrap [Y/n]? \033[00m").lower() in ['y', 'yes']:
                run_pacstrap = installer.pkg_install()
            else:
                break

        ## ( FSTAB )
        installer.fstab()

        ## ( ARCH-CHROOT )
        installer.chroot()

        ## ( ALL DONE )
        ## Returning from chroot.
        all_done = input(f"\033[34m[-]\033[00m \033[1mShutdown [Y/n]? \033[00m")
        if all_done.lower() in ['y', 'yes']:
            message('result', f"Good Bye!", wait=5)
            try:
                execute(f'umount -R /mnt')
                execute(f'shutdown now') 
            except:
                execute(f'shutdown now') 
        else:
            message('result', f"Do a manual shutdown when ready.", wait=5)

    ## [ SYSTEM CONFIGURATION ] -------------------------------------------- ##

    if args.sysconfig:
        mode = args.sysconfig

        installer = Installer(mode)

        ## ( GIT REPOSITORIES )
        installer.git_clone_ael()

        ## ( TIMEZONE & CLOCK )
        installer.set_time()

        ## ( LOCALE )
        installer.set_locale()

        ## ( NETWORK CONFIGURATION )
        installer.set_network()

        ## ( DEPLOY FILES )
        if mode not in ['bare']:
            installer.deploy_files('/', '/usr/local/alterEGO')

        ## ( USERS and PASSWORDS )
        installer.users()

        ## ( SWAPFILE )
        installer.swapfile()

        ## ( AUR )
        installer.aur()

        ## ( GENERATING mandb )
        installer.mandb()

        ## ( SETTING JAVA DEFAULT )
        installer.set_java()

        ## ( BOOTLOADER )
        installer.bootloader()

        ## ( VIRTUALBOX SERVICES )
        installer.vbox_services()

if __name__ == '__main__':
    main()

## FIN _____________________________________________________________ ¯\_(ツ)_/¯
