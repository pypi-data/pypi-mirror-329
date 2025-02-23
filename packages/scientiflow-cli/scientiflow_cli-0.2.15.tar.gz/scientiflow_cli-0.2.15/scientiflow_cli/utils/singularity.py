import subprocess
from pathlib import Path

import requests


def run_command(command, check=True):
    try:
        result = subprocess.run(
            command,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\n{e.stderr}")
        raise


def command_exists(command):
    result = subprocess.run(
        ["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.returncode == 0


def update_and_install_dependencies():
    print("[+] Updating package repository and installing dependencies...")
    run_command(["sudo", "apt", "update"])

    dependencies = [
        "cryptsetup-bin",
        "libfuse2",
        "uidmap",
        "fuse2fs",
        "fuse",
        "liblzo2-2",
        "squashfs-tools",
        "runc",
    ]
    run_command(["sudo", "apt-get", "install", "-y", *dependencies])


def install_go():
    if command_exists("go"):
        print("[+] Go is already installed.")
        return

    print("[+] Go not found! Installing Go")
    go_url = "https://go.dev/dl/go1.23.1.linux-amd64.tar.gz"
    temp_file = Path("/tmp/go1.23.1.linux-amd64.tar.gz")

    # Download Go tarball
    print("Downloading source files")
    response = requests.get(go_url, stream=True)
    response.raise_for_status()
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract and install Go
    print("Installing...")
    subprocess.run(["sudo", "rm", "-rf", "/usr/local/go"])
    subprocess.run(["sudo", "tar", "-C", "/usr/local", "-xzf", str(temp_file)])
    temp_file.unlink()

    # Add Go to PATH permanently
    bashrc = Path.home() / ".bashrc"
    with open(bashrc, "a") as f:
        f.write("\nexport GOPATH=${HOME}/go\n")
        f.write("export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin\n")
    print(
        "[+] Successfully Installed GO. Please source ~/.bashrc or restart the shell."
    )


def install_singularity():
    if command_exists("singularity"):
        print("[+] Singularity is already installed.")
        return

    print("[+] Installing Singularity")
    # Get Ubuntu codename
    os_release_path = Path("/etc/os-release")
    ubuntu_codename = None
    if os_release_path.exists():
        for line in os_release_path.read_text().splitlines():
            if line.startswith("UBUNTU_CODENAME="):
                ubuntu_codename = line.split("=")[1]
                break

    if not ubuntu_codename:
        raise ValueError("Could not determine Ubuntu codename from /etc/os-release.")

    singularity_url = f"https://github.com/sylabs/singularity/releases/download/v4.2.1/singularity-ce_4.2.1-{ubuntu_codename}_amd64.deb"
    temp_file = Path(f"/tmp/singularity-ce_4.2.1-{ubuntu_codename}_amd64.deb")

    # Download Singularity deb package
    print("Downloading Singularity package")
    response = requests.get(singularity_url, stream=True)
    response.raise_for_status()
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Install Singularity
    subprocess.run(["sudo", "dpkg", "-i", str(temp_file)], check=True)
    temp_file.unlink()
    print("Installation complete")


def install_singularity_main():
    update_and_install_dependencies()
    install_go()
    install_singularity()


if __name__ == "__main__":
    install_singularity_main()

